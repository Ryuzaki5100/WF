import ccxt
import pandas as pd
import numpy as np
from collections import defaultdict
from scipy.optimize import linprog

# Initialize the exchanges
exchanges = {
    'binance': ccxt.binance({'apiKey': 'YOUR_API_KEY', 'secret': 'YOUR_SECRET_KEY'}),
    'kraken': ccxt.kraken({'apiKey': 'YOUR_API_KEY', 'secret': 'YOUR_SECRET_KEY'}),
    # Add other exchanges similarly
}

cryptos = ['USD', 'BTC', 'ETH', 'XRP', 'LTC']
nodes = [f'{ex}_{crypto}' for ex in exchanges.keys() for crypto in cryptos]

# Assume we have functions to fetch trading fees, order books, and gas fees
def fetch_trading_fees(exchange):
    return exchange.fetch_trading_fees()

def fetch_order_book(exchange, pair):
    return exchange.fetch_order_book(pair)

def estimate_gas_fees():
    gas_price = 100  # in gwei
    gas_limit = 21000  # typical gas limit for ETH transfer
    eth_usd_price = 2000  # example ETH price in USD
    gas_fee_in_eth = gas_price * gas_limit / 1e9  # convert gwei to ETH
    gas_fee_in_usd = gas_fee_in_eth * eth_usd_price
    return gas_fee_in_usd

def estimate_slippage(order_book, volume):
    bids = order_book['bids']
    asks = order_book['asks']
    
    def calculate_slippage(orders, volume):
        total_cost = 0
        total_volume = 0
        for price, order_volume in orders:
            if total_volume + order_volume >= volume:
                total_cost += price * (volume - total_volume)
                total_volume = volume
                break
            else:
                total_cost += price * order_volume
                total_volume += order_volume
        return total_cost / total_volume, total_volume
    
    slippage_buy, volume_buy = calculate_slippage(asks, volume)
    slippage_sell, volume_sell = calculate_slippage(bids, volume)
    
    return slippage_buy, slippage_sell, volume_buy, volume_sell

# Graph representation
class Graph:
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}
        self.liquidity = {}

    def add_edge(self, from_node, to_node, weight, liquidity):
        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight
        self.liquidity[(from_node, to_node)] = liquidity

# Construct the graph
def construct_graph(exchanges, cryptos):
    graph = Graph()
    for ex_name, exchange in exchanges.items():
        fees = fetch_trading_fees(exchange)
        for crypto_from in cryptos:
            for crypto_to in cryptos:
                if crypto_from != crypto_to:
                    pair = f'{crypto_from}/{crypto_to}'
                    try:
                        order_book = fetch_order_book(exchange, pair)
                        slippage_buy, slippage_sell, volume_buy, volume_sell = estimate_slippage(order_book, 1)  # Assume 1 unit for slippage
                        if crypto_from == 'USD':
                            weight = slippage_buy + fees['taker'] + estimate_gas_fees()
                            liquidity = volume_buy
                        else:
                            weight = slippage_sell + fees['taker'] + estimate_gas_fees()
                            liquidity = volume_sell
                        graph.add_edge(f'{ex_name}_{crypto_from}', f'{ex_name}_{crypto_to}', weight, liquidity)
                    except ccxt.BaseError:
                        continue  # Skip pairs that are not available
    
    # Add edges for cross-exchange transfers
    for crypto in cryptos:
        for ex_from in exchanges.keys():
            for ex_to in exchanges.keys():
                if ex_from != ex_to:
                    withdraw_fee = exchanges[ex_from].fees['funding']['withdraw'][crypto.lower()]
                    deposit_fee = exchanges[ex_to].fees['funding']['deposit'][crypto.lower()]
                    gas_fee = estimate_gas_fees() if crypto != 'USD' else 0
                    total_fee = withdraw_fee + deposit_fee + gas_fee
                    graph.add_edge(f'{ex_from}_{crypto}', f'{ex_to}_{crypto}', total_fee, float('inf'))  # Assume high liquidity for cross-exchange
    return graph

# DFS to find all paths of length n with pruning
def dfs_with_pruning(graph, start, path_length, path=[], paths=[], profit_to_fee_ratio=1.5):
    path = path + [start]
    if len(path) ==
