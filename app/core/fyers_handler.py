import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict
from fyers_apiv3 import fyersModel
from app.core.config import settings
import webbrowser
import time

import requests
import requests.api

class FyersAuth:
    TOKEN_FILE = '.fyers_tokens.json'

    def __init__(self):
        # Apply Proxy settings if provided
        if settings.HTTP_PROXY:
            os.environ["HTTP_PROXY"] = settings.HTTP_PROXY
        if settings.HTTPS_PROXY:
            os.environ["HTTPS_PROXY"] = settings.HTTPS_PROXY

        # Monkeypatch requests to include User-Agent
        self._apply_patches()

        self.client_id = settings.FYERS_APP_ID
        self.secret_key = settings.FYERS_SECRET_KEY
        self.redirect_uri = settings.FYERS_REDIRECT_URI
        self.response_type = "code" 
        self.state = "sample_state"
        self.session = fyersModel.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key,
            redirect_uri=self.redirect_uri,
            response_type=self.response_type,
            state=self.state,
            grant_type='authorization_code'
        )

    def _apply_patches(self):
        """
        Global monkeypatch for requests to ensure User-Agent and Proxies are used.
        """
        ua = settings.USER_AGENT
        
        # 1. Patch Session.request (covers most SDK calls)
        original_session_request = requests.Session.request
        def patched_session_request(self, method, url, *args, **kwargs):
            headers = kwargs.get('headers')
            if headers is None or isinstance(headers, str):
                headers = {}
            if 'User-Agent' not in headers:
                headers['User-Agent'] = ua
            kwargs['headers'] = headers
            
            if 'proxies' not in kwargs and (settings.HTTP_PROXY or settings.HTTPS_PROXY):
                kwargs['proxies'] = {'http': settings.HTTP_PROXY, 'https': settings.HTTPS_PROXY}
            
            return original_session_request(self, method, url, *args, **kwargs)
        
        requests.Session.request = patched_session_request

        # 2. Patch requests.api.request (covers requests.get, requests.post, etc.)
        original_api_request = requests.api.request
        def patched_api_request(method, url, **kwargs):
            headers = kwargs.get('headers')
            if headers is None or isinstance(headers, str):
                headers = {}
            if 'User-Agent' not in headers:
                headers['User-Agent'] = ua
            kwargs['headers'] = headers
            return original_api_request(method, url, **kwargs)
        
        requests.api.request = patched_api_request
        requests.request = patched_api_request
        
        # 3. Patch explicit methods just in case they were already assigned
        for m in ['get', 'post', 'put', 'delete', 'patch', 'head']:
            def make_patch(method_name):
                orig = getattr(requests.api, method_name)
                def wrapped(url, **kwargs):
                    headers = kwargs.get('headers')
                    if headers is None or isinstance(headers, str):
                        headers = {}
                    if 'User-Agent' not in headers:
                        headers['User-Agent'] = ua
                    kwargs['headers'] = headers
                    return orig(url, **kwargs)
                return wrapped
            
            patched = make_patch(m)
            setattr(requests, m, patched)
            setattr(requests.api, m, patched)

    def get_login_url(self):
        url = self.session.generate_authcode()
        print(f"DEBUG: Generated Login URL: {url}")
        return url

    def generate_access_token(self, auth_code):
        self.session.set_token(auth_code)
        response = self.session.generate_token()
        if response.get('s') == 'ok':
            return response['access_token']
        else:
            raise Exception(f"Error generating token: {response.get('message')}")

    def save_access_token(self, access_token: str):
        expiry_timestamp = int((datetime.now() + timedelta(hours=24)).timestamp())
        token_data = {
            'access_token': access_token,
            'expiry': expiry_timestamp,
            'saved_at': datetime.now().isoformat(),
            'expires_at': datetime.fromtimestamp(expiry_timestamp).isoformat()
        }
        with open(self.TOKEN_FILE, 'w') as f:
            json.dump(token_data, f, indent=2)
        return True

    def load_access_token(self) -> Optional[str]:
        if not Path(self.TOKEN_FILE).exists():
            return None
        try:
            with open(self.TOKEN_FILE, 'r') as f:
                token_data = json.load(f)
            if datetime.now().timestamp() > token_data.get('expiry', 0):
                return None
            return token_data.get('access_token')
        except:
            return None

    def logout(self):
        """Clear the saved token session"""
        if Path(self.TOKEN_FILE).exists():
            os.remove(self.TOKEN_FILE)
        return True

    def validate_token(self, token: str) -> bool:
        """Perform a real API call to Fyers to check if the token is valid"""
        if not token or len(token) < 50: # Basic length check for a real token
            return False
            
        try:
            # We use a simple lightweight call like get_profile to validate
            from fyers_apiv3.fyersModel import FyersModel
            fyers = FyersModel(client_id=self.client_id, token=token, is_async=False)
            response = fyers.get_profile()
            
            # If 's' is 'ok', the token is valid
            return response.get('s') == 'ok'
        except Exception as e:
            print(f"Token validation failed: {str(e)}")
            return False

    def get_user_profile(self, token: str) -> Optional[Dict]:
        """Fetch user profile from Fyers"""
        if not token:
            return None
            
        try:
            from fyers_apiv3.fyersModel import FyersModel
            fyers = FyersModel(client_id=self.client_id, token=token, is_async=False)
            response = fyers.get_profile()
            
            if response.get('s') == 'ok':
                return response.get('data')
            return None
        except Exception as e:
            print(f"Error fetching profile: {str(e)}")
            return None

    def get_funds(self, token: str) -> Optional[Dict]:
        """Fetch fund details from Fyers"""
        if not token:
            return None
            
        try:
            from fyers_apiv3.fyersModel import FyersModel
            fyers = FyersModel(client_id=self.client_id, token=token, is_async=False)
            response = fyers.funds()
            
            if response.get('s') == 'ok':
                return response
            return None
        except Exception as e:
            print(f"Error fetching funds: {str(e)}")
            return None

    def get_holdings(self, token: str) -> Optional[Dict]:
        """Fetch holdings from Fyers"""
        if not token:
            return None
        try:
            from fyers_apiv3.fyersModel import FyersModel
            fyers = FyersModel(client_id=self.client_id, token=token, is_async=False)
            response = fyers.holdings()
            if response.get('s') == 'ok':
                return response
            return response # Return even if not ok to see error message in UI if needed
        except Exception as e:
            print(f"Error fetching holdings: {str(e)}")
            return None

    def get_positions(self, token: str) -> Optional[Dict]:
        """Fetch positions from Fyers"""
        if not token:
            return None
        try:
            from fyers_apiv3.fyersModel import FyersModel
            fyers = FyersModel(client_id=self.client_id, token=token, is_async=False)
            response = fyers.positions()
            if response.get('s') == 'ok':
                return response
            return response
        except Exception as e:
            print(f"Error fetching positions: {str(e)}")
            return None

    def get_orders(self, token: str) -> Optional[Dict]:
        """Fetch order book from Fyers"""
        if not token:
            return None
        try:
            from fyers_apiv3.fyersModel import FyersModel
            fyers = FyersModel(client_id=self.client_id, token=token, is_async=False)
            response = fyers.orderbook()
            if response.get('s') == 'ok':
                return response
            return response
        except Exception as e:
            print(f"Error fetching orders: {str(e)}")
            return None

    def place_order(self, token: str, data: Dict) -> Dict:
        """Place an order with Fyers"""
        try:
            from fyers_apiv3.fyersModel import FyersModel
            fyers = FyersModel(client_id=self.client_id, token=token, is_async=False)
            return fyers.place_order(data=data)
        except Exception as e:
            print(f"Error placing order: {str(e)}")
            return {"s": "error", "message": str(e)}

    def get_history_data(self, token: str, symbol: str, resolution: str, range_from: str, range_to: str) -> Optional[Dict]:
        """Fetch historical candle data from Fyers"""
        try:
            from fyers_apiv3.fyersModel import FyersModel
            fyers = FyersModel(client_id=self.client_id, token=token, is_async=False)
            data = {
                "symbol": symbol,
                "resolution": resolution,
                "date_format": "1", # yyyy-mm-dd
                "range_from": range_from,
                "range_to": range_to,
                "cont_flag": "1"
            }
            return fyers.history(data=data)
        except Exception as e:
            print(f"Error fetching historical data: {str(e)}")
            return None

fyers_auth = FyersAuth()
