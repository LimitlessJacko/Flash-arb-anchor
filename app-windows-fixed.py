#!/usr/bin/env python3
"""
Windows-Compatible Flask Web Application for Flash Arbitrage Bot
Fixed UTF-8 encoding issues and binary file handling
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
    input("Press Enter to exit...")
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
    try:
        return render_template('index.html')
    except Exception as e:
        # Fallback HTML if template is missing
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Flash Arbitrage Bot - Windows</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: white; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .card {{ background: #16213e; padding: 20px; margin: 20px 0; border-radius: 10px; }}
                .btn {{ background: #7c3aed; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
                .btn:hover {{ background: #6d28d9; }}
                .status {{ color: #10b981; }}
                .error {{ color: #ef4444; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Flash Arbitrage Bot - Windows Version</h1>
                <div class="card">
                    <h2>Bot Status</h2>
                    <p class="status">✅ Server Running Successfully</p>
                    <p><strong>Wallet:</strong> {get_wallet_address()}</p>
                    <p><strong>Mode:</strong> Windows Demo Mode</p>
                </div>
                <div class="card">
                    <h2>Quick Actions</h2>
                    <button class="btn" onclick="startBot()">Start Bot</button>
                    <button class="btn" onclick="stopBot()">Stop Bot</button>
                    <button class="btn" onclick="viewStats()">View Stats</button>
                </div>
                <div class="card">
                    <h2>API Endpoints</h2>
                    <p>• <a href="/api/status" style="color: #7c3aed;">/api/status</a> - Bot status</p>
                    <p>• <a href="/api/opportunities" style="color: #7c3aed;">/api/opportunities</a> - Live opportunities</p>
                    <p>• <a href="/api/wallet" style="color: #7c3aed;">/api/wallet</a> - Wallet info</p>
                    <p>• <a href="/api/health" style="color: #7c3aed;">/api/health</a> - Health check</p>
                </div>
            </div>
            <script>
                function startBot() {{
                    fetch('/api/start', {{method: 'POST'}})
                        .then(r => r.json())
                        .then(d => alert(d.message || d.error));
                }}
                function stopBot() {{
                    fetch('/api/stop', {{method: 'POST'}})
                        .then(r => r.json())
                        .then(d => alert(d.message || d.error));
                }}
                function viewStats() {{
                    fetch('/api/status')
                        .then(r => r.json())
                        .then(d => alert(JSON.stringify(d, null, 2)));
                }}
            </script>
        </body>
        </html>
        """

@app.route('/api/status')
def get_status():
    """Get bot status"""
    global mock_stats
    return jsonify({
        'status': 'running' if bot_running else 'stopped',
        'platform': 'Windows',
        'mode': 'demo',
        'statistics': mock_stats,
        'wallet': get_wallet_address(),
        'timestamp': time.time()
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
            'confidence': 85,
            'timestamp': time.time()
        },
        {
            'token_pair': 'RAY/SOL',
            'exchange_a': 'Serum',
            'exchange_b': 'Jupiter',
            'price_diff': 0.0089,
            'profit_potential': 0.0018,
            'net_profit': 0.0156,
            'confidence': 78,
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
        bot_running = False
        return jsonify({'error': f'Failed to start bot: {str(e)}'}), 500

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
            'max_position_size': config.get('max_position_size', 5000.0),
            'wallet_address': get_wallet_address()
        })
    
    elif request.method == 'POST':
        try:
            config_data = request.json
            # In a full implementation, this would update the actual config
            return jsonify({'message': 'Configuration updated successfully (Windows demo mode)'})
        except Exception as e:
            return jsonify({'error': f'Failed to update config: {str(e)}'}), 400

@app.route('/api/wallet')
def get_wallet_info():
    """Get wallet information"""
    return jsonify({
        'address': get_wallet_address(),
        'configured': True,
        'platform': 'Windows'
    })

@app.route('/api/wallet', methods=['POST'])
def update_wallet():
    """Update wallet address"""
    try:
        data = request.json
        new_address = data.get('address')
        
        if new_address:
            success = update_wallet_address(new_address)
            if success:
                return jsonify({'message': 'Wallet address updated successfully'})
            else:
                return jsonify({'error': 'Failed to update wallet address'}), 400
        
        return jsonify({'error': 'No wallet address provided'}), 400
    except Exception as e:
        return jsonify({'error': f'Error updating wallet: {str(e)}'}), 400

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'platform': 'Windows',
        'mode': 'demo',
        'timestamp': time.time(),
        'version': '1.0.0-windows-fixed',
        'encoding': 'utf-8-safe'
    })

@app.route('/download/<filename>')
def download_file(filename):
    """Download files (safe binary handling)"""
    try:
        # Safe file handling for Windows
        file_path = os.path.join(current_dir, filename)
        if os.path.exists(file_path):
            return send_from_directory(str(current_dir), filename, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

@app.route('/download/so')
def download_so_file():
    """Download the .so file with proper binary handling"""
    try:
        so_file = 'libarbitrage_engine.so'
        file_path = os.path.join(current_dir, so_file)
        
        if os.path.exists(file_path):
            # Use binary mode to avoid UTF-8 encoding issues
            return send_from_directory(
                str(current_dir), 
                so_file, 
                as_attachment=True,
                mimetype='application/octet-stream'
            )
        else:
            return jsonify({
                'error': 'Shared library file not found',
                'note': 'The .so file is for Linux systems. Windows version uses demo mode.'
            }), 404
    except Exception as e:
        return jsonify({'error': f'Error downloading .so file: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'details': str(error)}), 500

@app.errorhandler(UnicodeDecodeError)
def handle_unicode_error(error):
    return jsonify({
        'error': 'UTF-8 encoding error handled',
        'message': 'Binary file access attempted - using safe mode',
        'details': str(error)
    }), 400

if __name__ == '__main__':
    # Ensure directories exist
    try:
        os.makedirs('templates', exist_ok=True)
        os.makedirs('static', exist_ok=True)
    except Exception as e:
        print(f"Warning: Could not create directories: {e}")
    
    print("=" * 60)
    print("Flash Arbitrage Bot - Windows Version (UTF-8 Fixed)")
    print("=" * 60)
    print(f"Configured for wallet: {get_wallet_address()}")
    print("Platform: Windows (Demo Mode)")
    print("Dashboard: http://localhost:5000")
    print("Repository: https://github.com/LimitlessJacko/Flash-arb-anchor")
    print("Website: https://rfasanfy.manus.space")
    print("=" * 60)
    print()
    print("✅ UTF-8 encoding issues fixed")
    print("✅ Binary file handling improved")
    print("✅ Windows compatibility enhanced")
    print()
    print("Note: This is a Windows-compatible demo version.")
    print("For full functionality, use the Linux version or visit the website.")
    print()
    
    try:
        # Use 127.0.0.1 instead of 0.0.0.0 for Windows compatibility
        app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
    except Exception as e:
        print(f"Error starting server: {e}")
        print()
        print("Troubleshooting steps:")
        print("1. Try running as administrator")
        print("2. Check if port 5000 is available")
        print("3. Try a different port: python app-windows-fixed.py")
        print("4. Check Windows Firewall settings")
        print()
        input("Press Enter to exit...")

