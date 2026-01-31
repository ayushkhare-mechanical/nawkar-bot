# 1Min Strategy - Step-by-Step Execution Guide

## 🚀 Quick Start Workflow

This guide provides **exact prompts** to copy-paste into Claude for implementing the 1Min Strategy.

---

## PHASE 1: AUTHENTICATION & SETUP

### Step 1.1: Login to FYERS

**Copy this prompt:**
```
Login to FYERS and authenticate my account.
```

**Expected Result:**
- You'll get a URL to authenticate
- Click the URL and login to FYERS
- Authorization will be saved automatically

**Verification prompt:**
```
Check if I'm logged in. Show my account details and available funds.
```

---

## PHASE 2: DAILY MORNING SCAN (Run at 9:00 AM)

### Step 2.1: Scan Nifty 100 Stocks

**Copy this prompt:**
```
Run the 1Min Strategy daily scan:

1. Fetch yesterday's (2025-01-30) daily candle data for these Nifty 100 stocks:
   NSE:RELIANCE-EQ, NSE:TCS-EQ, NSE:HDFCBANK-EQ, NSE:INFY-EQ, NSE:ICICIBANK-EQ,
   NSE:HINDUNILVR-EQ, NSE:SBIN-EQ, NSE:BHARTIARTL-EQ, NSE:ITC-EQ, NSE:KOTAKBANK-EQ,
   NSE:LT-EQ, NSE:AXISBANK-EQ, NSE:HCLTECH-EQ, NSE:WIPRO-EQ, NSE:ASIANPAINT-EQ,
   NSE:MARUTI-EQ, NSE:TITAN-EQ, NSE:ULTRACEMCO-EQ, NSE:BAJFINANCE-EQ, NSE:NESTLEIND-EQ

2. For each stock, analyze the daily candle:
   - Calculate body percentage: (|close - open| / close) * 100
   - Calculate body ratio: body / (high - low)
   
3. Filter stocks that meet criteria:
   BUY ELIGIBLE: Green candle (close > open), body >= 0.8%, body ratio >= 75%
   SELL ELIGIBLE: Red candle (close < open), body >= 0.8%, body ratio >= 75%

4. Display results in a table with columns:
   Symbol | Type | Body % | Body Ratio | Close Price

5. Save the eligible stocks list for intraday monitoring.
```

**Alternative - If you want to do it manually for one stock first:**
```
Fetch yesterday's daily candle for NSE:RELIANCE-EQ:

Use get_chart_data:
- symbol: NSE:RELIANCE-EQ
- resolution: 1D
- rangeFrom: 2025-01-30
- rangeTo: 2025-01-31
- dateFormat: 1

Then analyze if it's eligible:
- If green candle (close > open) with body >= 0.8% and body ratio >= 75%: BUY ELIGIBLE
- If red candle (close < open) with body >= 0.8% and body ratio >= 75%: SELL ELIGIBLE
```

---

## PHASE 3: INTRADAY MONITORING (9:15 AM - 3:30 PM)

### Step 3.1: Monitor BUY Eligible Stocks

**Copy this prompt (replace SYMBOL with actual stock):**
```
Monitor NSE:RELIANCE-EQ for BUY entry (stock showed strong green candle yesterday):

1. Fetch 1-minute candles starting from 9:15 AM today
2. Watch for a RED candle to form (close < open)
3. When red candle appears:
   - Entry Price = Red candle HIGH
   - Stop Loss = Red candle LOW
   - Target = Entry + (2 × candle height)
   - Calculate quantity for ₹50,000 capital

4. Display the trade setup with:
   - Entry, SL, Target levels
   - Risk-reward ratio
   - Recommended quantity
   - Total capital required

5. Create price alerts:
   - Alert when price breaks above red candle high (entry trigger)
   - Alert when price hits stop loss
   - Alert when price hits target
```

### Step 3.2: Monitor SELL Eligible Stocks

**Copy this prompt (replace SYMBOL with actual stock):**
```
Monitor NSE:WIPRO-EQ for SELL entry (stock showed strong red candle yesterday):

1. Fetch 1-minute candles starting from 9:15 AM today
2. Watch for a GREEN candle to form (close > open)
3. When green candle appears:
   - Entry Price = Green candle LOW
   - Stop Loss = Green candle HIGH
   - Target = Entry - (2 × candle height)
   - Calculate quantity for ₹50,000 capital

4. Display the trade setup
5. Create price alerts for entry, SL, and target
```

### Step 3.3: Get Current 1-Min Candles

**Copy this prompt:**
```
Get the last 5 1-minute candles for NSE:RELIANCE-EQ:

Use get_chart_data:
- symbol: NSE:RELIANCE-EQ
- resolution: 1
- rangeFrom: 2025-01-31
- rangeTo: 2025-01-31
- dateFormat: 1

Show OHLC data and identify if any is a trigger candle (red for BUY setup, green for SELL setup).
```

---

## PHASE 4: TRADE EXECUTION

### Step 4.1: Execute Trade (Manual)

**Copy this prompt:**
```
I want to execute this trade:

Symbol: NSE:RELIANCE-EQ
Side: BUY
Entry: 2850.50
Stop Loss: 2840.00
Target: 2871.00
Quantity: 17

Please:
1. Open the trading page for this stock
2. Provide me the direct link to place the order
3. Create price alerts for SL and Target
```

**Expected Response:**
- Link to: https://fyers.in/web/symbol/RELIANCE
- Price alerts created

### Step 4.2: Monitor Active Position

