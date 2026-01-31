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

        self.client_id = settings.FYERS_CLIENT_ID
        self.secret_key = settings.FYERS_SECRET_KEY
        self.redirect_uri = settings.FYERS_REDIRECT_URI
        self.response_type = "code" 
        self.state = "sample_state"
        self.session = fyersModel.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key,
            redirect_uri=self.redirect_uri,
            response_type=self.response_type,
            grant_type='authorization_code'
        )

    def _apply_patches(self):
        """
        Global monkeypatch for requests to ensure User-Agent and Proxies are used.
        """
        original_request = requests.Session.request
        ua = settings.USER_AGENT

        def patched_request(self, method, url, *args, **kwargs):
            headers = kwargs.get('headers', {})
            if headers is None: headers = {}
            
            # Ensure User-Agent is set
            if 'User-Agent' not in headers:
                headers['User-Agent'] = ua
            
            kwargs['headers'] = headers
            
            # Apply proxies to kwargs if not present
            if 'proxies' not in kwargs and (settings.HTTP_PROXY or settings.HTTPS_PROXY):
                kwargs['proxies'] = {
                    'http': settings.HTTP_PROXY,
                    'https': settings.HTTPS_PROXY
                }
            
            return original_request(self, method, url, *args, **kwargs)

        # Apply to Session.request
        requests.Session.request = patched_request

        # Also patch requests.request for direct calls like requests.post
        original_direct_request = requests.request
        def patched_direct_request(method, url, **kwargs):
            headers = kwargs.get('headers', {})
            if headers is None: headers = {}
            if 'User-Agent' not in headers:
                headers['User-Agent'] = ua
            kwargs['headers'] = headers
            return original_direct_request(method, url, **kwargs)
        
        requests.request = patched_direct_request

    def get_login_url(self):
        return self.session.generate_authcode()

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

fyers_auth = FyersAuth()
