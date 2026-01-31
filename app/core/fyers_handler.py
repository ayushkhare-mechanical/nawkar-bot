import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict
from fyers_apiv3 import fyersModel
from app.core.config import settings
import webbrowser
import time

class FyersAuth:
    TOKEN_FILE = '.fyers_tokens.json'

    def __init__(self):
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
            grant_type='authorization_code'
        )

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
