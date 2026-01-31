# FYERS 1Min Strategy - Environment Setup Guide

## 🔐 Secure Environment Configuration

This guide will help you set up a secure `.env` file for your FYERS trading application with all necessary API credentials and configuration.

---

## Part 1: FYERS API Credentials Setup

### Step 1: Get Your FYERS API Credentials

1. **Login to FYERS Developer Portal**
   - Go to: https://myapi.fyers.in/dashboard
   - Login with your FYERS credentials

2. **Create a New App**
   - Click on "My Apps" or "Create App"
   - Fill in the details:
     - **App Name**: "1Min Strategy App"
     - **App Type**: "Web App"
     - **Redirect URL**: `http://localhost:5000/callback` (for local development)
     - **Description**: "Automated trading strategy for intraday"

3. **Get Your Credentials**
   After creating the app, you'll receive:
   - **App ID** (Client ID) - Example: `ABC12345-100`
   - **App Secret** (Secret Key) - Example: `1A2B3C4D5E6F7G8H9I0J`
   - **Redirect URI** - Example: `http://localhost:5000/callback`

---

## Part 2: Create .env File

### Create `.env` file in your project root directory

```bash
# Create the file
touch .env

# Set proper permissions (Unix/Linux/Mac)
chmod 600 .env
```

### `.env` File Template

Copy this template and fill in your actual values:

```env
# ==============================================================================
# FYERS API CONFIGURATION
# ==============================================================================

# Your FYERS App ID (Client ID)
# Get this from: https://myapi.fyers.in/dashboard
FYERS_APP_ID=ABC12345-100

# Your FYERS App Secret (Secret Key)
# KEEP THIS SECRET! Never commit to version control
FYERS_APP_SECRET=1A2B3C4D5E6F7G8H9I0J

# Redirect URI configured in FYERS App
FYERS_REDIRECT_URI=http://localhost:5000/callback

# FYERS API Base URL
FYERS_API_URL=https://api-t1.fyers.in/api/v3

# ==============================================================================
# AUTHENTICATION TOKENS (Auto-generated)
# ==============================================================================

# Access Token (Generated after authentication - leave empty initially)
FYERS_ACCESS_TOKEN=

# Refresh Token (For extending session)
FYERS_REFRESH_TOKEN=

# Token Expiry (Unix timestamp)
TOKEN_EXPIRY=

# ==============================================================================
# STRATEGY CONFIGURATION
# ==============================================================================

# Stock Selection Criteria
MIN_BODY_PERCENT=0.8
MIN_BODY_RATIO=0.75

# Risk Management
RISK_REWARD_RATIO=2.0
MAX_POSITIONS=5
CAPITAL_PER_TRADE=50000
MAX_DAILY_LOSS=5000

# Position Sizing
RISK_PER_TRADE=1000
MAX_CAPITAL_ALLOCATION=250000

# ==============================================================================
# TRADING HOURS
# ==============================================================================

MARKET_OPEN_TIME=09:15
MARKET_CLOSE_TIME=15:30
SCAN_TIME=09:00

# ==============================================================================
# DATABASE CONFIGURATION (Optional)
# ==============================================================================

# SQLite Database Path (for trade logging)
DB_PATH=./data/trades.db

# MongoDB (if using cloud database)
# MONGODB_URI=mongodb://localhost:27017/trading_strategy

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================

LOG_LEVEL=INFO
LOG_FILE=./logs/strategy.log
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5

# ==============================================================================
# NOTIFICATION SETTINGS (Optional)
# ==============================================================================

# Email Notifications
EMAIL_ENABLED=false
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
ALERT_EMAIL=trader@example.com

# Telegram Notifications
TELEGRAM_ENABLED=false
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id

# ==============================================================================
# DEVELOPMENT/PRODUCTION SETTINGS
# ==============================================================================

# Environment Mode: development, staging, production
ENVIRONMENT=development

# Paper Trading Mode (true = no real orders)
PAPER_TRADING=true

# Debug Mode
DEBUG=true

# API Rate Limiting
API_RATE_LIMIT=50
API_RATE_PERIOD=60

# ==============================================================================
# WEB DASHBOARD CONFIGURATION (Optional)
# ==============================================================================

# Dashboard Server Settings
DASHBOARD_PORT=5000
DASHBOARD_HOST=0.0.0.0
DASHBOARD_SECRET_KEY=change-this-to-random-secret-key

# Dashboard Authentication
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=change-this-password

# ==============================================================================
# BACKUP AND DATA STORAGE
# ==============================================================================

# Data Storage Path
DATA_DIR=./data
BACKUP_DIR=./backups
REPORTS_DIR=./reports

# Auto-backup trades
AUTO_BACKUP=true
BACKUP_FREQUENCY=daily

# ==============================================================================
# ADVANCED FEATURES
# ==============================================================================

# Enable trailing stop loss
ENABLE_TRAILING_SL=false
TRAILING_SL_PERCENT=0.5

# Enable partial profit booking
ENABLE_PARTIAL_BOOKING=false
PARTIAL_BOOK_AT_PERCENT=75

# Re-entry after stop loss
ENABLE_REENTRY=false
REENTRY_AFTER_MINUTES=15

# ==============================================================================
# WATCHLIST CONFIGURATION
# ==============================================================================

# Nifty 100 Stock List
STOCK_UNIVERSE=NIFTY100

# Custom stock list (comma-separated)
# CUSTOM_STOCKS=NSE:RELIANCE-EQ,NSE:TCS-EQ,NSE:INFY-EQ

# ==============================================================================
# NOTES
# ==============================================================================

# 1. Never commit this .env file to version control
# 2. Add .env to your .gitignore file
# 3. Keep backup of credentials in secure password manager
# 4. Rotate API keys periodically for security
# 5. Use different credentials for development and production
```

