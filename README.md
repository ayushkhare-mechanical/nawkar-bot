# Nawkar Trading Bot - Quick Start Guide

This guide provides instructions on how to run and test the Nawkar Trading Bot application.

## 🚀 How to Run

### 1. Prerequisites
- Python 3.10+
- Fyers API Credentials (App ID, Secret Key)

### 2. Environment Setup
The bot requires a `.env` file in the root directory. Use the provided template:

```env
FYERS_CLIENT_ID="Your_Client_ID"
FYERS_APP_ID="Your_App_ID"
FYERS_SECRET_KEY="Your_Secret_Key"
FYERS_REDIRECT_URI="https://trading.nirmitai.com/auth/callback"
```

### 3. Installation
Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

### 4. Running the Dashboard
Start the FastAPI server:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Visit `http://localhost:8000` in your browser.

---

## 🐳 Running with Docker

We provide an optimized, multi-stage Docker image that includes a Python virtual environment.

### 1. Build the Image
```bash
docker build -t nawkar-bot .
```

### 2. Run the Container
```bash
docker run -p 8000:8000 --env-file .env nawkar-bot
```

---

## ☁️ Deployment to Render

This project is optimized for deployment on **Render.com**.

1.  **Push your code** to GitHub or GitLab.
2.  **Create a New Web Service** on Render.
3.  **Runtime**: Select **Docker**.
4.  **Environment Variables**: In the Render Dashboard, add your `.env` variables (e.g., `FYERS_SECRET_KEY`) under the **Environment** tab.

> [!IMPORTANT]
> To avoid startup crashes, the app includes default empty values for credentials, but you **must** provide real ones in the Render dashboard for the bot to function.

## 🔐 Authentication Flow

Since you are running locally but the redirect URI points to your production server (`trading.nirmitai.com`):

1. **Login**: Click "Connect Fyers Account" on the dashboard.
2. **Authenticate**: Log in on the Fyers page.
3. **Capture Token**: After redirecting to Render, capture the `access_token` from your Render logs or dashboard.
4. **Sync Locally**: Save the token to your local environment:
   ```bash
   python must-read-files/auth_manager.py --save-token YOUR_ACCESS_TOKEN
   ```

## 🧪 How to Test

### 1. Verify Authentication
Check the dashboard at `http://localhost:8000`. It should show **Connected** and display a preview of your Token ID.

### 2. Test Strategy Logic
You can run a scan to see which stocks are currently eligible for the 1-minute strategy:
```bash
python app/scripts/scan_stocks.py
```

### 3. Monitor Data Stream
To verify the connection to Fyers data feed:
```bash
python app/core/data_streamer.py
```

## 📂 Project Structure
- `app/main.py`: Entry point for the web dashboard.
- `app/core/fyers_handler.py`: Handles Fyers API authentication and session.
- `app/strategies/`: Contains logic for the 1-minute trading strategy.
- `must-read-files/`: Detailed documentation and utility scripts.
