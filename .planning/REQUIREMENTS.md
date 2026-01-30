# Requirements

## v1 Requirements

### Core Engine
- [ ] **CORE-01:** System can connect to Fyers API and authenticate successfully.
- [ ] **CORE-02:** Engine can ingest real-time tick data via Fyers WebSocket.
- [ ] **CORE-03:** Engine processes configured strategies against incoming data stream.
- [ ] **CORE-04:** Order Manager handles Buy/Sell/Stoploss/Target orders automatically.

### Strategy System
- [ ] **STRAT-01:** Load strategies from JSON configuration files.
- [ ] **STRAT-02:** Support basic indicators (RSI, EMA, SMA, MACD).
- [ ] **STRAT-03:** Support complex logic groups (AND/OR conditions).
- [ ] **STRAT-04:** Support time-based constraints (e.g., "Only trade between 10:00 and 11:00").

### User Interface (Dashboard)
- [ ] **UI-01:** Modern Dashboard showing current P&L and Active Positions.
- [ ] **UI-02:** Real-time log/console view of bot actions.
- [ ] **UI-03:** Ability to Start/Stop the bot engine from the UI.
- [ ] **UI-04:** Visual indicator of connected broker status.

## v2 Requirements
- Multi-broker support (Crypto exchanges).
- Visual Strategy Builder (Drag & Drop).
- Backtesting Engine.

## Out of Scope (v1)
- High-Frequency Trading (HFT) arbitrage.
- AI/ML-based prediction models (unless defined in JSON logic).
