import pandas as pd
import numpy as np
from typing import Optional
from datetime import datetime, timedelta

# --- Copied from trading-expert SKILL.md ---

class TradingStrategy:
    def __init__(self, symbol: str, capital: float = 100000):
        self.symbol = symbol
        self.capital = capital
        self.position = 0
        self.cash = capital
        self.trades = []

    def moving_average_crossover(self, data: pd.DataFrame,
                                  short_window: int = 50,
                                  long_window: int = 200) -> pd.Series:
        """Simple Moving Average Crossover Strategy"""
        data = data.copy()
        data['SMA_short'] = data['close'].rolling(window=short_window).mean()
        data['SMA_long'] = data['close'].rolling(window=long_window).mean()

        # Generate signals
        data['signal'] = 0
        data.loc[data['SMA_short'] > data['SMA_long'], 'signal'] = 1
        data.loc[data['SMA_short'] < data['SMA_long'], 'signal'] = -1

        return data['signal']

class Backtester:
    def __init__(self, initial_capital: float = 100000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0
        self.trades = []

    def run(self, data: pd.DataFrame, signals: pd.Series) -> dict:
        """Run backtest on historical data"""
        portfolio_value = []
        
        # Ensure signals are aligned with data
        signals = signals.reindex(data.index).fillna(0)

        for i in range(len(data)):
            current_signal = signals.iloc[i]
            current_price = data['close'].iloc[i]
            current_date = data.index[i]
            
            if current_signal == 1 and self.position == 0:  # Buy signal
                shares = self.capital // current_price
                cost = shares * current_price
                self.capital -= cost
                self.position = shares
                self.trades.append({
                    'type': 'BUY',
                    'price': current_price,
                    'shares': shares,
                    'date': current_date
                })

            elif current_signal == -1 and self.position > 0:  # Sell signal
                proceeds = self.position * current_price
                self.capital += proceeds
                self.trades.append({
                    'type': 'SELL',
                    'price': current_price,
                    'shares': self.position,
                    'date': current_date
                })
                self.position = 0

            # Calculate portfolio value
            current_value = self.capital + (self.position * current_price)
            portfolio_value.append(current_value)

        return self.calculate_metrics(portfolio_value, data)

    def calculate_metrics(self, portfolio_value: list, data: pd.DataFrame) -> dict:
        """Calculate performance metrics"""
        returns = pd.Series(portfolio_value).pct_change()

        total_return = (portfolio_value[-1] - self.initial_capital) / self.initial_capital
        # Avoid division by zero if std is 0
        std_dev = returns.std()
        sharpe_ratio = 0 if std_dev == 0 else returns.mean() / std_dev * np.sqrt(252)
        max_drawdown = self.calculate_max_drawdown(portfolio_value)

        return {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'total_trades': len(self.trades),
            'final_value': portfolio_value[-1]
        }

    def calculate_max_drawdown(self, portfolio_value: list) -> float:
        """Calculate maximum drawdown"""
        if not portfolio_value:
            return 0.0
            
        peak = portfolio_value[0]
        max_dd = 0

        for value in portfolio_value:
            if value > peak:
                peak = value
            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd

        return max_dd

# --- Demo Execution ---

def generate_dummy_data(days=500):
    """Generate some random walk OHLCV data for testing"""
    date_rng = pd.date_range(start='1/1/2022', periods=days, freq='B')
    
    # Generate random close prices (random walk)
    returns = np.random.normal(0.0005, 0.012, days) # slight positive drift
    close = 100 * np.cumprod(1 + returns)
    
    # Generate High, Low, Open based on Close
    high = close * (1 + np.abs(np.random.normal(0, 0.005, days)))
    low = close * (1 - np.abs(np.random.normal(0, 0.005, days)))
    open_p = close * (1 + np.random.normal(0, 0.002, days)) # Open near close
    
    # Fix High/Low to encompass Open/Close
    high = np.maximum(high, np.maximum(open_p, close))
    low = np.minimum(low, np.minimum(open_p, close))
    
    # Volume
    volume = np.random.randint(1000, 10000, days)
    
    df = pd.DataFrame({
        'date': date_rng,
        'Open': open_p,
        'High': high,
        'Low': low,
        'Close': close,
        'Volume': volume
    })
    
    # Standardize column names for mplfinance and strategies
    df.rename(columns={'Close': 'close', 'Volume': 'volume'}, inplace=True)
    # mplfinance expects capitalized Open, High, Low, Close, Volume usually, 
    # but we need lowercase 'close' for the Strategy class we copied.
    # Let's keep lowercase for strategy and create capitalized for mpf plotting later or adapt.
    
    # Actually, TradingStrategy uses 'close', mplfinance expects 'Close'. 
    # Let's align on Capitalized for DataFrame and support 'close' via copy or alias?
    # Or just rename required columns for Strategy.
    
    # Better approach: 
    # TradingStrategy expects 'close'. 
    # mplfinance expects 'Open', 'High', 'Low', 'Close'.
    # We will provide 'Open', 'High', 'Low', 'Close' in the DF.
    # And we will also provide 'close' as a column (duplicate of 'Close') or update Strategy to use 'Close'.
    # Since Strategy is copied code, let's keep it as is ('close') and add 'Open', 'High', 'Low', 'Close' to DF.
    
    df = pd.DataFrame({
        'date': date_rng,
        'Open': open_p,
        'High': high,
        'Low': low,
        'Close': close,
        'Volume': volume
    })
    
    # Add lowercase columns for the Strategy class compatibility
    df['close'] = df['Close']
    
    df.set_index('date', inplace=True)
    return df

def main():
    print("Generating dummy market data...")
    data = generate_dummy_data(days=500)
    print(f"Generated {len(data)} days of data.")
    print(f"Start Price: ${data['close'].iloc[0]:.2f}")
    print(f"End Price:   ${data['close'].iloc[-1]:.2f}")
    print("-" * 30)

    # Initialize Strategy and Backtester
    initial_cash = 10000.0
    strategy = TradingStrategy(symbol="TEST", capital=initial_cash)
    backtester = Backtester(initial_capital=initial_cash)

    print("Running Moving Average Crossover Strategy (Short=20, Long=50)...")
    # Using shorter windows for the demo to ensure we get some crosses in 500 days
    signals = strategy.moving_average_crossover(data, short_window=20, long_window=50)

    # Run Backtest
    results = backtester.run(data, signals)

    print("-" * 30)
    print("BACKTEST RESULTS:")
    print(f"Final Portfolio V.: ${results['final_value']:.2f}")
    print(f"Total Return:       {results['total_return']*100:.2f}%")
    print(f"Total Trades:       {results['total_trades']}")
    print(f"Sharpe Ratio:       {results['sharpe_ratio']:.2f}")
    print(f"Max Drawdown:       {results['max_drawdown']*100:.2f}%")
    
    if results['total_trades'] > 0:
        print("\nLast 3 Trades:")
        for trade in backtester.trades[-3:]:
            print(f"  {trade['date'].strftime('%Y-%m-%d')} | {trade['type']} {trade['shares']} @ ${trade['price']:.2f}")

    # Plot results
    print("\nPlotting results...")
    plot_backtest(data, backtester.trades)

def plot_backtest(data: pd.DataFrame, trades: list):
    """Plot candlestick chart with buy/sell markers"""
    try:
        import mplfinance as mpf
    except ImportError:
        print("Error: mplfinance not found. Please install it: pip install mplfinance")
        return

    # Create marker series
    buy_signals = [np.nan] * len(data)
    sell_signals = [np.nan] * len(data)

    for trade in trades:
        date_idx = trade['date']
        if date_idx in data.index:
            if trade['type'] == 'BUY':
                buy_signals[data.index.get_loc(date_idx)] = trade['price'] * 0.99  # Below candle
            elif trade['type'] == 'SELL':
                sell_signals[data.index.get_loc(date_idx)] = trade['price'] * 1.01 # Above candle

    # Create addplots
    apds = []
    
    # Check if we have any buys/sells to plot to avoid errors
    if not all(np.isnan(x) for x in buy_signals):
        apds.append(mpf.make_addplot(buy_signals, type='scatter', markersize=100, marker='^', color='g', label='Buy'))
    
    if not all(np.isnan(x) for x in sell_signals):
        apds.append(mpf.make_addplot(sell_signals, type='scatter', markersize=100, marker='v', color='r', label='Sell'))

    # Add SMA text
    # (Optional: Plot SMAs if we returned the updated dataframe with SMAs, 
    # but for now we'll just plot price and trades)
    
    # Plot
    mpf.plot(data, 
             type='candle', 
             style='charles', 
             title='Backtest Results (SMA Crossover)',
             ylabel='Price ($)',
             volume=False,
             addplot=apds if apds else None,
             figsize=(12, 8))

if __name__ == "__main__":
    main()
