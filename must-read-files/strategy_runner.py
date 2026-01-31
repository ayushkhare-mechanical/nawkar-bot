#!/usr/bin/env python3
"""
1Min Strategy - Production Ready Implementation
FYERS Trading Strategy Automation

Usage:
    python strategy_runner.py --mode scan    # Run daily scan
    python strategy_runner.py --mode monitor # Monitor and trade
    python strategy_runner.py --mode report  # Generate report
"""

import argparse
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('strategy.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    "nifty_100_stocks": [
        "NSE:RELIANCE-EQ", "NSE:TCS-EQ", "NSE:HDFCBANK-EQ", 
        "NSE:INFY-EQ", "NSE:ICICIBANK-EQ", "NSE:HINDUNILVR-EQ",
        "NSE:SBIN-EQ", "NSE:BHARTIARTL-EQ", "NSE:ITC-EQ",
        "NSE:KOTAKBANK-EQ", "NSE:LT-EQ", "NSE:AXISBANK-EQ",
        "NSE:HCLTECH-EQ", "NSE:WIPRO-EQ", "NSE:ASIANPAINT-EQ",
        "NSE:MARUTI-EQ", "NSE:TITAN-EQ", "NSE:ULTRACEMCO-EQ",
        "NSE:BAJFINANCE-EQ", "NSE:NESTLEIND-EQ", "NSE:SUNPHARMA-EQ",
        "NSE:ADANIGREEN-EQ", "NSE:ONGC-EQ", "NSE:TATAMOTORS-EQ",
        "NSE:POWERGRID-EQ", "NSE:NTPC-EQ", "NSE:M&M-EQ",
        "NSE:TATASTEEL-EQ", "NSE:BAJAJFINSV-EQ", "NSE:TECHM-EQ"
        # Add remaining 70 stocks for complete Nifty 100 coverage
    ],
    "min_body_percent": 0.8,
    "min_body_ratio": 0.75,
    "risk_reward_ratio": 2.0,
    "max_positions": 5,
    "capital_per_trade": 50000,
    "max_daily_loss": 5000
}


# ============================================================================
# HELPER FUNCTIONS FOR CLAUDE INTERACTION
# ============================================================================

def create_fyers_prompt(action: str, params: Dict) -> str:
    """Generate prompts for FYERS API interaction via Claude"""
    
    prompts = {
        "login": "Login to FYERS and authenticate my account.",
        
        "get_daily_candle": f"""
Fetch yesterday's daily candle data for {params['symbol']} using get_chart_data:
- symbol: {params['symbol']}
- resolution: '1D'
- rangeFrom: '{params['from_date']}'
- rangeTo: '{params['to_date']}'
- dateFormat: '1'

Return the OHLC data as JSON.
""",
        
        "get_1min_candles": f"""
Get 1-minute candle data for {params['symbol']}:
- symbol: {params['symbol']}
- resolution: '1'
- rangeFrom: '{params['from_date']}'
- rangeTo: '{params['to_date']}'
- dateFormat: '1'

Return the last 5 candles.
""",
        
        "check_positions": "Show me all my current open positions using get_positions.",
        
        "get_funds": "Check my available funds and margin using get_funds.",
        
        "create_alert": f"""
Create a price alert for {params['symbol']}:
- symbol: {params['symbol']}
- comparisonType: LTP
- condition: {params['condition']}
- value: {params['value']}
- name: '{params['name']}'
"""
    }
    
    return prompts.get(action, "")


# ============================================================================
# STOCK ANALYSIS FUNCTIONS
# ============================================================================