---

## Part 3: Create `.env.example` File

Create a template file for other developers (without sensitive data):

```env
# ==============================================================================
# FYERS API CONFIGURATION - .env.example
# ==============================================================================
# Copy this file to .env and fill in your actual values

FYERS_APP_ID=your-app-id-here
FYERS_APP_SECRET=your-app-secret-here
FYERS_REDIRECT_URI=http://localhost:5000/callback
FYERS_API_URL=https://api-t1.fyers.in/api/v3

FYERS_ACCESS_TOKEN=
FYERS_REFRESH_TOKEN=
TOKEN_EXPIRY=

MIN_BODY_PERCENT=0.8
MIN_BODY_RATIO=0.75
RISK_REWARD_RATIO=2.0
MAX_POSITIONS=5
CAPITAL_PER_TRADE=50000
MAX_DAILY_LOSS=5000

MARKET_OPEN_TIME=09:15
MARKET_CLOSE_TIME=15:30

ENVIRONMENT=development
PAPER_TRADING=true
DEBUG=true

LOG_LEVEL=INFO
LOG_FILE=./logs/strategy.log
```

---

## Part 4: Update .gitignore

Create or update your `.gitignore` file:

```gitignore
# Environment Variables
.env
.env.local
.env.*.local

# Secrets and Credentials
*.key
*.pem
*.p12
secrets/
credentials/

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Database
*.db
*.sqlite
*.sqlite3
data/
backups/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Reports and Outputs
reports/
outputs/
*.csv
*.xlsx

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Compiled files
*.pyc
dist/
build/
```

---

## Part 5: Load Environment Variables in Python

### Create `config.py`:

