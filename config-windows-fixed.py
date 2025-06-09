#!/usr/bin/env python3
"""
Configuration module for Flash Arbitrage Bot
Windows-compatible with proper encoding handling
"""

import os
import json
from pathlib import Path

# Configuration file path
CONFIG_FILE = Path(__file__).parent / 'bot_config.json'

# Default configuration
DEFAULT_CONFIG = {
    'wallet_address': '68Jxdxbe2GC86GoJGBwNeaRAqun1ttyEEntUSnBsokMK',
    'min_profit_threshold': 0.0005,  # 0.05% minimum profit
    'max_gas_cost': 0.02,            # 0.02 SOL max gas
    'max_slippage': 0.03,            # 3% max slippage
    'max_position_size': 5000.0,     # Max 5000 SOL position
    'solana_rpc_url': 'https://api.mainnet-beta.solana.com',
    'exchanges': {
        'raydium': True,
        'orca': True,
        'serum': True,
        'jupiter': True
    },
    'risk_management': {
        'max_daily_loss': 10.0,      # Max 10 SOL daily loss
        'stop_loss_threshold': 0.05,  # 5% stop loss
        'position_size_limit': 0.1    # 10% of balance max
    }
}

def load_config():
    """Load configuration from file with proper encoding"""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged_config = DEFAULT_CONFIG.copy()
                merged_config.update(config)
                return merged_config
        else:
            # Create default config file
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
    except Exception as e:
        print(f"Warning: Could not load config file: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save configuration to file with proper encoding"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Warning: Could not save config file: {e}")
        return False

def get_config():
    """Get current configuration"""
    return load_config()

def get_wallet_address():
    """Get the configured wallet address"""
    config = load_config()
    return config.get('wallet_address', DEFAULT_CONFIG['wallet_address'])

def update_wallet_address(new_address):
    """Update the wallet address"""
    try:
        config = load_config()
        config['wallet_address'] = new_address
        return save_config(config)
    except Exception as e:
        print(f"Error updating wallet address: {e}")
        return False

def update_exchange_api_key(exchange, api_key):
    """Update API key for an exchange"""
    try:
        config = load_config()
        if 'api_keys' not in config:
            config['api_keys'] = {}
        config['api_keys'][exchange] = api_key
        return save_config(config)
    except Exception as e:
        print(f"Error updating API key: {e}")
        return False

def get_exchange_status():
    """Get exchange connection status"""
    config = load_config()
    exchanges = config.get('exchanges', {})
    
    status = {}
    for exchange, enabled in exchanges.items():
        status[exchange] = {
            'enabled': enabled,
            'connected': enabled,  # Mock connection status
            'latency': '< 1ms' if enabled else 'N/A'
        }
    
    return status

def validate_config():
    """Validate configuration values"""
    config = load_config()
    errors = []
    
    # Validate wallet address
    wallet = config.get('wallet_address', '')
    if not wallet or len(wallet) < 32:
        errors.append("Invalid wallet address")
    
    # Validate profit threshold
    profit_threshold = config.get('min_profit_threshold', 0)
    if profit_threshold <= 0 or profit_threshold > 1:
        errors.append("Profit threshold must be between 0 and 1")
    
    # Validate position size
    position_size = config.get('max_position_size', 0)
    if position_size <= 0:
        errors.append("Position size must be greater than 0")
    
    return len(errors) == 0, errors

if __name__ == "__main__":
    # Test configuration
    print("Flash Arbitrage Bot Configuration")
    print("=" * 40)
    
    config = get_config()
    print(f"Wallet: {get_wallet_address()}")
    print(f"Min Profit: {config['min_profit_threshold']*100:.3f}%")
    print(f"Max Position: {config['max_position_size']} SOL")
    print(f"Max Gas: {config['max_gas_cost']} SOL")
    
    valid, errors = validate_config()
    if valid:
        print("✅ Configuration is valid")
    else:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"  - {error}")
    
    print(f"Config file: {CONFIG_FILE}")
    print("Exchange status:")
    for exchange, status in get_exchange_status().items():
        print(f"  {exchange}: {'✅' if status['enabled'] else '❌'}")

