#!/usr/bin/env python3
"""
Python wrapper for the Flash Arbitrage Engine shared library
"""

import ctypes
import os
from typing import Optional, Tuple, List

class ArbitrageEngine:
    """Python wrapper for the C++ arbitrage engine"""
    
    def __init__(self, lib_path: str = None):
        """Initialize the arbitrage engine
        
        Args:
            lib_path: Path to the shared library. If None, looks in current directory.
        """
        if lib_path is None:
            lib_path = os.path.join(os.path.dirname(__file__), 'libarbitrage_engine.so')
        
        self.lib = ctypes.CDLL(lib_path)
        
        # Define function signatures
        self._setup_function_signatures()
        
        # Initialize the engine
        if not self.lib.init_arbitrage_engine():
            raise RuntimeError("Failed to initialize arbitrage engine")
    
    def _setup_function_signatures(self):
        """Setup ctypes function signatures"""
        
        # init_arbitrage_engine() -> bool
        self.lib.init_arbitrage_engine.restype = ctypes.c_bool
        
        # add_market_data(exchange, token_pair, bid_price, ask_price, volume)
        self.lib.add_market_data.argtypes = [
            ctypes.c_char_p, ctypes.c_char_p, 
            ctypes.c_double, ctypes.c_double, ctypes.c_double
        ]
        
        # scan_for_opportunities() -> int
        self.lib.scan_for_opportunities.restype = ctypes.c_int
        
        # execute_trade(opportunity_index) -> bool
        self.lib.execute_trade.argtypes = [ctypes.c_int]
        self.lib.execute_trade.restype = ctypes.c_bool
        
        # get_engine_stats(total_profit*, successful_trades*, failed_trades*, opportunities_count*)
        self.lib.get_engine_stats.argtypes = [
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int)
        ]
        
        # get_opportunity_details(index, token_pair*, profit_potential*, exchange_a*, exchange_b*, net_profit*) -> bool
        self.lib.get_opportunity_details.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_double)
        ]
        self.lib.get_opportunity_details.restype = ctypes.c_bool
        
        # set_engine_config(min_profit, max_gas, max_slippage)
        self.lib.set_engine_config.argtypes = [
            ctypes.c_double, ctypes.c_double, ctypes.c_double
        ]
        
        # stop_engine()
        self.lib.stop_engine.argtypes = []
        
        # cleanup_engine()
        self.lib.cleanup_engine.argtypes = []
    
    def add_market_data(self, exchange: str, token_pair: str, 
                       bid_price: float, ask_price: float, volume: float):
        """Add market data from an exchange
        
        Args:
            exchange: Name of the exchange (e.g., "Raydium", "Orca")
            token_pair: Token pair (e.g., "SOL/USDC")
            bid_price: Current bid price
            ask_price: Current ask price
            volume: Available volume
        """
        self.lib.add_market_data(
            exchange.encode('utf-8'),
            token_pair.encode('utf-8'),
            ctypes.c_double(bid_price),
            ctypes.c_double(ask_price),
            ctypes.c_double(volume)
        )
    
    def scan_opportunities(self) -> int:
        """Scan for arbitrage opportunities
        
        Returns:
            Number of opportunities found
        """
        return self.lib.scan_for_opportunities()
    
    def execute_trade(self, opportunity_index: int) -> bool:
        """Execute a specific arbitrage trade
        
        Args:
            opportunity_index: Index of the opportunity to execute
            
        Returns:
            True if trade was successful, False otherwise
        """
        return self.lib.execute_trade(ctypes.c_int(opportunity_index))
    
    def get_statistics(self) -> Tuple[float, int, int, int]:
        """Get engine statistics
        
        Returns:
            Tuple of (total_profit, successful_trades, failed_trades, opportunities_count)
        """
        total_profit = ctypes.c_double()
        successful_trades = ctypes.c_int()
        failed_trades = ctypes.c_int()
        opportunities_count = ctypes.c_int()
        
        self.lib.get_engine_stats(
            ctypes.byref(total_profit),
            ctypes.byref(successful_trades),
            ctypes.byref(failed_trades),
            ctypes.byref(opportunities_count)
        )
        
        return (
            total_profit.value,
            successful_trades.value,
            failed_trades.value,
            opportunities_count.value
        )
    
    def get_opportunity_details(self, index: int) -> Optional[dict]:
        """Get details of a specific opportunity
        
        Args:
            index: Index of the opportunity
            
        Returns:
            Dictionary with opportunity details or None if index is invalid
        """
        token_pair = ctypes.create_string_buffer(256)
        exchange_a = ctypes.create_string_buffer(256)
        exchange_b = ctypes.create_string_buffer(256)
        profit_potential = ctypes.c_double()
        net_profit = ctypes.c_double()
        
        success = self.lib.get_opportunity_details(
            ctypes.c_int(index),
            token_pair,
            ctypes.byref(profit_potential),
            exchange_a,
            exchange_b,
            ctypes.byref(net_profit)
        )
        
        if success:
            return {
                'token_pair': token_pair.value.decode('utf-8'),
                'exchange_a': exchange_a.value.decode('utf-8'),
                'exchange_b': exchange_b.value.decode('utf-8'),
                'profit_potential': profit_potential.value,
                'net_profit': net_profit.value
            }
        return None
    
    def get_all_opportunities(self) -> List[dict]:
        """Get details of all current opportunities
        
        Returns:
            List of opportunity dictionaries
        """
        _, _, _, count = self.get_statistics()
        opportunities = []
        
        for i in range(count):
            opp = self.get_opportunity_details(i)
            if opp:
                opportunities.append(opp)
        
        return opportunities
    
    def set_config(self, min_profit: float = 0.01, max_gas: float = 0.005, 
                   max_slippage: float = 0.02):
        """Set engine configuration
        
        Args:
            min_profit: Minimum profit threshold (default 1%)
            max_gas: Maximum gas cost in SOL (default 0.005)
            max_slippage: Maximum slippage tolerance (default 2%)
        """
        self.lib.set_engine_config(
            ctypes.c_double(min_profit),
            ctypes.c_double(max_gas),
            ctypes.c_double(max_slippage)
        )
    
    def stop(self):
        """Stop the arbitrage engine"""
        self.lib.stop_engine()
    
    def cleanup(self):
        """Cleanup engine resources"""
        self.lib.cleanup_engine()
    
    def __del__(self):
        """Destructor - cleanup resources"""
        try:
            self.cleanup()
        except:
            pass


