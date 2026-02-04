import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.strategy_manager import strategy_manager
from app.core.order_manager import order_manager
import pandas as pd

def test_order_flow():
    print("[TEST] Starting Full Pipeline Test (Signal -> Order -> Risk)")
    
    # Enable Paper Trading for safety
    order_manager.paper_trading = True
    
    # 1. Load Strategy
    strategy_manager.load_strategies()
    strat = strategy_manager.active_strategies[0]
    symbol = strat['symbol']
    print(f"Strategy: {strat['name']} for {symbol}")

    # 2. Simulate Entry Signal
    print("\nSimulating Bullish Signal...")
    # Flat base where EMA_fast == EMA_slow
    df_entry = pd.DataFrame({"close": [100.0] * 40})
    
    # Inject data history
    strategy_manager.data_frames[symbol] = df_entry
    
    # Trigger on_tick manually with a jump to 120
    # This ensures prev_ema_fast (100) <= prev_ema_slow (100)
    # and curr_ema_fast (104) > curr_ema_slow (101.8)
    tick = {"symbol": symbol, "last_price": 120}
    strategy_manager.on_tick(tick)
    
    # Verify trade is active
    if symbol in order_manager.active_trades:
        print(f"SUCCESS: Trade entered for {symbol} at {order_manager.active_trades[symbol]['entry_price']}")
    else:
        print("FAIL: Trade not entered")
        return

    # 3. Simulate Stop Loss Hit
    print("\nSimulating price drop to hit Stop Loss...")
    sl_price = order_manager.active_trades[symbol]['sl_price']
    print(f"Targeting SL: {sl_price}")
    
    # Trigger tick at SL price
    tick_sl = {"symbol": symbol, "last_price": sl_price - 1} # Slightly below SL
    strategy_manager.on_tick(tick_sl)
    
    # Verify trade is closed
    if symbol not in order_manager.active_trades:
        print(f"SUCCESS: Trade stopped out. Last PnL: {order_manager.history[-1]['pnl']:.2f}")
    else:
        print("FAIL: Trade still active after SL hit")

if __name__ == "__main__":
    test_order_flow()
