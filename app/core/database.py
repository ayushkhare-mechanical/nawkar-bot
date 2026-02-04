from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DB_URL = "sqlite:///logs/backtest_results.db"
os.makedirs("logs", exist_ok=True)

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BacktestRun(Base):
    __tablename__ = "backtest_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_name = Column(String)
    symbol = Column(String)
    parameters = Column(JSON)
    total_pnl = Column(Float)
    win_rate = Column(Float)
    total_trades = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

class BacktestTrade(Base):
    __tablename__ = "backtest_trades"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("backtest_runs.id"))
    symbol = Column(String)
    entry_price = Column(Float)
    exit_price = Column(Float)
    entry_time = Column(String)
    exit_time = Column(String)
    pnl = Column(Float)
    exit_reason = Column(String)

Base.metadata.create_all(bind=engine)
