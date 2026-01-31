import sys
import os
from pathlib import Path

# Add the project root to sys.path to allow imports from 'app'
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.fyers_handler import fyers_auth
from fyers_apiv3.fyersModel import FyersModel
from app.core.config import settings

def main():
    print("--- Fetching your Fyers Account Details ---\n")
    
    # Load the access token
    token = fyers_auth.load_access_token()
    if not token:
        print("[!] No active session found. Please login via the dashboard first.")
        return

    try:
        # Initialize Fyers Model
        fyers = FyersModel(
            client_id=settings.FYERS_APP_ID, 
            token=token, 
            is_async=False,
            log_path=str(Path.home())
        )
        
        # 1. Get Profile
        profile = fyers.get_profile()
        if profile.get('s') == 'ok':
            data = profile.get('data', {})
            print(f"[OK] Connection: SUCCESS")
            print(f"User: {data.get('name')} ({data.get('fy_id')})")
            print(f"Email: {data.get('email_id')}")
        else:
            print(f"[ERROR] Failed to fetch profile: {profile.get('message')}")
            return

        # 2. Get Funds
        funds = fyers.funds()
        if funds.get('s') == 'ok':
            fund_data = funds.get('fund_limits', [])
            # Find equity balance (usually the first item or identified by 'id')
            cash_balance = 0
            for item in fund_data:
                if item.get('title') == 'Total Balance':
                    cash_balance = item.get('equityAmount', 0)
            
            print(f"Cash Balance: INR {cash_balance:,}")
        
        print("\n[INFO] You are ready to trade! Since the market is currently closed,")
        print("       your live strategies will automatically start at 9:15 AM tomorrow.")

    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
