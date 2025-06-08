#!/usr/bin/env python3
"""
Flash Arbitrage Bot - Enhanced Solana Arbitrage Engine
Based on the original implementation with unlimited profit potential
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from decimal import Decimal
import websockets
import aiohttp
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solana.publickey import PublicKey
from solana.transaction import Transaction
import numpy as np

# Import configuration
from config import get_config, get_wallet_address

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ArbitrageOpportunity:
    """Represents a flash arbitrage opportunity"""
    token_pair: str
    exchange_a: str
    exchange_b: str
    price_a: float
    price_b: float
    price_diff: float
    profit_potential: float
    volume: float
    gas_cost: float
    net_profit: float
    timestamp: float
    confidence: float
    risk_score: float

@dataclass
class MarketData:
    """Market data from exchanges"""
    exchange: str
    token_pair: str
    bid_price: float
    ask_price: float
    volume: float
    timestamp: float
    liquidity: float

class FlashArbitrageEngine:
    """Enhanced Flash Arbitrage Engine with unlimited profit potential"""
    
    def __init__(self, config: Dict = None):
        # Use provided config or load from config.py
        if config is None:
            config = get_config()
        
        self.config = config
        self.wallet_address = get_wallet_address()
        self.opportunities = []
        self.market_data = {}
        self.running = False
        self.total_profit = 0.0
        self.successful_trades = 0
        self.failed_trades = 0
        
        logger.info(f"Initializing Flash Arbitrage Engine for wallet: {self.wallet_address}")
        
        # Enhanced configuration for unlimited profit
        self.min_profit_threshold = config.get('min_profit_threshold', 0.0005)  # 0.05% minimum
        self.max_gas_cost = config.get('max_gas_cost', 0.02)  # 0.02 SOL max gas
        self.max_slippage = config.get('max_slippage', 0.03)  # 3% max slippage
        self.max_position_size = config.get('max_position_size', 5000.0)  # Max position size
        
        # Solana RPC client
        self.solana_client = AsyncClient(
            config.get('solana_rpc_url', 'https://api.mainnet-beta.solana.com')
        )
        
        # Exchange configurations
        self.exchanges = {
            'raydium': {
                'name': 'Raydium',
                'api_url': 'https://api.raydium.io/v2',
                'websocket_url': 'wss://api.raydium.io/v2/ws',
                'fee': 0.0025  # 0.25%
            },
            'orca': {
                'name': 'Orca',
                'api_url': 'https://api.orca.so/v1',
                'websocket_url': 'wss://api.orca.so/v1/ws',
                'fee': 0.003   # 0.3%
            },
            'serum': {
                'name': 'Serum',
                'api_url': 'https://api.projectserum.com/v1',
                'websocket_url': 'wss://api.projectserum.com/v1/ws',
                'fee': 0.0022  # 0.22%
            },
            'jupiter': {
                'name': 'Jupiter',
                'api_url': 'https://quote-api.jup.ag/v6',
                'websocket_url': 'wss://quote-api.jup.ag/v6/ws',
                'fee': 0.001   # 0.1%
            }
        }
        
        # Token pairs to monitor
        self.token_pairs = [
            'SOL/USDC', 'SOL/USDT', 'RAY/SOL', 'SRM/SOL',
            'ORCA/SOL', 'MNGO/SOL', 'STEP/SOL', 'COPE/SOL',
            'MEDIA/SOL', 'ROPE/SOL', 'TULIP/SOL', 'SLIM/SOL'
        ]
    
    async def start(self):
        """Start the arbitrage engine"""
        logger.info("Starting Flash Arbitrage Engine...")
        self.running = True
        
        # Start market data collection
        tasks = []
        for exchange in self.exchanges.keys():
            tasks.append(self.collect_market_data(exchange))
        
        # Start opportunity scanning
        tasks.append(self.scan_opportunities_loop())
        
        # Start trade execution
        tasks.append(self.execute_trades_loop())
        
        await asyncio.gather(*tasks)
    
    async def collect_market_data(self, exchange: str):
        """Collect real-time market data from exchange"""
        while self.running:
            try:
                exchange_config = self.exchanges[exchange]
                
                # Simulate market data collection (replace with real API calls)
                for pair in self.token_pairs:
                    # Generate realistic market data with some randomness
                    base_price = self.get_base_price(pair)
                    spread = base_price * 0.001  # 0.1% spread
                    
                    bid_price = base_price - (spread / 2) + np.random.normal(0, spread * 0.1)
                    ask_price = base_price + (spread / 2) + np.random.normal(0, spread * 0.1)
                    volume = np.random.uniform(1000, 10000)
                    liquidity = np.random.uniform(50000, 500000)
                    
                    market_data = MarketData(
                        exchange=exchange,
                        token_pair=pair,
                        bid_price=max(0, bid_price),
                        ask_price=max(bid_price, ask_price),
                        volume=volume,
                        timestamp=time.time(),
                        liquidity=liquidity
                    )
                    
                    # Store market data
                    key = f"{exchange}:{pair}"
                    self.market_data[key] = market_data
                
                await asyncio.sleep(0.1)  # 100ms update interval
                
            except Exception as e:
                logger.error(f"Error collecting market data from {exchange}: {e}")
                await asyncio.sleep(1)
    
    def get_base_price(self, pair: str) -> float:
        """Get base price for token pair"""
        base_prices = {
            'SOL/USDC': 100.0,
            'SOL/USDT': 100.0,
            'RAY/SOL': 0.5,
            'SRM/SOL': 0.1,
            'ORCA/SOL': 0.3,
            'MNGO/SOL': 0.05,
            'STEP/SOL': 0.02,
            'COPE/SOL': 0.01,
            'MEDIA/SOL': 0.15,
            'ROPE/SOL': 0.001,
            'TULIP/SOL': 0.08,
            'SLIM/SOL': 0.003
        }
        return base_prices.get(pair, 1.0)
    
    async def scan_opportunities_loop(self):
        """Continuously scan for arbitrage opportunities"""
        while self.running:
            try:
                await self.scan_opportunities()
                await asyncio.sleep(0.05)  # 50ms scan interval
            except Exception as e:
                logger.error(f"Error scanning opportunities: {e}")
                await asyncio.sleep(0.1)
    
    async def scan_opportunities(self):
        """Scan for arbitrage opportunities across exchanges"""
        opportunities = []
        
        # Group market data by token pair
        pairs_data = {}
        for key, data in self.market_data.items():
            pair = data.token_pair
            if pair not in pairs_data:
                pairs_data[pair] = []
            pairs_data[pair].append(data)
        
        # Find arbitrage opportunities
        for pair, data_list in pairs_data.items():
            if len(data_list) < 2:
                continue
            
            # Compare all exchange combinations
            for i in range(len(data_list)):
                for j in range(i + 1, len(data_list)):
                    data_a = data_list[i]
                    data_b = data_list[j]
                    
                    # Calculate potential profit
                    if data_a.ask_price < data_b.bid_price:
                        # Buy on A, sell on B
                        price_diff = data_b.bid_price - data_a.ask_price
                        profit_pct = price_diff / data_a.ask_price
                        
                        if profit_pct > self.min_profit_threshold:
                            opportunity = await self.create_opportunity(
                                data_a, data_b, price_diff, profit_pct, 'buy_a_sell_b'
                            )
                            if opportunity:
                                opportunities.append(opportunity)
                    
                    elif data_b.ask_price < data_a.bid_price:
                        # Buy on B, sell on A
                        price_diff = data_a.bid_price - data_b.ask_price
                        profit_pct = price_diff / data_b.ask_price
                        
                        if profit_pct > self.min_profit_threshold:
                            opportunity = await self.create_opportunity(
                                data_b, data_a, price_diff, profit_pct, 'buy_b_sell_a'
                            )
                            if opportunity:
                                opportunities.append(opportunity)
        
        # Sort opportunities by profit potential
        opportunities.sort(key=lambda x: x.net_profit, reverse=True)
        self.opportunities = opportunities[:50]  # Keep top 50 opportunities
    
    async def create_opportunity(self, buy_data: MarketData, sell_data: MarketData, 
                               price_diff: float, profit_pct: float, direction: str) -> Optional[ArbitrageOpportunity]:
        """Create an arbitrage opportunity object"""
        try:
            # Calculate optimal volume
            max_volume = min(buy_data.volume, sell_data.volume)
            optimal_volume = min(max_volume, self.max_position_size)
            
            # Calculate costs
            buy_fee = optimal_volume * buy_data.ask_price * self.exchanges[buy_data.exchange]['fee']
            sell_fee = optimal_volume * sell_data.bid_price * self.exchanges[sell_data.exchange]['fee']
            gas_cost = self.estimate_gas_cost(optimal_volume)
            
            # Calculate net profit
            gross_profit = optimal_volume * price_diff
            total_costs = buy_fee + sell_fee + gas_cost
            net_profit = gross_profit - total_costs
            
            # Risk assessment
            confidence = self.calculate_confidence(buy_data, sell_data)
            risk_score = self.calculate_risk_score(buy_data, sell_data, optimal_volume)
            
            if net_profit > 0 and gas_cost < self.max_gas_cost:
                return ArbitrageOpportunity(
                    token_pair=buy_data.token_pair,
                    exchange_a=buy_data.exchange,
                    exchange_b=sell_data.exchange,
                    price_a=buy_data.ask_price,
                    price_b=sell_data.bid_price,
                    price_diff=price_diff,
                    profit_potential=profit_pct,
                    volume=optimal_volume,
                    gas_cost=gas_cost,
                    net_profit=net_profit,
                    timestamp=time.time(),
                    confidence=confidence,
                    risk_score=risk_score
                )
        except Exception as e:
            logger.error(f"Error creating opportunity: {e}")
        
        return None
    
    def estimate_gas_cost(self, volume: float) -> float:
        """Estimate gas cost for the arbitrage transaction"""
        # Base gas cost + volume-dependent cost
        base_cost = 0.001  # 0.001 SOL base cost
        volume_cost = volume * 0.00001  # 0.00001 SOL per unit volume
        return base_cost + volume_cost
    
    def calculate_confidence(self, buy_data: MarketData, sell_data: MarketData) -> float:
        """Calculate confidence score for the opportunity"""
        # Factors: liquidity, volume, price stability
        liquidity_score = min(1.0, (buy_data.liquidity + sell_data.liquidity) / 100000)
        volume_score = min(1.0, (buy_data.volume + sell_data.volume) / 10000)
        
        # Time freshness
        current_time = time.time()
        age_a = current_time - buy_data.timestamp
        age_b = current_time - sell_data.timestamp
        freshness_score = max(0, 1.0 - max(age_a, age_b) / 10.0)  # 10 second decay
        
        return (liquidity_score + volume_score + freshness_score) / 3.0
    
    def calculate_risk_score(self, buy_data: MarketData, sell_data: MarketData, volume: float) -> float:
        """Calculate risk score for the opportunity"""
        # Lower score = lower risk
        
        # Volume risk (higher volume = higher risk)
        volume_risk = min(1.0, volume / self.max_position_size)
        
        # Liquidity risk (lower liquidity = higher risk)
        min_liquidity = min(buy_data.liquidity, sell_data.liquidity)
        liquidity_risk = max(0, 1.0 - min_liquidity / 50000)
        
        # Exchange risk (some exchanges are riskier)
        exchange_risk = 0.1  # Base exchange risk
        
        return (volume_risk + liquidity_risk + exchange_risk) / 3.0
    
    async def execute_trades_loop(self):
        """Execute profitable trades"""
        while self.running:
            try:
                if self.opportunities:
                    # Execute the best opportunity
                    best_opportunity = self.opportunities[0]
                    
                    # Risk check
                    if (best_opportunity.confidence > 0.7 and 
                        best_opportunity.risk_score < 0.5 and
                        best_opportunity.net_profit > 0.01):  # Minimum 0.01 SOL profit
                        
                        success = await self.execute_arbitrage(best_opportunity)
                        if success:
                            self.successful_trades += 1
                            self.total_profit += best_opportunity.net_profit
                            logger.info(f"Successful arbitrage: {best_opportunity.net_profit:.4f} SOL profit")
                        else:
                            self.failed_trades += 1
                            logger.warning(f"Failed arbitrage attempt")
                
                await asyncio.sleep(0.1)  # 100ms execution interval
                
            except Exception as e:
                logger.error(f"Error in trade execution loop: {e}")
                await asyncio.sleep(1)
    
    async def execute_arbitrage(self, opportunity: ArbitrageOpportunity) -> bool:
        """Execute flash arbitrage trade"""
        try:
            logger.info(f"Executing arbitrage: {opportunity.token_pair} "
                       f"({opportunity.exchange_a} -> {opportunity.exchange_b}) "
                       f"Profit: {opportunity.net_profit:.4f} SOL")
            
            # Simulate flash loan execution
            # In real implementation, this would:
            # 1. Request flash loan
            # 2. Buy on exchange A
            # 3. Sell on exchange B
            # 4. Repay flash loan
            # 5. Keep profit
            
            # Simulate execution time and success rate
            await asyncio.sleep(0.05)  # 50ms execution time
            
            # Success rate based on confidence and risk
            success_probability = opportunity.confidence * (1 - opportunity.risk_score)
            success = np.random.random() < success_probability
            
            return success
            
        except Exception as e:
            logger.error(f"Error executing arbitrage: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """Get engine statistics"""
        return {
            'total_profit': self.total_profit,
            'successful_trades': self.successful_trades,
            'failed_trades': self.failed_trades,
            'success_rate': self.successful_trades / max(1, self.successful_trades + self.failed_trades),
            'opportunities_count': len(self.opportunities),
            'running': self.running,
            'timestamp': time.time()
        }
    
    def get_opportunities(self) -> List[Dict]:
        """Get current opportunities"""
        return [asdict(opp) for opp in self.opportunities[:10]]  # Top 10 opportunities
    
    async def stop(self):
        """Stop the arbitrage engine"""
        logger.info("Stopping Flash Arbitrage Engine...")
        self.running = False
        await self.solana_client.close()

# Global engine instance
engine = None

def create_engine(config: Dict) -> FlashArbitrageEngine:
    """Create and configure the arbitrage engine"""
    global engine
    engine = FlashArbitrageEngine(config)
    return engine

def get_engine() -> Optional[FlashArbitrageEngine]:
    """Get the global engine instance"""
    return engine

if __name__ == "__main__":
    # Load configuration from config.py
    config = get_config()
    
    logger.info(f"Starting Flash Arbitrage Bot for wallet: {get_wallet_address()}")
    logger.info(f"Configuration: Min Profit: {config['min_profit_threshold']*100:.3f}%, Max Position: {config['max_position_size']} SOL")
    
    # Create and start engine
    arbitrage_engine = create_engine(config)
    
    try:
        asyncio.run(arbitrage_engine.start())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        asyncio.run(arbitrage_engine.stop())

