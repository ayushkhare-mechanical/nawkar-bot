#!/usr/bin/env python3
"""
Configuration Management Module
Loads and validates environment variables from .env file
"""

import os
from dotenv import load_dotenv
from pathlib import Path
import sys

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Application configuration from environment variables"""
    
    # ==============================================================================
    # FYERS API CONFIGURATION
    # ==============================================================================
    
    FYERS_APP_ID = os.getenv('FYERS_APP_ID')
    FYERS_APP_SECRET = os.getenv('FYERS_APP_SECRET')
    FYERS_REDIRECT_URI = os.getenv('FYERS_REDIRECT_URI', 'http://localhost:5000/callback')
    FYERS_API_URL = os.getenv('FYERS_API_URL', 'https://api-t1.fyers.in/api/v3')
    
    # Authentication Tokens
    FYERS_ACCESS_TOKEN = os.getenv('FYERS_ACCESS_TOKEN', '')
    FYERS_REFRESH_TOKEN = os.getenv('FYERS_REFRESH_TOKEN', '')
    TOKEN_EXPIRY = os.getenv('TOKEN_EXPIRY', '')
    
    # ==============================================================================
    # STRATEGY CONFIGURATION
    # ==============================================================================
    
    # Stock Selection Criteria
    MIN_BODY_PERCENT = float(os.getenv('MIN_BODY_PERCENT', 0.8))
    MIN_BODY_RATIO = float(os.getenv('MIN_BODY_RATIO', 0.75))
    
    # Risk Management
    RISK_REWARD_RATIO = float(os.getenv('RISK_REWARD_RATIO', 2.0))
    MAX_POSITIONS = int(os.getenv('MAX_POSITIONS', 5))
    CAPITAL_PER_TRADE = float(os.getenv('CAPITAL_PER_TRADE', 50000))
    MAX_DAILY_LOSS = float(os.getenv('MAX_DAILY_LOSS', 5000))
    RISK_PER_TRADE = float(os.getenv('RISK_PER_TRADE', 1000))
    
    # ==============================================================================
    # TRADING HOURS
    # ==============================================================================
    
    MARKET_OPEN_TIME = os.getenv('MARKET_OPEN_TIME', '09:15')
    MARKET_CLOSE_TIME = os.getenv('MARKET_CLOSE_TIME', '15:30')
    SCAN_TIME = os.getenv('SCAN_TIME', '09:00')
    
    # ==============================================================================
    # ENVIRONMENT SETTINGS
    # ==============================================================================
    
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    PAPER_TRADING = os.getenv('PAPER_TRADING', 'true').lower() == 'true'
    DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'
    
    # ==============================================================================
    # LOGGING CONFIGURATION
    # ==============================================================================
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', './logs/strategy.log')
    LOG_MAX_SIZE = int(os.getenv('LOG_MAX_SIZE', 10485760))
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))
    
    # ==============================================================================
    # DATABASE CONFIGURATION
    # ==============================================================================
    
    DB_PATH = os.getenv('DB_PATH', './data/trades.db')
    
    # ==============================================================================
    # NOTIFICATION SETTINGS
    # ==============================================================================
    
    # Email
    EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'false').lower() == 'true'
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    ALERT_EMAIL = os.getenv('ALERT_EMAIL', '')
    
    # Telegram
    TELEGRAM_ENABLED = os.getenv('TELEGRAM_ENABLED', 'false').lower() == 'true'
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    
    # ==============================================================================
    # DASHBOARD CONFIGURATION
    # ==============================================================================
    
    DASHBOARD_PORT = int(os.getenv('DASHBOARD_PORT', 5000))
    DASHBOARD_HOST = os.getenv('DASHBOARD_HOST', '0.0.0.0')
    DASHBOARD_SECRET_KEY = os.getenv('DASHBOARD_SECRET_KEY', 'change-this-secret')
    DASHBOARD_USERNAME = os.getenv('DASHBOARD_USERNAME', 'admin')
    DASHBOARD_PASSWORD = os.getenv('DASHBOARD_PASSWORD', 'change-this-password')
    
    # ==============================================================================
    # VALIDATION METHODS
    # ==============================================================================
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        warnings = []
        
        # Required variables
        required_vars = {
            'FYERS_APP_ID': cls.FYERS_APP_ID,
            'FYERS_APP_SECRET': cls.FYERS_APP_SECRET,
            'FYERS_REDIRECT_URI': cls.FYERS_REDIRECT_URI
        }
        
        for var_name, var_value in required_vars.items():
            if not var_value or var_value == 'your-app-id-here' or var_value == 'your-app-secret-here':
                errors.append(f"❌ {var_name} is not configured")
        
        # Warnings for security
        if cls.DASHBOARD_SECRET_KEY == 'change-this-secret':
            warnings.append("⚠️  DASHBOARD_SECRET_KEY should be changed")
        
        if cls.DASHBOARD_PASSWORD == 'change-this-password':
            warnings.append("⚠️  DASHBOARD_PASSWORD should be changed")
        
        # Display errors and warnings
        if errors:
            print("\n" + "="*80)
            print("CONFIGURATION ERRORS")
            print("="*80)
            for error in errors:
                print(error)
            print("\n💡 Tip: Copy .env.example to .env and fill in your FYERS API credentials")
            print("   Get credentials from: https://myapi.fyers.in/dashboard")
            print("="*80)
            return False
        
        if warnings:
            print("\n" + "="*80)
            print("CONFIGURATION WARNINGS")
            print("="*80)
            for warning in warnings:
                print(warning)
            print("="*80)
        
        return True
    
    @classmethod
    def display_config(cls, show_sensitive=False):
        """Display current configuration (hide sensitive data by default)"""
        print("\n" + "="*80)
        print("CURRENT CONFIGURATION")
        print("="*80)
        
        print("\n📊 ENVIRONMENT:")
        print(f"   Mode: {cls.ENVIRONMENT}")
        print(f"   Paper Trading: {'✅ Enabled' if cls.PAPER_TRADING else '❌ Disabled'}")
        print(f"   Debug: {'✅ Enabled' if cls.DEBUG else '❌ Disabled'}")
        
        print("\n🔐 FYERS API:")
        if show_sensitive:
            print(f"   App ID: {cls.FYERS_APP_ID}")
            print(f"   App Secret: {cls.FYERS_APP_SECRET}")
        else:
            print(f"   App ID: {cls.FYERS_APP_ID[:10]}..." if cls.FYERS_APP_ID else "   App ID: Not Set")
            print(f"   App Secret: {'*' * 20}" if cls.FYERS_APP_SECRET else "   App Secret: Not Set")
        
        print(f"   Redirect URI: {cls.FYERS_REDIRECT_URI}")
        print(f"   API URL: {cls.FYERS_API_URL}")
        
        if cls.FYERS_ACCESS_TOKEN:
            print(f"   Access Token: {'*' * 30} (Set)")
        else:
            print(f"   Access Token: Not Set")
        
        print("\n📈 STRATEGY SETTINGS:")
        print(f"   Min Body %: {cls.MIN_BODY_PERCENT}%")
        print(f"   Min Body Ratio: {cls.MIN_BODY_RATIO}")
        print(f"   Risk:Reward: 1:{cls.RISK_REWARD_RATIO}")
        print(f"   Max Positions: {cls.MAX_POSITIONS}")
        print(f"   Capital per Trade: ₹{cls.CAPITAL_PER_TRADE:,.2f}")
        print(f"   Max Daily Loss: ₹{cls.MAX_DAILY_LOSS:,.2f}")
        print(f"   Risk per Trade: ₹{cls.RISK_PER_TRADE:,.2f}")
        
        print("\n⏰ TRADING HOURS:")
        print(f"   Scan Time: {cls.SCAN_TIME}")
        print(f"   Market Open: {cls.MARKET_OPEN_TIME}")
        print(f"   Market Close: {cls.MARKET_CLOSE_TIME}")
        
        print("\n📝 LOGGING:")
        print(f"   Log Level: {cls.LOG_LEVEL}")
        print(f"   Log File: {cls.LOG_FILE}")
        print(f"   Max Size: {cls.LOG_MAX_SIZE:,} bytes")
        print(f"   Backup Count: {cls.LOG_BACKUP_COUNT}")
        
        print("\n💾 DATABASE:")
        print(f"   Database Path: {cls.DB_PATH}")
        
        print("\n🔔 NOTIFICATIONS:")
        print(f"   Email: {'✅ Enabled' if cls.EMAIL_ENABLED else '❌ Disabled'}")
        print(f"   Telegram: {'✅ Enabled' if cls.TELEGRAM_ENABLED else '❌ Disabled'}")
        
        print("\n🌐 DASHBOARD:")
        print(f"   Port: {cls.DASHBOARD_PORT}")
        print(f"   Host: {cls.DASHBOARD_HOST}")
        print(f"   Username: {cls.DASHBOARD_USERNAME}")
        
        print("="*80 + "\n")
    
    @classmethod
    def get_summary(cls):
        """Get configuration summary as dictionary"""
        return {
            'environment': cls.ENVIRONMENT,
            'paper_trading': cls.PAPER_TRADING,
            'authenticated': bool(cls.FYERS_ACCESS_TOKEN),
            'strategy': {
                'min_body_percent': cls.MIN_BODY_PERCENT,
                'min_body_ratio': cls.MIN_BODY_RATIO,
                'risk_reward': cls.RISK_REWARD_RATIO,
                'max_positions': cls.MAX_POSITIONS,
                'capital_per_trade': cls.CAPITAL_PER_TRADE,
                'max_daily_loss': cls.MAX_DAILY_LOSS
            }
        }


def check_env_file():
    """Check if .env file exists"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("\n⚠️  WARNING: .env file not found!")
        print("\n📝 To create .env file:")
        print("   1. Copy .env.example to .env")
        print("   2. Edit .env with your FYERS API credentials")
        print("\nCommand: cp .env.example .env")
        return False
    
    return True


def main():
    """Main function to validate and display configuration"""
    print("\n🚀 FYERS 1Min Strategy - Configuration Validator")
    
    # Check if .env file exists
    if not check_env_file():
        sys.exit(1)
    
    # Validate configuration
    if not Config.validate():
        print("\n❌ Configuration validation failed!")
        print("   Please fix the errors above and try again.")
        sys.exit(1)
    
    # Display configuration
    Config.display_config(show_sensitive=False)
    
    print("✅ Configuration validated successfully!\n")
    
    # Next steps
    print("📋 NEXT STEPS:")
    print("   1. If not authenticated, login to FYERS")
    print("   2. Run daily scan: python strategy_runner.py --mode scan")
    print("   3. Start monitoring: python strategy_runner.py --mode monitor")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
