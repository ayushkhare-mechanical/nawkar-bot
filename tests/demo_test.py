import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.strategy_manager import strategy_manager
import pandas as pd
import time

def run_demo():
    print("🚀 Starting Strategy Engine Demo...")
    
    # 1. Load active strategies from app/strategies/
    strategy_manager.load_strategies()
    if not strategy_manager.active_strategies:
        print("❌ No strategies found in app/strategies/!")
        return

    strat = strategy_manager.active_strategies[0]
    print(f"✅ Loaded: {strat['name']} ({strat['symbol']})")

    # 2. Simulate a Price Trend (Bullish Crossover)
    print("\n📈 Simulating Bullish Trend (EMA Fast crossing above Slow)...")
    # Data where EMA(9) will eventually cross over EMA(21)
    bullish_prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 112, 115, 120]
    df_bullish = pd.DataFrame({"close": bullish_prices})
    
    result = strategy_manager.evaluate_strategy(strat, df_bullish)
    print(f"Result: {result}")
    if result.get('entry_signal'):
        print("🔥 ENTRY SIGNAL DETECTED!")

    # 3. Simulate a Price Drop (Bearish Crossover)
    print("\n📉 Simulating Bearish Drop (EMA Fast crossing below Slow)...")
    bearish_prices = [120, 118, 115, 112, 110, 108, 105, 102, 100, 98, 95, 90]
    df_bearish = pd.DataFrame({"close": bearish_prices})
    
    result_bearish = strategy_manager.evaluate_strategy(strat, df_bearish)
    print(f"Result: {result_bearish}")
    if result_bearish.get('exit_signal'):
        print("🛑 EXIT SIGNAL DETECTED!")

if __name__ == "__main__":
    run_demo()