**Copy this prompt:**
```
Check my current position for NSE:RELIANCE-EQ:

1. Show current price (LTP)
2. Show my entry price and quantity
3. Calculate current P&L
4. Check if price has hit SL or Target
5. Show distance to SL and Target
```

---

## PHASE 5: RISK MANAGEMENT

### Step 5.1: Check Portfolio Status

**Copy this prompt:**
```
Show my portfolio status:

1. List all open positions
2. Calculate total P&L for today
3. Count number of active trades
4. Show available margin
5. Check if I'm approaching max positions limit (5 trades)
6. Alert if daily loss is approaching ₹5,000 limit
```

### Step 5.2: Exit Trade at SL or Target

**Copy this prompt:**
```
Exit my position in NSE:RELIANCE-EQ:

Reason: [Stop Loss Hit / Target Reached / Manual Exit]

Please:
1. Show me the exit link
2. Calculate final P&L
3. Update trade log
4. Remove price alerts for this trade
```

---

## PHASE 6: END OF DAY ACTIVITIES

### Step 6.1: Generate Daily Report

**Copy this prompt:**
```
Generate end-of-day report for 1Min Strategy:

1. Summary of today's scan:
   - Total stocks scanned
   - BUY eligible count
   - SELL eligible count

2. Trading activity:
   - Total trades taken
   - Trades closed
   - Trades still active

3. Performance:
   - Winning trades count
   - Losing trades count
   - Win rate percentage
   - Total P&L for the day
   - Best trade
   - Worst trade

4. Save report as formatted text file.
```

### Step 6.2: Close All Positions (Optional)

**Copy this prompt:**
```
Close all my open positions at market price:

1. List all open positions
2. For each position, provide exit link
3. Calculate P&L for each
4. Calculate total P&L
5. Update trade log with all exits
```

---

## AUTOMATED WORKFLOW (Advanced)

### Full Automation Prompt

**Copy this prompt for complete automation:**
```
Automate the 1Min Strategy for today:

MORNING (9:00 AM):
1. Scan all Nifty 100 stocks for yesterday's daily candle
2. Filter eligible stocks (BUY: green body >= 0.8%, SELL: red body >= 0.8%)
3. Save eligible list

INTRADAY (9:15 AM - 3:30 PM):
4. Monitor eligible stocks every minute
5. For BUY eligible: Watch for red candle, calculate entry/SL/target
6. For SELL eligible: Watch for green candle, calculate entry/SL/target
7. Create price alerts for each setup
8. Alert me when trigger conditions are met

TRADE MANAGEMENT:
9. When entry is triggered, provide trading link
10. Monitor active positions for SL/Target
11. Alert when positions need to be closed
12. Maximum 5 concurrent positions
13. Stop trading if daily loss exceeds ₹5,000

END OF DAY (3:30 PM):
14. Generate comprehensive report
15. Calculate total P&L
16. Save trade log

Start monitoring now and alert me at each important event.
```

---

## TROUBLESHOOTING

### If Authentication Expires

**Prompt:**
```
Re-authenticate with FYERS. My session might have expired.
```

### If No Eligible Stocks Found

**Prompt:**
```
The daily scan found no eligible stocks. Please:
1. Verify the scan criteria (body >= 0.8%, ratio >= 75%)
2. Check if market was volatile yesterday
3. Show me the top 10 stocks by body percentage even if they don't meet criteria
```

### If Trade Setup Seems Wrong

**Prompt:**
```
Verify this trade setup for NSE:RELIANCE-EQ:

Trigger candle: Open 2845, High 2851, Low 2843, Close 2844
My calculation: Entry 2851, SL 2843, Target 2867

Is this correct for a BUY setup? Please recalculate.
```

---

## TESTING MODE

### Paper Trading Test

**Copy this prompt:**
```
Run a paper trading simulation of 1Min Strategy:

1. Use historical data from last week (Jan 20-24, 2025)
2. Simulate the daily scan and trade setups
3. Calculate hypothetical entries, exits, and P&L
4. Don't place any real orders
5. Generate performance report

This will help me validate the strategy before live trading.
```

---

## QUICK REFERENCE

### Daily Checklist

- [ ] 9:00 AM: Run daily scan
- [ ] 9:15 AM: Start monitoring eligible stocks
- [ ] Monitor: Watch for trigger candles
- [ ] Entry: Create price alerts
- [ ] Active: Monitor SL/Target
- [ ] Exit: Close positions
- [ ] 3:30 PM: Generate daily report

### Key Rules

✅ Body percentage must be >= 0.8%
✅ Body ratio must be >= 75%
✅ BUY: Wait for red candle after green daily
✅ SELL: Wait for green candle after red daily
✅ Risk-Reward: Always 1:2 ratio
✅ Max positions: 5 concurrent trades
✅ Max loss: ₹5,000 per day
✅ Capital per trade: ₹50,000

---

## SAMPLE EXECUTION LOG

```
09:00 - Started daily scan
09:05 - Found 3 BUY eligible, 2 SELL eligible
09:15 - Monitoring started
09:23 - Red candle on RELIANCE (BUY setup)
09:24 - Created alerts for RELIANCE
09:28 - Price triggered entry at 2851
09:45 - Target hit on RELIANCE (+₹340)
...
15:30 - Day ended, Total P&L: +₹1,250
```

---

**Remember:**
- Always verify calculations before placing real trades
- Start with paper trading to test the strategy
- Monitor your risk limits closely
- Keep a trade journal for continuous improvement

**Disclaimer:**
FYERS Intelligent Assistant (FIA) offers AI-generated stock insights for informational use only and not financial advice. Always do your own research or consult a licensed advisor.
