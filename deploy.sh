#!/bin/bash

# Flash Arbitrage Bot Deployment Script
# This script sets up and deploys the flash arbitrage bot

echo "🚀 Flash Arbitrage Bot Deployment Script"
echo "========================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .so file exists
if [ ! -f "libarbitrage_engine.so" ]; then
    echo "⚠️  Warning: libarbitrage_engine.so not found. C++ engine will not be available."
    echo "   You can still use the Python engine."
fi

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Create logs directory
mkdir -p logs

echo "✅ Setup complete!"
echo ""
echo "🎯 To start the bot:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run the application: python app.py"
echo "   3. Open browser to: http://localhost:5000"
echo ""
echo "🔧 Configuration:"
echo "   - Edit configuration through the web interface"
echo "   - Or modify the config in arbitrage_engine.py"
echo ""
echo "📊 Features:"
echo "   - Real-time arbitrage opportunity detection"
echo "   - Web-based dashboard with live statistics"
echo "   - C++ engine integration (.so file)"
echo "   - Multi-exchange support (Raydium, Orca, Serum, Jupiter)"
echo "   - Risk management and profit optimization"
echo ""

# Check if we should start the bot automatically
read -p "🤖 Would you like to start the bot now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Starting Flash Arbitrage Bot..."
    python app.py
fi

