#!/usr/bin/env python3
"""
Windows-Compatible Flask Web Application for Flash Arbitrage Bot
Simplified version with better Windows compatibility
"""

import sys
import os
import json
import time
import threading
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from flask import Flask, render_template, jsonify, request, send_from_directory
    from flask_cors import CORS
except ImportError as e:
    print(f"Error importing Flask: {e}")
    print("Please run: pip install flask flask-cors")
    sys.exit(1)

try:
    from config import get_config, get_wallet_address, update_wallet_address
except ImportError:
    print("Warning: config.py not found, using default configuration")
    def get_config():
        return {
            'wallet_address': '68Jxdxbe2GC86GoJGBwNeaRAqun1ttyEEntUSnBsokMK',
            'min_profit_threshold': 0.0005,
            'max_gas_cost': 0.02,
            'max_slippage': 0.03,
            'max_position_size': 5000.0
        }
    
    def get_wallet_address():
        return '68Jxdxbe2GC86GoJGBwNeaRAqun1ttyEEntUSnBsokMK'
    
    def update_wallet_address(address):
        return True

app = Flask(__name__)
CORS(app)

# Global variables
bot_running = False
mock_stats = {
    'total_profit': 0.0,
    'successful_trades': 0,
    'failed_trades': 0,
    'opportunities_count': 0,
    'success_rate': 0.0
}

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get bot status"""
    global mock_stats
    return jsonify({
        'status': 'running' if bot_running else 'stopped',
        'statistics': mock_stats
    })

@app.route('/api/opportunities')
def get_opportunities():
    """Get current arbitrage opportunities (mock data for Windows)"""
    mock_opportunities = [
        {
            'token_pair': 'SOL/USDC',
            'exchange_a': 'Raydium',
            'exchange_b': 'Orca',
            'price_diff': 0.0125,
            'profit_potential': 0.0025,
            'net_profit': 0.0234,
            'confidence': 0.85,
            'timestamp': time.time()
        },
        {
            'token_pair': 'RAY/SOL',
            'exchange_a': 'Serum',
            'exchange_b': 'Jupiter',
            'price_diff': 0.0089,
            'profit_potential': 0.0018,
            'net_profit': 0.0156,
            'confidence': 0.78,
            'timestamp': time.time()
        }
    ]
    return jsonify({'opportunities': mock_opportunities})

@app.route('/api/start', methods=['POST'])
def start_bot():
    """Start the arbitrage bot (mock for Windows)"""
    global bot_running, mock_stats
    
    if bot_running:
        return jsonify({'error': 'Bot is already running'}), 400
    
    try:
        bot_running = True
        
        # Start mock profit generation
        def mock_trading():
            global mock_stats
            while bot_running:
                time.sleep(5)  # Update every 5 seconds
                if bot_running:
                    mock_stats['total_profit'] += 0.001  # Small profit increment
                    mock_stats['successful_trades'] += 1
                    mock_stats['opportunities_count'] = 5
                    total_trades = mock_stats['successful_trades'] + mock_stats['failed_trades']
                    mock_stats['success_rate'] = mock_stats['successful_trades'] / max(1, total_trades)
        
        trading_thread = threading.Thread(target=mock_trading)
        trading_thread.daemon = True
        trading_thread.start()
        
        return jsonify({'message': 'Bot started successfully (Windows demo mode)'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    """Stop the arbitrage bot"""
    global bot_running
    bot_running = False
    return jsonify({'message': 'Bot stopped successfully'})

@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    """Get or update bot configuration"""
    if request.method == 'GET':
        config = get_config()
        return jsonify({
            'min_profit_threshold': config.get('min_profit_threshold', 0.0005),
            'max_gas_cost': config.get('max_gas_cost', 0.02),
            'max_slippage': config.get('max_slippage', 0.03),
            'max_position_size': config.get('max_position_size', 5000.0)
        })
    
    elif request.method == 'POST':
        config_data = request.json
        # In a full implementation, this would update the actual config
        return jsonify({'message': 'Configuration updated successfully (Windows demo mode)'})

@app.route('/api/wallet')
def get_wallet_info():
    """Get wallet information"""
    return jsonify({
        'address': get_wallet_address(),
        'configured': True
    })

@app.route('/api/wallet', methods=['POST'])
def update_wallet():
    """Update wallet address"""
    data = request.json
    new_address = data.get('address')
    
    if new_address:
        success = update_wallet_address(new_address)
        if success:
            return jsonify({'message': 'Wallet address updated successfully'})
        else:
            return jsonify({'error': 'Failed to update wallet address'}), 400
    
    return jsonify({'error': 'No wallet address provided'}), 400

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'platform': 'Windows',
        'mode': 'demo',
        'timestamp': time.time(),
        'version': '1.0.0-windows'
    })

@app.route('/download/<filename>')
def download_file(filename):
    """Download files"""
    try:
        return send_from_directory('.', filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Ensure templates and static directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("=" * 50)
    print("Flash Arbitrage Bot - Windows Version")
    print("=" * 50)
    print(f"Configured for wallet: {get_wallet_address()}")
    print("Platform: Windows (Demo Mode)")
    print("Dashboard: http://localhost:5000")
    print("Repository: https://github.com/LimitlessJacko/Flash-arb-anchor")
    print("=" * 50)
    print()
    print("Note: This is a Windows-compatible demo version.")
    print("For full functionality, use the Linux version.")
    print()
    
    try:
        app.run(host='127.0.0.1', port=5000, debug=False)
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Try running as administrator or check if port 5000 is available.")
        input("Press Enter to exit...")

