# Roadmap

## Phase 1: Foundation & Fyers Connectivity
**Goal:** Establish a working backend that connects to Fyers and streams data.
- **Requirements:** CORE-01, CORE-02
- **Deliverables:**
    - Python environment setup.
    - Fyers Authentication Module.
    - Real-time Data Streamer (WebSocket).

## Phase 2: Strategy Engine & JSON Parser
**Goal:** Build the logic engine that reads JSON config and evaluates data.
- **Requirements:** CORE-03, STRAT-01, STRAT-02, STRAT-03, STRAT-04
- **Deliverables:**
    - JSON Strategy Schema definition.
    - Indicator Calculation Library (pandas-ta/ta-lib).
    - Logic Evaluation Engine.

## Phase 3: Order Execution & Risk Management
**Goal:** Enable the bot to actually place and manage orders.
- **Requirements:** CORE-04
- **Deliverables:**
    - Order Execution Module (Place/Modify/Cancel).
    - Basic Risk Manager (Stoploss/Target handling).
    - Paper Trading Mode (Mock execution).

## Phase 4: Modern Web Dashboard
**Goal:** Create the visual interface for control and monitoring.
- **Requirements:** UI-01, UI-02, UI-03, UI-04
- **Deliverables:**
    - Next.js Frontend setup.
    - FastAPI API endpoints for UI.
    - WebSocket streaming to Frontend (Backend -> UI).
    - Deployment/Run scripts.
