#!/bin/bash

# FYERS 1Min Strategy - Quick Setup Script
# This script sets up the environment for the trading strategy

set -e  # Exit on error

echo ""
echo "=================================="
echo "🚀 FYERS 1Min Strategy Setup"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data
mkdir -p logs
mkdir -p backups
mkdir -p reports
print_success "Directories created"

# Create .env file from template
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        print_success ".env file created"
        print_warning "Please edit .env with your FYERS API credentials"
    else
        print_error ".env.example not found"
        echo "Creating basic .env file..."
        cat > .env << 'EOF'
# FYERS API Credentials
FYERS_APP_ID=your-app-id-here
FYERS_APP_SECRET=your-app-secret-here
FYERS_REDIRECT_URI=http://localhost:5000/callback
FYERS_API_URL=https://api-t1.fyers.in/api/v3

# Tokens (auto-generated)
FYERS_ACCESS_TOKEN=
FYERS_REFRESH_TOKEN=
TOKEN_EXPIRY=

# Strategy Configuration
MIN_BODY_PERCENT=0.8
MIN_BODY_RATIO=0.75
RISK_REWARD_RATIO=2.0
MAX_POSITIONS=5
CAPITAL_PER_TRADE=50000
MAX_DAILY_LOSS=5000

# Trading Hours
MARKET_OPEN_TIME=09:15
MARKET_CLOSE_TIME=15:30

# Environment
ENVIRONMENT=development
PAPER_TRADING=true
DEBUG=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/strategy.log

# Database
DB_PATH=./data/trades.db
EOF
        print_success "Basic .env file created"
    fi
else
    print_warning ".env file already exists, skipping..."
fi

echo ""

# Set proper file permissions for security
echo "🔒 Setting secure file permissions..."
if [ -f .env ]; then
    chmod 600 .env
    print_success "Set .env permissions to 600 (read/write for owner only)"
fi

if [ -f .fyers_tokens.json ]; then
    chmod 600 .fyers_tokens.json
    print_success "Set token file permissions to 600"
fi

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo ""
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Environment Variables
.env
.env.local
.env.*.local

# Authentication Tokens
.fyers_tokens.json

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*

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
.venv/

# Reports
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

# Compiled
*.pyc
dist/
build/
*.egg-info/
EOF
    print_success ".gitignore created"
else
    print_warning ".gitignore already exists, skipping..."
fi

echo ""

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    print_error "Python is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

print_success "Python found: $PYTHON_CMD"

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
print_success "Python version: $PYTHON_VERSION"

echo ""

# Create requirements.txt if it doesn't exist
if [ ! -f requirements.txt ]; then
    echo "📝 Creating requirements.txt..."
    cat > requirements.txt << 'EOF'
# Core Dependencies
python-dotenv==1.0.0
requests==2.31.0

# Optional: Data Analysis
# pandas==2.1.0
# numpy==1.24.3

# Optional: Database
# sqlalchemy==2.0.20

# Optional: Logging
# colorlog==6.7.0

# Optional: Web Dashboard
# flask==3.0.0
# flask-cors==4.0.0

# Utilities
python-dateutil==2.8.2
EOF
    print_success "requirements.txt created"
fi

# Install Python dependencies
echo ""
read -p "📦 Install Python dependencies? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing dependencies..."
    $PYTHON_CMD -m pip install -r requirements.txt
    print_success "Dependencies installed"
else
    print_warning "Skipped dependency installation"
    echo "To install later, run: pip install -r requirements.txt"
fi

echo ""

# Validate configuration
if [ -f config.py ]; then
    echo "🔍 Validating configuration..."
    $PYTHON_CMD config.py
else
    print_warning "config.py not found, skipping validation"
fi

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. Get FYERS API Credentials:"
echo "   → Visit: https://myapi.fyers.in/dashboard"
echo "   → Create a new app"
echo "   → Get your App ID and App Secret"
echo ""
echo "2. Configure .env file:"
echo "   → Edit .env with your credentials"
echo "   → Command: nano .env"
echo ""
echo "3. Authenticate with FYERS:"
echo "   → Use Claude: 'Login to FYERS and authenticate'"
echo "   → Or run: python auth_manager.py --status"
echo ""
echo "4. Run the strategy:"
echo "   → Daily scan: python strategy_runner.py --mode scan"
echo "   → Monitor: python strategy_runner.py --mode monitor"
echo ""
echo "📚 Documentation:"
echo "   → See env_setup_guide.md for detailed instructions"
echo "   → See execution_workflow.md for trading workflow"
echo ""
echo "=================================="
echo ""
