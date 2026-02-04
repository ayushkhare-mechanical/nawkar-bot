from fastapi import APIRouter, Request, Depends, HTTPException
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.fyers_handler import fyers_auth
from app.core.strategy_manager import strategy_manager
from app.core.order_manager import order_manager

router = APIRouter(prefix="/monitor", tags=["monitor"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/data")
async def get_monitor_data():
    token = fyers_auth.load_access_token()
    
    if not token:
        return {"authenticated": False, "message": "Authentication required"}
        
    user_profile = fyers_auth.get_user_profile(token)
    funds = fyers_auth.get_funds(token)
    holdings = fyers_auth.get_holdings(token)
    positions = fyers_auth.get_positions(token)
    orders = fyers_auth.get_orders(token)
    
    # Get last linked from token file
    last_linked = None
    import json
    import os
    if os.path.exists(fyers_auth.TOKEN_FILE):
        try:
            with open(fyers_auth.TOKEN_FILE, 'r') as f:
                token_data = json.load(f)
                last_linked = token_data.get('saved_at')
        except:
            pass

    return {
        "authenticated": True,
        "user_profile": user_profile,
        "funds": funds,
        "holdings": holdings,
        "positions": positions,
        "orders": orders,
        "last_linked": last_linked,
        "active_trades_count": len(order_manager.active_trades),
        "total_trades_count": len(order_manager.history)
    }

@router.get("/strategies")
async def get_strategies():
    return {
        "active_strategies": strategy_manager.active_strategies,
        "strategies_directory": strategy_manager.strategies_dir
    }

@router.post("/strategies/reload")
async def reload_strategies():
    strategy_manager.load_strategies()
    return {"status": "success", "count": len(strategy_manager.active_strategies)}

@router.get("/trades/active")
async def get_active_trades():
    return {"active_trades": list(order_manager.active_trades.values())}

@router.get("/trades/history")
async def get_trade_history():
    return {"history": order_manager.history}

@router.post("/backtest/run")
async def run_backtest(request: Request):
    from app.core.backtest_engine import backtest_engine
    import pandas as pd
    
    body = await request.json()
    strategy_name = body.get('strategy_name')
    symbol = body.get('symbol')
    overrides = body.get('parameters', {}) # e.g. {"ema_fast": {"period": 10}}
    
    # 1. Find the strategy
    strategy = next((s for s in strategy_manager.active_strategies if s['name'] == strategy_name), None)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
        
    token = fyers_auth.load_access_token()
    if not token:
        raise HTTPException(status_code=401, detail="Authentication required for historical data")
        
    # 2. Fetch Historical Data (Last 30 days)
    to_date = datetime.now().strftime("%Y-%m-%d")
    from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    # Map resolution (e.g. 1m -> 1, 1d -> 1D)
    res_map = {"1m": "1", "5m": "5", "15m": "15", "30m": "30", "1h": "60", "1d": "D"}
    resolution = res_map.get(strategy.get('timeframe', '1m'), '1')

    history = fyers_auth.get_history_data(token, symbol, resolution, from_date, to_date)
    if not history or history.get('s') != 'ok':
        error_msg = history.get('message', 'Fyers API error') if history else 'Timeout or Connection Error'
        raise HTTPException(status_code=400, detail=f"Fyers History Error: {error_msg}")
        
    if not history.get('candles'):
        raise HTTPException(status_code=400, detail="No historical candles returned for this symbol/range")
        
    # Convert to DataFrame
    cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame(history['candles'], columns=cols)
    
    # 3. Run Backtest
    results = backtest_engine.run_backtest(strategy, df, overrides)
    
    # 4. Save to SQLite and attach ID
    run_id = backtest_engine.save_results(results)
    results['summary']['id'] = run_id
    
    return results

@router.get("/backtest/history")
async def get_backtest_history():
    from app.core.database import SessionLocal, BacktestRun
    db = SessionLocal()
    runs = db.query(BacktestRun).order_by(BacktestRun.timestamp.desc()).all()
    db.close()
    return {"history": runs}

@router.get("/backtest/export/{run_id}")
async def export_backtest_csv(run_id: int):
    from app.core.database import SessionLocal, BacktestTrade, BacktestRun
    from fastapi.responses import StreamingResponse
    import io
    import csv
    
    db = SessionLocal()
    trades = db.query(BacktestTrade).filter(BacktestTrade.run_id == run_id).all()
    run = db.query(BacktestRun).filter(BacktestRun.id == run_id).first()
    db.close()
    
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Symbol', 'Entry Price', 'Exit Price', 'Entry Time', 'Exit Time', 'PnL', 'Exit Reason'])
    
    for t in trades:
        writer.writerow([t.symbol, t.entry_price, t.exit_price, t.entry_time, t.exit_time, t.pnl, t.exit_reason])
    
    output.seek(0)
    filename = f"backtest_{run.strategy_name}_{run.timestamp.strftime('%Y%m%d_%H%M%S')}.csv"
    
@router.delete("/backtest/clear")
async def clear_backtest_history():
    from app.core.database import SessionLocal, BacktestRun, BacktestTrade
    db = SessionLocal()
    try:
        db.query(BacktestTrade).delete()
        db.query(BacktestRun).delete()
        db.commit()
    finally:
        db.close()
    return {"message": "Backtest history cleared successfully"}