```python
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Application configuration from environment variables"""
    
    # FYERS API Configuration
    FYERS_APP_ID = os.getenv('FYERS_APP_ID')
    FYERS_APP_SECRET = os.getenv('FYERS_APP_SECRET')
    FYERS_REDIRECT_URI = os.getenv('FYERS_REDIRECT_URI')
    FYERS_API_URL = os.getenv('FYERS_API_URL', 'https://api-t1.fyers.in/api/v3')
    
    # Authentication Tokens
    FYERS_ACCESS_TOKEN = os.getenv('FYERS_ACCESS_TOKEN', '')
    FYERS_REFRESH_TOKEN = os.getenv('FYERS_REFRESH_TOKEN', '')
    TOKEN_EXPIRY = os.getenv('TOKEN_EXPIRY', '')
    
    # Strategy Configuration
    MIN_BODY_PERCENT = float(os.getenv('MIN_BODY_PERCENT', 0.8))
    MIN_BODY_RATIO = float(os.getenv('MIN_BODY_RATIO', 0.75))
    RISK_REWARD_RATIO = float(os.getenv('RISK_REWARD_RATIO', 2.0))
    MAX_POSITIONS = int(os.getenv('MAX_POSITIONS', 5))
    CAPITAL_PER_TRADE = float(os.getenv('CAPITAL_PER_TRADE', 50000))
    MAX_DAILY_LOSS = float(os.getenv('MAX_DAILY_LOSS', 5000))
    
    # Trading Hours
    MARKET_OPEN_TIME = os.getenv('MARKET_OPEN_TIME', '09:15')
    MARKET_CLOSE_TIME = os.getenv('MARKET_CLOSE_TIME', '15:30')
    
    # Environment Settings
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    PAPER_TRADING = os.getenv('PAPER_TRADING', 'true').lower() == 'true'
    DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', './logs/strategy.log')
    
    # Database
    DB_PATH = os.getenv('DB_PATH', './data/trades.db')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required_vars = [
            'FYERS_APP_ID',
            'FYERS_APP_SECRET',
            'FYERS_REDIRECT_URI'
        ]
        
        missing = []
        for var in required_vars:
            if not getattr(cls, var):
                missing.append(var)
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True
    
    @classmethod
    def display_config(cls):
        """Display current configuration (hide sensitive data)"""
        print("="*80)
        print("CURRENT CONFIGURATION")
        print("="*80)
        print(f"Environment: {cls.ENVIRONMENT}")
        print(f"Paper Trading: {cls.PAPER_TRADING}")
        print(f"Debug Mode: {cls.DEBUG}")
        print(f"App ID: {cls.FYERS_APP_ID[:10]}..." if cls.FYERS_APP_ID else "Not Set")
        print(f"API URL: {cls.FYERS_API_URL}")
        print(f"Max Positions: {cls.MAX_POSITIONS}")
        print(f"Capital per Trade: ₹{cls.CAPITAL_PER_TRADE:,.2f}")
        print(f"Max Daily Loss: ₹{cls.MAX_DAILY_LOSS:,.2f}")
        print("="*80)


# Usage in your code
if __name__ == "__main__":
    try:
        Config.validate()
        Config.display_config()
        print("✅ Configuration loaded successfully!")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
```

---

## Part 6: Install Required Packages

### Create `requirements.txt`:

```txt
# Core Dependencies
python-dotenv==1.0.0
requests==2.31.0
pandas==2.1.0
numpy==1.24.3

# FYERS SDK (if available)
# fyers-apiv3==3.0.0

# Database
sqlalchemy==2.0.20

# Logging
colorlog==6.7.0

# Web Dashboard (Optional)
flask==3.0.0
flask-cors==4.0.0

# Notifications (Optional)
python-telegram-bot==20.5

# Utilities
python-dateutil==2.8.2
pytz==2023.3
```

### Install packages:

```bash
pip install -r requirements.txt
```

---

## Part 7: Token Management Module

### Create `auth_manager.py`:

```python
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from config import Config

class TokenManager:
    """Manage FYERS authentication tokens"""
    
    TOKEN_FILE = '.fyers_tokens.json'
    
    @staticmethod
    def save_tokens(access_token: str, expiry_timestamp: int = None):
        """Save tokens to file and environment"""
        
        if expiry_timestamp is None:
            # Default: token expires in 24 hours
            expiry_timestamp = int((datetime.now() + timedelta(hours=24)).timestamp())
        
        token_data = {
            'access_token': access_token,
            'expiry': expiry_timestamp,
            'saved_at': datetime.now().isoformat()
        }
        
        # Save to file
        with open(TokenManager.TOKEN_FILE, 'w') as f:
            json.dump(token_data, f, indent=2)
        
        # Update .env file
        TokenManager._update_env_file('FYERS_ACCESS_TOKEN', access_token)
        TokenManager._update_env_file('TOKEN_EXPIRY', str(expiry_timestamp))
        
        print(f"✅ Tokens saved successfully")
        print(f"   Access Token: {access_token[:20]}...")
        print(f"   Expires at: {datetime.fromtimestamp(expiry_timestamp)}")
    
    @staticmethod
    def load_tokens():
        """Load tokens from file"""
        try:
            with open(TokenManager.TOKEN_FILE, 'r') as f:
                token_data = json.load(f)
            
            expiry = token_data.get('expiry', 0)
            
            # Check if token is expired
            if datetime.now().timestamp() > expiry:
                print("⚠️  Token has expired. Please re-authenticate.")
                return None
            
            return token_data
        
        except FileNotFoundError:
            print("⚠️  No saved tokens found. Please authenticate first.")
            return None
    
    @staticmethod
    def is_token_valid():
        """Check if current token is valid"""
        token_data = TokenManager.load_tokens()
        
        if not token_data:
            return False
        
        expiry = token_data.get('expiry', 0)
        current_time = datetime.now().timestamp()
        
        # Consider token valid if it has more than 1 hour left
        return current_time < (expiry - 3600)
    
    @staticmethod
    def _update_env_file(key: str, value: str):
        """Update a specific key in .env file"""
        env_path = Path('.env')
        
        if not env_path.exists():
            return
        
        # Read existing content
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        # Update or add the key
        key_found = False
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                key_found = True
                break
        
        if not key_found:
            lines.append(f"{key}={value}\n")
        
        # Write back
        with open(env_path, 'w') as f:
            f.writelines(lines)
    
    @staticmethod
    def clear_tokens():
        """Clear saved tokens"""
        if Path(TokenManager.TOKEN_FILE).exists():
            os.remove(TokenManager.TOKEN_FILE)
        
        TokenManager._update_env_file('FYERS_ACCESS_TOKEN', '')
        TokenManager._update_env_file('TOKEN_EXPIRY', '')
        
        print("✅ Tokens cleared")
```

