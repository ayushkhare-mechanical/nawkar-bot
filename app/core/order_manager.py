import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
from app.core.fyers_handler import fyers_auth

class OrderManager:
    def __init__(self, paper_trading: bool = True):
        self.paper_trading = paper_trading
        self.active_trades: Dict[str, Any] = {} # symbol -> trade_details
        self.trade_history_file = "logs/trade_history.json"
        self._load_history()

    def _load_history(self):
        if os.path.exists(self.trade_history_file):
            try:
                with open(self.trade_history_file, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = []
        else:
            self.history = []

    def execute_signal(self, symbol: str, signal_data: Dict[str, Any], current_price: float, strategy_config: Dict[str, Any]):
        """Decide whether to enter or exit a trade based on signals"""
        
        # 1. Handle Entry
        if signal_data.get('entry_signal') and symbol not in self.active_trades:
            self.enter_trade(symbol, current_price, strategy_config)
            
        # 2. Handle Exit
        elif signal_data.get('exit_signal') and symbol in self.active_trades:
            self.exit_trade(symbol, current_price, "Strategy Signal")

    def enter_trade(self, symbol: str, entry_price: float, config: Dict[str, Any]):
        """Calculate SL/Target and place entry order"""
        risk = config.get('risk_management', {})
        sl_perc = risk.get('stop_loss_perc', 1.0)
        target_perc = risk.get('target_perc', 2.0)
        
        sl_price = entry_price * (1 - sl_perc / 100)
        target_price = entry_price * (1 + target_perc / 100)
        
        trade = {
            "symbol": symbol,
            "entry_price": entry_price,
            "entry_time": datetime.now().isoformat(),
            "sl_price": sl_price,
            "target_price": target_price,
            "status": "OPEN",
            "qty": 1 # Default for now
        }
        
        print(f"[ORDER] Entering {symbol} at {entry_price}. SL: {sl_price:.2f}, Tgt: {target_price:.2f}")
        
        if not self.paper_trading:
            token = fyers_auth.load_access_token()
            if token:
                order_data = {
                    "symbol": symbol,
                    "qty": trade["qty"],
                    "type": 2, # Market Order
                    "side": 1, # Buy
                    "productType": "INTRADAY",
                    "limitPrice": 0,
                    "stopPrice": 0,
                    "validity": "DAY",
                    "disclosedQty": 0,
                    "offlineOrder": False,
                }
                response = fyers_auth.place_order(token, order_data)
                print(f"FYERS RESPONSE: {response}")
                trade["fyers_order_id"] = response.get("id")
            
        self.active_trades[symbol] = trade

    def exit_trade(self, symbol: str, exit_price: float, reason: str):
        """Place exit order and record results"""
        trade = self.active_trades.pop(symbol, None)
        if not trade: return
        
        trade["exit_price"] = exit_price
        trade["exit_time"] = datetime.now().isoformat()
        trade["exit_reason"] = reason
        trade["status"] = "CLOSED"
        trade["pnl"] = (exit_price - trade["entry_price"]) * trade["qty"]
        
        print(f"[ORDER] Exiting {symbol} at {exit_price}. Reason: {reason}. PnL: {trade['pnl']:.2f}")
        
        if not self.paper_trading:
            token = fyers_auth.load_access_token()
            if token:
                order_data = {
                    "symbol": symbol,
                    "qty": trade["qty"],
                    "type": 2, # Market Order
                    "side": -1, # Sell
                    "productType": "INTRADAY",
                    "limitPrice": 0,
                    "stopPrice": 0,
                    "validity": "DAY",
                    "disclosedQty": 0,
                    "offlineOrder": False,
                }
                response = fyers_auth.place_order(token, order_data)
                print(f"FYERS RESPONSE: {response}")
            
        self.history.append(trade)
        self._save_history()

    def check_risk_management(self, symbol: str, current_price: float):
        """Monitor price for SL or Target hit"""
        trade = self.active_trades.get(symbol)
        if not trade: return
        
        if current_price <= trade["sl_price"]:
            self.exit_trade(symbol, current_price, "Stop Loss Hit")
        elif current_price >= trade["target_price"]:
            self.exit_trade(symbol, current_price, "Target Hit")

    def _save_history(self):
        os.makedirs(os.path.dirname(self.trade_history_file), exist_ok=True)
        with open(self.trade_history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

order_manager = OrderManager(paper_trading=True)
