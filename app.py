#!/usr/bin/env python3
"""
Flask Web Application for Flash Arbitrage Bot
Provides web interface and API endpoints for bot management
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import asyncio
import threading
import json
import time
from arbitrage_engine import create_engine, get_engine
from arbitrage_wrapper import ArbitrageEngine as CppEngine
import os

app = Flask(__name__)
CORS(app)

# Global variables
bot_thread = None
bot_running = False
cpp_engine = None

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get bot status"""
    engine = get_engine()
    if engine:
        stats = engine.get_statistics()
        return jsonify({
            'status': 'running' if engine.running else 'stopped',
            'statistics': stats
        })
    return jsonify({'status': 'stopped', 'statistics': {}})

@app.route('/api/opportunities')
def get_opportunities():
    """Get current arbitrage opportunities"""
    engine = get_engine()
    if engine:
        opportunities = engine.get_opportunities()
        return jsonify({'opportunities': opportunities})
    return jsonify({'opportunities': []})

@app.route('/api/start', methods=['POST'])
def start_bot():
    """Start the arbitrage bot"""
    global bot_thread, bot_running, cpp_engine
    
    if bot_running:
        return jsonify({'error': 'Bot is already running'}), 400
    
    try:
        # Get configuration from request
        config = request.json or {}
        
        # Default configuration
        default_config = {
            'min_profit_threshold': 0.001,
            'max_gas_cost': 0.01,
            'max_slippage': 0.02,
            'max_position_size': 1000.0,
            'solana_rpc_url': 'https://api.mainnet-beta.solana.com'
        }
        default_config.update(config)
        
        # Create engines
        engine = create_engine(default_config)
        cpp_engine = CppEngine()
        
        # Start bot in separate thread
        def run_bot():
            global bot_running
            bot_running = True
            try:
                asyncio.run(engine.start())
            except Exception as e:
                print(f"Bot error: {e}")
            finally:
                bot_running = False
        
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.daemon = True
        bot_thread.start()
        
        return jsonify({'message': 'Bot started successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    """Stop the arbitrage bot"""
    global bot_running, cpp_engine
    
    engine = get_engine()
    if engine:
        asyncio.run(engine.stop())
    
    if cpp_engine:
        cpp_engine.stop()
    
    bot_running = False
    return jsonify({'message': 'Bot stopped successfully'})

@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    """Get or update bot configuration"""
    if request.method == 'GET':
        # Return current configuration
        engine = get_engine()
        if engine:
            return jsonify({
                'min_profit_threshold': engine.min_profit_threshold,
                'max_gas_cost': engine.max_gas_cost,
                'max_slippage': engine.max_slippage,
                'max_position_size': engine.max_position_size
            })
        return jsonify({})
    
    elif request.method == 'POST':
        # Update configuration
        config = request.json
        engine = get_engine()
        if engine:
            engine.min_profit_threshold = config.get('min_profit_threshold', engine.min_profit_threshold)
            engine.max_gas_cost = config.get('max_gas_cost', engine.max_gas_cost)
            engine.max_slippage = config.get('max_slippage', engine.max_slippage)
            engine.max_position_size = config.get('max_position_size', engine.max_position_size)
            
            return jsonify({'message': 'Configuration updated successfully'})
        
        return jsonify({'error': 'Bot not initialized'}), 400

@app.route('/api/cpp/status')
def get_cpp_status():
    """Get C++ engine status"""
    global cpp_engine
    if cpp_engine:
        try:
            total_profit, successful, failed, opportunities = cpp_engine.get_statistics()
            return jsonify({
                'total_profit': total_profit,
                'successful_trades': successful,
                'failed_trades': failed,
                'opportunities_count': opportunities,
                'success_rate': successful / max(1, successful + failed)
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'C++ engine not initialized'}), 400

@app.route('/api/cpp/opportunities')
def get_cpp_opportunities():
    """Get opportunities from C++ engine"""
    global cpp_engine
    if cpp_engine:
        try:
            opportunities = cpp_engine.get_all_opportunities()
            return jsonify({'opportunities': opportunities})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'opportunities': []})

@app.route('/api/cpp/execute/<int:index>', methods=['POST'])
def execute_cpp_trade(index):
    """Execute trade using C++ engine"""
    global cpp_engine
    if cpp_engine:
        try:
            success = cpp_engine.execute_trade(index)
            return jsonify({'success': success})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'C++ engine not initialized'}), 400

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'version': '1.0.0'
    })

@app.route('/download/<filename>')
def download_file(filename):
    """Download files (like .so files)"""
    try:
        return send_from_directory('.', filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    # Ensure templates directory exists
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("Starting Flash Arbitrage Bot Web Interface...")
    print("Dashboard will be available at: http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

