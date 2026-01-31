#!/usr/bin/env python3
"""
Authentication Token Manager
Handles secure storage and management of FYERS authentication tokens
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict


class TokenManager:
    """Manage FYERS authentication tokens securely"""
    
    TOKEN_FILE = '.fyers_tokens.json'
    ENV_FILE = '.env'
    
    @staticmethod
    def save_tokens(access_token: str, expiry_timestamp: Optional[int] = None, 
                    refresh_token: Optional[str] = None):
        """
        Save authentication tokens to secure storage
        
        Args:
            access_token: FYERS access token
            expiry_timestamp: Unix timestamp when token expires
            refresh_token: Refresh token (optional)
        """
        
        if expiry_timestamp is None:
            # Default: token expires in 24 hours
            expiry_timestamp = int((datetime.now() + timedelta(hours=24)).timestamp())
        
        token_data = {
            'access_token': access_token,
            'refresh_token': refresh_token or '',
            'expiry': expiry_timestamp,
            'saved_at': datetime.now().isoformat(),
            'expires_at': datetime.fromtimestamp(expiry_timestamp).isoformat()
        }
        
        # Save to JSON file
        try:
            with open(TokenManager.TOKEN_FILE, 'w') as f:
                json.dump(token_data, f, indent=2)
            
            # Set restrictive file permissions (Unix/Linux/Mac)
            try:
                os.chmod(TokenManager.TOKEN_FILE, 0o600)
            except:
                pass
            
            print(f"✅ Tokens saved successfully")
            print(f"   File: {TokenManager.TOKEN_FILE}")
            print(f"   Access Token: {access_token[:20]}...")
            print(f"   Expires at: {datetime.fromtimestamp(expiry_timestamp).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Update .env file
            TokenManager._update_env_file('FYERS_ACCESS_TOKEN', access_token)
            TokenManager._update_env_file('TOKEN_EXPIRY', str(expiry_timestamp))
            
            if refresh_token:
                TokenManager._update_env_file('FYERS_REFRESH_TOKEN', refresh_token)
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving tokens: {e}")
            return False
    
    @staticmethod
    def load_tokens() -> Optional[Dict]:
        """
        Load tokens from secure storage
        
        Returns:
            Dictionary with token data or None if not found/expired
        """
        try:
            if not Path(TokenManager.TOKEN_FILE).exists():
                print("⚠️  No saved tokens found.")
                print("   Please authenticate first using: python auth_manager.py --login")
                return None
            
            with open(TokenManager.TOKEN_FILE, 'r') as f:
                token_data = json.load(f)
            
            expiry = token_data.get('expiry', 0)
            current_time = datetime.now().timestamp()
            
            # Check if token is expired
            if current_time > expiry:
                time_expired = datetime.fromtimestamp(expiry).strftime('%Y-%m-%d %H:%M:%S')
                print(f"⚠️  Token expired at: {time_expired}")
                print("   Please re-authenticate.")
                return None
            
            # Check if token expires soon (within 1 hour)
            time_remaining = expiry - current_time
            if time_remaining < 3600:
                minutes_left = int(time_remaining / 60)
                print(f"⚠️  Token expires in {minutes_left} minutes")
                print("   Consider refreshing your token soon.")
            
            return token_data
        
        except json.JSONDecodeError:
            print("❌ Error: Token file is corrupted")
            return None
        except Exception as e:
            print(f"❌ Error loading tokens: {e}")
            return None
    
    @staticmethod
    def get_access_token() -> Optional[str]:
        """
        Get valid access token
        
        Returns:
            Access token string or None if not available/expired
        """
        token_data = TokenManager.load_tokens()
        
        if token_data:
            return token_data.get('access_token')
        
        return None
    
    @staticmethod
    def is_token_valid() -> bool:
        """
        Check if current token is valid and not expired
        
        Returns:
            True if token is valid, False otherwise
        """
        token_data = TokenManager.load_tokens()
        
        if not token_data:
            return False
        
        expiry = token_data.get('expiry', 0)
        current_time = datetime.now().timestamp()
        
        # Consider token valid if it has more than 1 hour left
        return current_time < (expiry - 3600)
    
    @staticmethod
    def get_token_info() -> Dict:
        """
        Get information about current token
        
        Returns:
            Dictionary with token status information
        """
        token_data = TokenManager.load_tokens()
        
        if not token_data:
            return {
                'valid': False,
                'message': 'No token found',
                'expires_at': None,
                'time_remaining': 0
            }
        
        expiry = token_data.get('expiry', 0)
        current_time = datetime.now().timestamp()
        time_remaining = max(0, expiry - current_time)
        
        return {
            'valid': time_remaining > 3600,
            'expires_at': datetime.fromtimestamp(expiry).isoformat(),
            'time_remaining': int(time_remaining),
            'time_remaining_hours': round(time_remaining / 3600, 2),
            'saved_at': token_data.get('saved_at'),
            'access_token_preview': token_data.get('access_token', '')[:20] + '...'
        }
    
    @staticmethod
    def clear_tokens():
        """Clear all saved tokens"""
        try:
            # Remove token file
            if Path(TokenManager.TOKEN_FILE).exists():
                os.remove(TokenManager.TOKEN_FILE)
                print(f"✅ Token file deleted: {TokenManager.TOKEN_FILE}")
            
            # Clear from .env file
            TokenManager._update_env_file('FYERS_ACCESS_TOKEN', '')
            TokenManager._update_env_file('FYERS_REFRESH_TOKEN', '')
            TokenManager._update_env_file('TOKEN_EXPIRY', '')
            
            print("✅ All tokens cleared successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error clearing tokens: {e}")
            return False
    
    @staticmethod
    def _update_env_file(key: str, value: str):
        """
        Update a specific key in .env file
        
        Args:
            key: Environment variable name
            value: New value
        """
        env_path = Path(TokenManager.ENV_FILE)
        
        if not env_path.exists():
            print(f"⚠️  .env file not found. Creating new one...")
            env_path.touch()
        
        try:
            # Read existing content
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            # Update or add the key
            key_found = False
            for i, line in enumerate(lines):
                if line.strip().startswith(f"{key}="):
                    lines[i] = f"{key}={value}\n"
                    key_found = True
                    break
            
            if not key_found:
                # Add new key at the end
                if lines and not lines[-1].endswith('\n'):
                    lines.append('\n')
                lines.append(f"{key}={value}\n")
            
            # Write back
            with open(env_path, 'w') as f:
                f.writelines(lines)
            
        except Exception as e:
            print(f"⚠️  Could not update .env file: {e}")
    
    @staticmethod
    def display_status():
        """Display current authentication status"""
        print("\n" + "="*80)
        print("AUTHENTICATION STATUS")
        print("="*80)
        
        info = TokenManager.get_token_info()
        
        if info['valid']:
            print("✅ Status: AUTHENTICATED")
            print(f"   Token Preview: {info['access_token_preview']}")
            print(f"   Expires At: {info['expires_at']}")
            print(f"   Time Remaining: {info['time_remaining_hours']:.2f} hours")
            print(f"   Saved At: {info['saved_at']}")
        else:
            print("❌ Status: NOT AUTHENTICATED")
            print(f"   Message: {info['message']}")
            print("\n💡 To authenticate:")
            print("   1. Use Claude to login: 'Login to FYERS and authenticate'")
            print("   2. Save the token using: python auth_manager.py --save-token YOUR_TOKEN")
        
        print("="*80 + "\n")


def main():
    """Main function for CLI usage"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='FYERS Token Manager')
    parser.add_argument('--status', action='store_true', help='Show authentication status')
    parser.add_argument('--save-token', type=str, help='Save access token')
    parser.add_argument('--expiry', type=int, help='Token expiry timestamp')
    parser.add_argument('--clear', action='store_true', help='Clear all tokens')
    parser.add_argument('--get-token', action='store_true', help='Get current access token')
    
    args = parser.parse_args()
    
    if args.status or len(sys.argv) == 1:
        # Show status (default action)
        TokenManager.display_status()
    
    elif args.save_token:
        # Save token
        expiry = args.expiry
        if not expiry:
            # Default: 24 hours from now
            expiry = int((datetime.now() + timedelta(hours=24)).timestamp())
        
        TokenManager.save_tokens(args.save_token, expiry)
        print("\n✅ Token saved successfully!")
        TokenManager.display_status()
    
    elif args.clear:
        # Clear tokens
        confirm = input("⚠️  Are you sure you want to clear all tokens? (yes/no): ")
        if confirm.lower() in ['yes', 'y']:
            TokenManager.clear_tokens()
        else:
            print("❌ Operation cancelled")
    
    elif args.get_token:
        # Get token
        token = TokenManager.get_access_token()
        if token:
            print(f"Access Token: {token}")
        else:
            print("❌ No valid token found")
            sys.exit(1)


if __name__ == "__main__":
    main()
