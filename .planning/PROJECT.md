# Intraday Trading Bot

## Vision
Build a high-performance, fully autonomous intraday trading bot capable of executing complex strategies on Indian Stock Markets (via Fyers) and Crypto markets. The system emphasizes modularity for easy strategy definition via JSON and provides a premium, modern web dashboard for monitoring and control.

## Core Value
- **Autonomous Execution:** Removes emotional trading by executing logic-based strategies automatically.
- **Complex Strategy Support:** JSON-based configuration allowing for nested logic (AND/OR, Indicators, Time-based rules).
- **Real-time Monitoring:** A visual dashboard to track signals, positions, and P&L in real-time.

## Architecture
- **Backend:** Python (FastAPI) for high-performance strategy execution and API handling.
- **Frontend:** Next.js/React for a modern, responsive, and premium UI.
- **Broker Layer:** Adapter pattern to support Fyers initially, with extensibility for Crypto exchanges.
- **Data Layer:** WebSocket integration for real-time tick data processing.

## Constraints
- **Speed:** Intraday requires low-latency processing.
- **Reliability:** Must handle network failures and API rate limits gracefully.
