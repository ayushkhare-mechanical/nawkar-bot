import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.fyers_handler import fyers_auth
from app.core.config import settings

def main():
    print("--- Fyers Token Generator ---")
    print(f"App ID: {settings.FYERS_APP_ID}")
    print(f"Redirect URI: {settings.FYERS_REDIRECT_URI}")
    
    login_url = fyers_auth.get_login_url()
    print(f"\n1. Open this URL in your browser:\n{login_url}\n")
    print("2. Login to Fyers.")
    print("3. After login, you will be redirected to a URL (e.g. localhost:8000/api/v1/auth/callback...)")
    print("4. Copy that FULL URL (or just the auth_code) and paste it below.")
    
    auth_input = input("\nEnter Redirect URL or Auth Code: ").strip()
    
    if not auth_input:
        print("Error: No input provided.")
        return

    try:
        access_token = None
        
        # Try to extract from URL
        if "://" in auth_input or "auth_code=" in auth_input:
            from urllib.parse import urlparse, parse_qs
            import urllib
            
            # Handle full URL or partial query string
            if "://" not in auth_input and "?" not in auth_input:
               auth_input = "?" + auth_input
               
            parsed = urlparse(auth_input)
            qs = parse_qs(parsed.query)
            
            if 'auth_code' in qs:
                auth_code = qs['auth_code'][0]
                print(f"Found Auth Code: {auth_code[:10]}...")
                access_token = fyers_auth.generate_access_token(auth_code)
            else:
                 print("Could not find 'auth_code' in the URL.")
                 return
        else:
             # Assume raw auth code
             print(f"Assuming input is raw Auth Code...")
             auth_code = auth_input
             access_token = fyers_auth.generate_access_token(auth_code)
             
        if access_token:
            fyers_auth.save_access_token(access_token)
            print("\nSUCCESS: Access Token generated and saved to .fyers_tokens.json")
            print("You can now refresh the Dashboard.")
        else:
            print("Failed to generate access token.")

    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    main()
