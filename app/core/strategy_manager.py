import json
import os
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path
from app.core.order_manager import order_manager

class StrategyManager:
    def __init__(self, strategies_dir: str = "app/strategies"):
        self.strategies_dir = strategies_dir
        self.active_strategies = []
        self.data_frames: Dict[str, pd.DataFrame] = {} # symbol -> ohlcv
        self.load_strategies()

    def load_strategies(self):
        """Load all JSON strategies from the strategies directory"""
        self.active_strategies = []
        path = Path(self.strategies_dir)
        if not path.exists():
            return

        for file in path.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    strategy = json.load(f)
                    self.active_strategies.append(strategy)
            except Exception as e:
                print(f"Error loading strategy {file}: {e}")

    def evaluate_strategy(self, strategy: Dict, df: pd.DataFrame):
        """Evaluate entry and exit conditions for a strategy"""
        if df.empty:
            return None

        # 1. Recalculate indicators
        df = self.calculate_indicators(strategy['symbol'], df, strategy.get('indicators', []))
        
        # 2. Check Conditions
        is_entry = self._check_condition_group(strategy.get('entry_conditions', {}), df)
        is_exit = self._check_condition_group(strategy.get('exit_conditions', {}), df)
        
        if is_entry or is_exit:
            # You can log here if needed, but removing for now
            pass
            
        return {
            "symbol": strategy['symbol'],
            "entry_signal": is_entry,
            "exit_signal": is_exit
        }

    def _check_condition_group(self, group: Dict, df: pd.DataFrame) -> bool:
        """Recursively check AND/OR condition groups"""
        if "and" in group:
            return all(self._check_condition_group(c, df) if isinstance(c, dict) and ("and" in c or "or" in c) 
                       else self._evaluate_single_condition(c, df) for c in group["and"])
        if "or" in group:
            return any(self._check_condition_group(c, df) if isinstance(c, dict) and ("and" in c or "or" in c) 
                       else self._evaluate_single_condition(c, df) for c in group["or"])
        
        # Single condition fallback
        return self._evaluate_single_condition(group, df)

    def _evaluate_single_condition(self, cond: Dict, df: pd.DataFrame) -> bool:
        """Evaluate a single comparison (e.g., fast_ema > slow_ema)"""
        if not cond: return False
        
        op = cond['operator']
        left_key = cond['left']
        right_key = cond['right']
        
        # Get latest values (last row)
        curr = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else curr
        
        left_val = curr[left_key] if left_key in curr else left_key
        right_val = curr[right_key] if right_key in curr else right_key
        
        res = False
        if op == ">": res = left_val > right_val
        elif op == "<": res = left_val < right_val
        elif op == "==": res = left_val == right_val
        elif op == "cross_over":
            prev_left = prev[left_key] if left_key in prev else left_key
            prev_right = prev[right_key] if right_key in prev else right_key
            res = prev_left <= prev_right and left_val > right_val
        elif op == "cross_under":
            prev_left = prev[left_key] if left_key in prev else left_key
            prev_right = prev[right_key] if right_key in prev else right_key
            res = prev_left >= prev_right and left_val < right_val
            
        return res

    def calculate_indicators(self, symbol: str, df: pd.DataFrame, indicators: List[Dict]):
        """Calculate technical indicators using local pandas implementations"""
        if df.empty: return df
        
        # Ensure we are not working on a view/slice to avoid SettingWithCopyWarning
        df = df.copy()
        
        for ind in indicators:
            ind_type = ind['type'].lower()
            params = ind.get('params', {})
            period = params.get('period', 14)
            
            if ind_type == "ema":
                df[ind['id']] = df['close'].ewm(span=period, adjust=False).mean()
            elif ind_type == "sma":
                df[ind['id']] = df['close'].rolling(window=period).mean()
            elif ind_type == "rsi":
                delta = df['close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
                rs = gain / loss
                df[ind['id']] = 100 - (100 / (1 + rs))
        return df

    def on_tick(self, tick_data: Dict[str, Any]):
        """Process incoming tick data, evaluate strategies, and manage risk"""
        symbol = tick_data.get('symbol')
        current_price = tick_data.get('last_price', 0)
        
        # 1. Update risk management for existing trades
        order_manager.check_risk_management(symbol, current_price)
        
        # 2. Update price history (OHLCV) - Simple version for Phase 2/3
        if symbol not in self.data_frames:
            # Initialize with dummy startup data if needed, or start fresh
            self.data_frames[symbol] = pd.DataFrame(columns=["close"])
        
        # Append latest price
        new_row = pd.DataFrame({"close": [current_price]})
        self.data_frames[symbol] = pd.concat([self.data_frames[symbol], new_row], ignore_index=True).tail(100)
        
        # 3. Evaluate strategies for this symbol
        for strategy in self.active_strategies:
            if strategy['symbol'] == symbol:
                result = self.evaluate_strategy(strategy, self.data_frames[symbol])
                if result:
                    # Pass signal to Order Manager
                    order_manager.execute_signal(symbol, result, current_price, strategy)

strategy_manager = StrategyManager()