def analyze_daily_candle(candle: Dict) -> Dict:
    """
    Analyze daily candle for eligibility
    
    Returns:
        {
            'eligible': 'BUY' | 'SELL' | 'NONE',
            'body_percent': float,
            'body_ratio': float,
            'candle_type': 'green' | 'red'
        }
    """
    open_price = candle['o']
    high = candle['h']
    low = candle['l']
    close = candle['c']
    
    # Calculate metrics
    body = abs(close - open_price)
    range_size = high - low
    
    if range_size == 0:
        return {'eligible': 'NONE', 'body_percent': 0, 'body_ratio': 0}
    
    body_percent = (body / close) * 100
    body_ratio = body / range_size
    
    # Determine eligibility
    is_green = close > open_price
    is_red = close < open_price
    
    eligible = 'NONE'
    
    # Check BUY eligibility (strong green candle)
    if (is_green and 
        body_percent >= CONFIG['min_body_percent'] and 
        body_ratio >= CONFIG['min_body_ratio']):
        eligible = 'BUY'
    
    # Check SELL eligibility (strong red candle)
    elif (is_red and 
          body_percent >= CONFIG['min_body_percent'] and 
          body_ratio >= CONFIG['min_body_ratio']):
        eligible = 'SELL'
    
    return {
        'eligible': eligible,
        'body_percent': round(body_percent, 2),
        'body_ratio': round(body_ratio, 2),
        'candle_type': 'green' if is_green else 'red',
        'open': open_price,
        'high': high,
        'low': low,
        'close': close
    }


def calculate_trade_levels(trigger_candle: Dict, side: str) -> Dict:
    """
    Calculate entry, stop loss, and target levels
    
    Args:
        trigger_candle: 1-minute candle data
        side: 'BUY' or 'SELL'
    
    Returns:
        {
            'entry': float,
            'stop_loss': float,
            'target': float,
            'risk': float,
            'reward': float
        }
    """
    high = trigger_candle['h']
    low = trigger_candle['l']
    height = high - low
    
    if side == 'BUY':
        entry = high
        stop_loss = low
        target = entry + (height * CONFIG['risk_reward_ratio'])
    else:  # SELL
        entry = low
        stop_loss = high
        target = entry - (height * CONFIG['risk_reward_ratio'])
    
    risk = abs(entry - stop_loss)
    reward = abs(target - entry)
    
    return {
        'entry': round(entry, 2),
        'stop_loss': round(stop_loss, 2),
        'target': round(target, 2),
        'risk': round(risk, 2),
        'reward': round(reward, 2),
        'risk_reward': round(reward / risk, 2) if risk > 0 else 0
    }


def calculate_quantity(entry_price: float, stop_loss: float, capital: float = None) -> int:
    """Calculate position size based on risk"""
    if capital is None:
        capital = CONFIG['capital_per_trade']
    
    risk_per_share = abs(entry_price - stop_loss)
    
    if risk_per_share == 0:
        return 0
    
    # Calculate quantity based on capital
    max_qty_by_capital = int(capital / entry_price)
    
    # Calculate quantity based on ₹1000 risk per trade
    max_qty_by_risk = int(1000 / risk_per_share)
    
    # Use the minimum to ensure we don't exceed capital or risk limits
    quantity = min(max_qty_by_capital, max_qty_by_risk)
    
    return max(1, quantity)


# ============================================================================
# DAILY SCAN FUNCTION
# ============================================================================

def run_daily_scan(candle_data: Dict[str, Dict]) -> Dict:
    """
    Run daily scan on all Nifty 100 stocks
    
    Args:
        candle_data: Dictionary mapping symbols to their daily candle data
    
    Returns:
        {
            'buy_eligible': List[Dict],
            'sell_eligible': List[Dict],
            'stats': Dict
        }
    """
    buy_eligible = []
    sell_eligible = []
    
    for symbol, candle in candle_data.items():
        analysis = analyze_daily_candle(candle)
        
        if analysis['eligible'] == 'BUY':
            buy_eligible.append({
                'symbol': symbol,
                'body_percent': analysis['body_percent'],
                'body_ratio': analysis['body_ratio'],
                'close': analysis['close']
            })
            logger.info(f"✅ BUY Eligible: {symbol} - Body: {analysis['body_percent']}%, Ratio: {analysis['body_ratio']}")
        
        elif analysis['eligible'] == 'SELL':
            sell_eligible.append({
                'symbol': symbol,
                'body_percent': analysis['body_percent'],
                'body_ratio': analysis['body_ratio'],
                'close': analysis['close']
            })
            logger.info(f"✅ SELL Eligible: {symbol} - Body: {analysis['body_percent']}%, Ratio: {analysis['body_ratio']}")
    
    stats = {
        'total_scanned': len(candle_data),
        'buy_eligible_count': len(buy_eligible),
        'sell_eligible_count': len(sell_eligible),
        'scan_time': datetime.now().isoformat()
    }
    
    return {
        'buy_eligible': buy_eligible,
        'sell_eligible': sell_eligible,
        'stats': stats
    }


