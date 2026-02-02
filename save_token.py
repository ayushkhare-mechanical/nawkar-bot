import json
from datetime import datetime, timedelta
from app.core.fyers_handler import fyers_auth

def main():
    print("--- Save Fyers Token ---")
    print("Paste the Access Token you obtained from trading.nirmitai.com below.")
    print("(You can also paste an Auth Code if the Redirect URI matches .env)")
    
    token_input = input("\nEnter Token/Code: ").strip()
    
    if not token_input:
        print("Error: No input provided.")
        return

    # 1. Try to see if it's a URL or Auth Code first
    if "://" in token_input or (len(token_input) < 100 and "&" in token_input):
         # Logic from generate_token (omitted for brevity, assuming raw token mostly)
         pass

    # 2. Assume it is a raw Access Token if it's long
    # (Fyers access tokens are usually quite long JWTs or opaque strings)
    if len(token_input) > 50:
        print(f"Saving as Access Token...")
        fyers_auth.save_access_token(token_input)
        
        # Validate
        print("Validating with Fyers API...")
        if fyers_auth.validate_token(token_input):
            print("SUCCESS: Token is valid and saved.")
        else:
            print("WARNING: Token saved but Fyers validation failed (Expired or Invalid).")
            
    else:
        # Try as Auth Code
        print("Input looks short. Attempting to exchange as Auth Code...")
        try:
            token = fyers_auth.generate_access_token(token_input)
            fyers_auth.save_access_token(token)
            print("SUCCESS: Exchanged Auth Code for Token and saved.")
        except Exception as e:
            print(f"ERROR: Could not exchange code. {e}")
            print("Ensure .env Redirect URI matches where you got this code.")

if __name__ == "__main__":
    main()