# Example usage
if __name__ == "__main__":
    # Initialize the engine
    engine = ArbitrageEngine()
    
    # Configure the engine
    engine.set_config(min_profit=0.005, max_gas=0.01, max_slippage=0.03)
    
    # Add some sample market data
    engine.add_market_data("Raydium", "SOL/USDC", 100.5, 100.8, 1000.0)
    engine.add_market_data("Orca", "SOL/USDC", 101.2, 101.5, 800.0)
    engine.add_market_data("Serum", "SOL/USDC", 99.8, 100.1, 1200.0)
    
    # Scan for opportunities
    count = engine.scan_opportunities()
    print(f"Found {count} arbitrage opportunities")
    
    # Get all opportunities
    opportunities = engine.get_all_opportunities()
    for i, opp in enumerate(opportunities):
        print(f"Opportunity {i}: {opp}")
    
    # Execute the best opportunity if available
    if opportunities:
        success = engine.execute_trade(0)
        print(f"Trade execution: {'Success' if success else 'Failed'}")
    
    # Get statistics
    total_profit, successful, failed, opp_count = engine.get_statistics()
    print(f"Statistics: Profit={total_profit:.4f}, Success={successful}, Failed={failed}, Opportunities={opp_count}")
    
    # Cleanup
    engine.stop()