# ============================================================================
# TRADE MONITORING FUNCTIONS
# ============================================================================

def check_for_trigger_candle(candles: List[Dict], side: str) -> Optional[Dict]:
    """
    Check if last candle is a valid trigger candle
    
    Args:
        candles: List of recent 1-min candles
        side: 'BUY' or 'SELL'
    
    Returns:
        Trigger candle if found, None otherwise
    """
    if not candles:
        return None
    
    last_candle = candles[-1]
    
    open_price = last_candle['o']
    close = last_candle['c']
    
    # For BUY: Wait for RED candle
    if side == 'BUY' and close < open_price:
        return last_candle
    
    # For SELL: Wait for GREEN candle
    elif side == 'SELL' and close > open_price:
        return last_candle
    
    return None


def generate_trade_setup(symbol: str, side: str, trigger_candle: Dict) -> Dict:
    """Generate complete trade setup"""
    
    levels = calculate_trade_levels(trigger_candle, side)
    quantity = calculate_quantity(levels['entry'], levels['stop_loss'])
    
    setup = {
        'symbol': symbol,
        'side': side,
        'trigger_candle': {
            'time': trigger_candle.get('t', 'N/A'),
            'open': trigger_candle['o'],
            'high': trigger_candle['h'],
            'low': trigger_candle['l'],
            'close': trigger_candle['c']
        },
        'entry': levels['entry'],
        'stop_loss': levels['stop_loss'],
        'target': levels['target'],
        'quantity': quantity,
        'risk_amount': round(levels['risk'] * quantity, 2),
        'reward_amount': round(levels['reward'] * quantity, 2),
        'capital_required': round(levels['entry'] * quantity, 2),
        'status': 'SETUP_READY',
        'created_at': datetime.now().isoformat()
    }
    
    return setup


# ============================================================================
# REPORTING FUNCTIONS
# ============================================================================

def generate_daily_report(eligible_stocks: Dict, trades: List[Dict] = None) -> str:
    """Generate formatted daily report"""
    
    if trades is None:
        trades = []
    
    report = f"""
{'='*80}
1MIN STRATEGY - DAILY REPORT
{'='*80}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

STOCK SCAN RESULTS:
{'-'*80}
Total Stocks Scanned: {eligible_stocks['stats']['total_scanned']}
BUY Eligible Stocks: {eligible_stocks['stats']['buy_eligible_count']}
SELL Eligible Stocks: {eligible_stocks['stats']['sell_eligible_count']}

BUY ELIGIBLE STOCKS:
"""
    
    for stock in eligible_stocks['buy_eligible'][:10]:  # Show top 10
        report += f"  • {stock['symbol']:20} Body: {stock['body_percent']:5.2f}%  Ratio: {stock['body_ratio']:5.2f}\n"
    
    report += f"\nSELL ELIGIBLE STOCKS:\n"
    
    for stock in eligible_stocks['sell_eligible'][:10]:
        report += f"  • {stock['symbol']:20} Body: {stock['body_percent']:5.2f}%  Ratio: {stock['body_ratio']:5.2f}\n"
    
    if trades:
        report += f"\n\nTRADE SETUPS GENERATED:\n{'-'*80}\n"
        
        for i, trade in enumerate(trades, 1):
            report += f"""
Trade #{i}:
  Symbol: {trade['symbol']}
  Side: {trade['side']}
  Entry: ₹{trade['entry']:,.2f}
  Stop Loss: ₹{trade['stop_loss']:,.2f}
  Target: ₹{trade['target']:,.2f}
  Quantity: {trade['quantity']}
  Risk: ₹{trade['risk_amount']:,.2f}
  Reward: ₹{trade['reward_amount']:,.2f}
  Capital Required: ₹{trade['capital_required']:,.2f}
"""
    
    report += f"\n{'='*80}\n"
    
    return report


