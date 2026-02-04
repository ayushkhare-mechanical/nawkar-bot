import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from app.core.strategy_manager import StrategyManager
from app.core.database import SessionLocal, BacktestRun, BacktestTrade

class BacktestEngine:
    def __init__(self):
        self.strategy_evaluator = StrategyManager()

    def run_backtest(self, strategy_config: Dict, df: pd.DataFrame, overrides: Dict = None) -> Dict:
        """
        Run a backtest on provided historical data.
        overrides: Dict of indicator_id -> {param_name: value}
        """
        # 1. Apply overrides to strategy config
        backtest_config = self._apply_overrides(strategy_config, overrides)
        
        # 2. Calculate initial indicators
        df = self.strategy_evaluator.calculate_indicators(
            backtest_config['symbol'], 
            df.copy(), 
            backtest_config['indicators']
        )
        
        trades = []
        active_trade = None
        
        # 3. Step through candles (start from where indicators are ready)
        if len(df) < 20: 
            return {
                "summary": {"strategy_name": backtest_config['name'], "symbol": backtest_config['symbol'], "total_pnl": 0, "win_rate": 0, "total_trades": 0},
                "trades": [], "parameters": overrides or {}
            }
            
        start_idx = min(50, len(df) - 1)
        for i in range(start_idx, len(df)):
            curr_df = df.iloc[:i+1] # Visible data up to now
            current_candle = curr_df.iloc[-1]
            current_price = current_candle['close']
            
            # Risk Management Check (if trade is open)
            if active_trade:
                if current_price <= active_trade['sl_price']:
                    active_trade['exit_price'] = active_trade['sl_price']
                    active_trade['exit_time'] = str(current_candle.name) if hasattr(current_candle, 'name') else str(i)
                    active_trade['exit_reason'] = "Stop Loss"
                    active_trade['pnl'] = (active_trade['exit_price'] - active_trade['entry_price'])
                    trades.append(active_trade)
                    active_trade = None
                elif current_price >= active_trade['target_price']:
                    active_trade['exit_price'] = active_trade['target_price']
                    active_trade['exit_time'] = str(current_candle.name) if hasattr(current_candle, 'name') else str(i)
                    active_trade['exit_reason'] = "Target Hit"
                    active_trade['pnl'] = (active_trade['exit_price'] - active_trade['entry_price'])
                    trades.append(active_trade)
                    active_trade = None

            # Strategy Signal Check
            result = self.strategy_evaluator.evaluate_strategy(backtest_config, curr_df)
            
            if result['entry_signal'] and not active_trade:
                # Enter Trade
                risk = backtest_config.get('risk_management', {})
                sl_perc = risk.get('stop_loss_perc', 1.0)
                target_perc = risk.get('target_perc', 2.0)
                
                active_trade = {
                    "symbol": backtest_config['symbol'],
                    "entry_price": current_price,
                    "entry_time": str(current_candle.name) if hasattr(current_candle, 'name') else str(i),
                    "sl_price": current_price * (1 - sl_perc/100),
                    "target_price": current_price * (1 + target_perc/100),
                    "status": "CLOSED"
                }
            
            elif result['exit_signal'] and active_trade:
                # Exit Trade
                active_trade['exit_price'] = current_price
                active_trade['exit_time'] = str(current_candle.name) if hasattr(current_candle, 'name') else str(i)
                active_trade['exit_reason'] = "Strategy Signal"
                active_trade['pnl'] = (active_trade['exit_price'] - active_trade['entry_price'])
                trades.append(active_trade)
                active_trade = None

        # Summary Metrics
        total_pnl = sum(t['pnl'] for t in trades)
        winners = [t for t in trades if t['pnl'] > 0]
        win_rate = (len(winners) / len(trades) * 100) if trades else 0
        
        return {
            "summary": {
                "strategy_name": backtest_config['name'],
                "symbol": backtest_config['symbol'],
                "total_pnl": total_pnl,
                "win_rate": win_rate,
                "total_trades": len(trades)
            },
            "trades": trades,
            "parameters": overrides or {}
        }

    def _apply_overrides(self, config: Dict, overrides: Dict) -> Dict:
        if not overrides: return config
        
        new_config = config.copy()
        new_indicators = []
        
        for ind in new_config['indicators']:
            new_ind = ind.copy()
            if ind['id'] in overrides:
                new_ind['params'] = ind['params'].copy()
                new_ind['params'].update(overrides[ind['id']])
            new_indicators.append(new_ind)
            
        new_config['indicators'] = new_indicators
        return new_config

    def save_results(self, result: Dict) -> int:
        db = SessionLocal()
        try:
            run = BacktestRun(
                strategy_name=result['summary']['strategy_name'],
                symbol=result['summary']['symbol'],
                parameters=result['parameters'],
                total_pnl=result['summary']['total_pnl'],
                win_rate=result['summary']['win_rate'],
                total_trades=result['summary']['total_trades']
            )
            db.add(run)
            db.commit()
            db.refresh(run)
            
            for t in result['trades']:
                trade = BacktestTrade(
                    run_id=run.id,
                    symbol=t['symbol'],
                    entry_price=t['entry_price'],
                    exit_price=t['exit_price'],
                    entry_time=t['entry_time'],
                    exit_time=t['exit_time'],
                    pnl=t['pnl'],
                    exit_reason=t['exit_reason']
                )
                db.add(trade)
            db.commit()

            # --- Auto-Cleanup (Keep Last 100 Runs) ---
            max_runs = 100
            total_runs = db.query(BacktestRun).count()
            if total_runs > max_runs:
                # Get the IDs of the oldest runs to delete
                old_runs = db.query(BacktestRun).order_by(BacktestRun.timestamp.asc()).limit(total_runs - max_runs).all()
                for old_run in old_runs:
                    # Delete associated trades first
                    db.query(BacktestTrade).filter(BacktestTrade.run_id == old_run.id).delete()
                    db.delete(old_run)
                db.commit()

            return run.id
        finally:
            db.close()

backtest_engine = BacktestEngine()