---

## Part 8: Security Best Practices

### 🔒 Security Checklist

```markdown
✅ 1. Never commit .env file to version control
✅ 2. Add .env to .gitignore
✅ 3. Use .env.example for sharing configuration structure
✅ 4. Store credentials in secure password manager
✅ 5. Use different credentials for dev/staging/production
✅ 6. Rotate API keys regularly (every 3-6 months)
✅ 7. Use environment-specific .env files (.env.dev, .env.prod)
✅ 8. Encrypt sensitive data at rest
✅ 9. Use HTTPS for all API communications
✅ 10. Implement rate limiting for API calls
✅ 11. Log security events (auth failures, token expiry)
✅ 12. Set proper file permissions (chmod 600 .env)
✅ 13. Never log sensitive credentials
✅ 14. Use secure token storage (not plain text in code)
✅ 15. Implement token refresh mechanism
```

---

## Part 9: Quick Setup Script

### Create `setup.sh`:

```bash
#!/bin/bash

echo "🚀 Setting up FYERS 1Min Strategy Environment"
echo "=============================================="

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs backups reports

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your credentials."
else
    echo "⚠️  .env file already exists. Skipping..."
fi

# Set proper permissions
echo "🔒 Setting file permissions..."
chmod 600 .env
chmod 600 .fyers_tokens.json 2>/dev/null || true

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << EOF
.env
.env.local
*.log
data/
logs/
backups/
__pycache__/
*.pyc
.fyers_tokens.json
EOF
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your FYERS API credentials"
echo "2. Run: python config.py (to validate configuration)"
echo "3. Authenticate with FYERS"
echo "4. Start trading!"
```

### Make it executable:

```bash
chmod +x setup.sh
./setup.sh
```

---

## Part 10: Usage Examples

### Example 1: Basic Usage

```python
from config import Config
from auth_manager import TokenManager

# Load configuration
Config.validate()
Config.display_config()

# Check if authenticated
if not TokenManager.is_token_valid():
    print("⚠️  Please authenticate first!")
    # Trigger authentication flow
else:
    print("✅ Authentication valid!")
    # Start trading
```

### Example 2: With Claude Integration

**Prompt to use with Claude:**

```
I need to authenticate with FYERS and save my credentials securely.

My FYERS credentials:
- App ID: ABC12345-100
- App Secret: [I'll provide this separately]
- Redirect URI: http://localhost:5000/callback

Please:
1. Login to FYERS
2. Save the access token to my .env file
3. Confirm the token is working by checking my account balance
```

---

## 🎯 Summary

You now have:

✅ Complete `.env` file template with all configurations
✅ Security best practices for credential management  
✅ Token management system with auto-expiry
✅ Configuration module for easy access
✅ Setup script for quick initialization
✅ `.gitignore` to prevent credential leaks

### Quick Start Commands:

```bash
# 1. Setup environment
./setup.sh

# 2. Edit .env with your credentials
nano .env

# 3. Validate configuration
python config.py

# 4. Authenticate with Claude
# Use the prompts in the execution_workflow.md file

# 5. Start trading
python strategy_runner.py --mode scan
```

**Remember**: NEVER share your `.env` file or commit it to version control!