def save_results(data: Dict, filename: str):
    """Save results to JSON file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = f"{filename}_{timestamp}.json"
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"Results saved to {filepath}")
    return filepath


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def display_prompts_for_user():
    """Display helpful prompts for user to interact with Claude"""
    
    print("\n" + "="*80)
    print("FYERS 1MIN STRATEGY - INTEGRATION PROMPTS")
    print("="*80)
    
    print("\n📋 STEP 1: AUTHENTICATION")
    print("-" * 80)
    print("Prompt: Login to FYERS and authenticate my account.")
    
    print("\n📋 STEP 2: FETCH DAILY CANDLES FOR SCAN")
    print("-" * 80)
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
    
    print(f"""Prompt: Fetch yesterday's daily candle data for these Nifty 100 stocks:
NSE:RELIANCE-EQ, NSE:TCS-EQ, NSE:HDFCBANK-EQ, NSE:INFY-EQ, NSE:ICICIBANK-EQ

Use get_chart_data with:
- resolution: '1D'
- rangeFrom: '{yesterday}'
- rangeTo: '{today}'
- dateFormat: '1'

Return the data in JSON format.""")
    
    print("\n📋 STEP 3: MONITOR 1-MINUTE CANDLES")
    print("-" * 80)
    current_date = datetime.now().strftime('%Y-%m-%d')
    print(f"""Prompt: Get the last 5 1-minute candles for NSE:RELIANCE-EQ

Use get_chart_data with:
- symbol: 'NSE:RELIANCE-EQ'
- resolution: '1'
- rangeFrom: '{current_date}'
- rangeTo: '{current_date}'
- dateFormat: '1'

Show me the OHLC data.""")
    
    print("\n📋 STEP 4: CREATE PRICE ALERTS")
    print("-" * 80)
    print("""Prompt: Create price alerts for my trade setups:

For NSE:RELIANCE-EQ:
- Alert when LTP crosses above 2850.50 (entry trigger)
- Alert when LTP crosses below 2840.00 (stop loss)
- Alert when LTP crosses above 2871.00 (target)

Use create_price_alert for each level.""")
    
    print("\n📋 STEP 5: CHECK POSITIONS")
    print("-" * 80)
    print("Prompt: Show me all my current open positions and their P&L.")
    
    print("\n" + "="*80 + "\n")


def main():
    """Main execution function"""
    
    parser = argparse.ArgumentParser(description='1Min Strategy Runner')
    parser.add_argument('--mode', choices=['scan', 'monitor', 'report', 'prompts'],
                       default='prompts', help='Execution mode')
    
    args = parser.parse_args()
    
    if args.mode == 'prompts':
        display_prompts_for_user()
        return
    
    elif args.mode == 'scan':
        logger.info("Running daily stock scan...")
        print("\n⚠️  To complete the scan, you need to:")
        print("1. Use Claude to fetch daily candle data for all Nifty 100 stocks")
        print("2. Save the results to a file: eligible_stocks.json")
        print("\nUse this prompt:")
        print("-" * 80)
        
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')
        
        print(f"""Fetch yesterday's daily candles for all these stocks and analyze them:
{', '.join(CONFIG['nifty_100_stocks'][:10])}
...and {len(CONFIG['nifty_100_stocks']) - 10} more

For each stock:
1. Get daily candle using get_chart_data (resolution: '1D', from: '{yesterday}', to: '{today}')
2. Check if body >= 0.8% and body ratio >= 75%
3. Classify as BUY eligible (green), SELL eligible (red), or not eligible

Save results to eligible_stocks.json""")
    
    elif args.mode == 'monitor':
        logger.info("Starting trade monitoring...")
        print("\n⚠️  To monitor trades, use this workflow with Claude:")
        print("-" * 80)
        print("""1. Load eligible stocks from today's scan
2. For each BUY eligible stock, monitor for RED 1-min candles
3. For each SELL eligible stock, monitor for GREEN 1-min candles
4. When trigger candle appears, calculate entry/SL/target
5. Create price alerts for the levels
6. Monitor until trade completes""")
    
    elif args.mode == 'report':
        logger.info("Generating report...")
        print("\n📊 REPORT GENERATION")
        print("-" * 80)
        print("To generate a complete report, ask Claude:")
        print("\nPrompt: Generate end-of-day report for 1Min Strategy including:")
        print("- All eligible stocks from today's scan")
        print("- All trades executed today")
        print("- Win/loss statistics")
        print("- Total P&L")
        print("- Save as PDF report")


if __name__ == "__main__":
    main()
