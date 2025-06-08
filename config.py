#!/usr/bin/env python3
"""
Configuration file for Flash Arbitrage Bot
Contains wallet addresses and API configurations
"""

# Solana Wallet Configuration
SOLANA_WALLET_ADDRESS = "68Jxdxbe2GC86GoJGBwNeaRAqun1ttyEEntUSnBsokMK"

# Bot Configuration
BOT_CONFIG = {
    # Wallet Settings
    'wallet_address': SOLANA_WALLET_ADDRESS,
    'private_key': None,  # Set this for automated trading
    
    # Profit Settings (Optimized for unlimited profit potential)
    'min_profit_threshold': 0.0005,  # 0.05% minimum profit (very low for max opportunities)
    'max_gas_cost': 0.02,            # 0.02 SOL max gas cost
    'max_slippage': 0.03,            # 3% max slippage
    'max_position_size': 5000.0,     # Increased position size for higher profits
    
    # Risk Management
    'max_daily_trades': 1000,        # Maximum trades per day
    'max_daily_loss': 10.0,          # Maximum daily loss in SOL
    'stop_loss_percentage': 0.05,    # 5% stop loss
    
    # Exchange Settings
    'exchanges': {
        'raydium': {
            'enabled': True,
            'api_key': None,  # Set your Raydium API key
            'priority': 1
        },
        'orca': {
            'enabled': True,
            'api_key': None,  # Set your Orca API key
            'priority': 2
        },
        'serum': {
            'enabled': True,
            'api_key': None,  # Set your Serum API key
            'priority': 3
        },
        'jupiter': {
            'enabled': True,
            'api_key': None,  # Set your Jupiter API key
            'priority': 4
        }
    },
    
    # Solana RPC Configuration
    'solana_rpc_url': 'https://api.mainnet-beta.solana.com',
    'solana_ws_url': 'wss://api.mainnet-beta.solana.com',
    
    # Advanced Settings
    'enable_flash_loans': True,
    'enable_cpp_engine': True,
    'log_level': 'INFO',
    'update_interval': 0.1,  # 100ms update interval for maximum speed
    
    # Profit Optimization
    'compound_profits': True,
    'reinvest_percentage': 0.8,  # Reinvest 80% of profits
    'reserve_percentage': 0.2,   # Keep 20% as reserve
}

# Multi-Chain Wallet Addresses (for future expansion)
MULTI_CHAIN_WALLETS = {
    'solana': '68Jxdxbe2GC86GoJGBwNeaRAqun1ttyEEntUSnBsokMK',
    'ethereum': None,  # Add Ethereum wallet if needed
    'polygon': None,   # Add Polygon wallet if needed
    'bsc': None,       # Add BSC wallet if needed
    'arbitrum': None   # Add Arbitrum wallet if needed
}

# GitHub Integration Settings
GITHUB_CONFIG = {
    'repository': 'LimitlessJacko/Flash-arb-anchor',
    'auto_update': True,
    'backup_frequency': 'daily'
}

def get_config():
    """Get the complete bot configuration"""
    return BOT_CONFIG

def update_wallet_address(new_address):
    """Update the wallet address"""
    global BOT_CONFIG
    BOT_CONFIG['wallet_address'] = new_address
    return True

def update_exchange_api_key(exchange, api_key):
    """Update exchange API key"""
    global BOT_CONFIG
    if exchange in BOT_CONFIG['exchanges']:
        BOT_CONFIG['exchanges'][exchange]['api_key'] = api_key
        return True
    return False

def get_wallet_address():
    """Get the current wallet address"""
    return BOT_CONFIG['wallet_address']

if __name__ == "__main__":
    print("Flash Arbitrage Bot Configuration")
    print("=================================")
    print(f"Wallet Address: {get_wallet_address()}")
    print(f"Min Profit Threshold: {BOT_CONFIG['min_profit_threshold']*100:.3f}%")
    print(f"Max Position Size: {BOT_CONFIG['max_position_size']} SOL")
    print(f"Enabled Exchanges: {[ex for ex, config in BOT_CONFIG['exchanges'].items() if config['enabled']]}")
    print(f"GitHub Repository: {GITHUB_CONFIG['repository']}")

