import time
from binance.spot import Spot
from rich import print


client = Spot()

# Get server timestamp
# print(client.time())
# Get klines of BTCUSDT at 1m interval
# print(client.klines("BTCUSDT", "1m"))
# Get last 10 klines of BNBUSDT at 1h interval
# print(client.klines("BNBUSDT", "1h", limit=10))

# API key/secret are required for user data endpoints
client = Spot(
    api_key='VVLbrJ2l3Rn947tJwoQzW94CtdfzisLLBuRtlHAXH52Q6pRxmqApTAHh6kjIttgh',
    api_secret='2eGON9bg3R4wkCokU733z9Q2qxphc04QnDBud4wvVhDYzypYQ0elR0yR4X5CpY5o',
    base_url='https://testnet.binance.vision',
)
# client.cancel_open_orders(symbol='BTCUSDT')
# Get account and balance information
print(client.get_order_rate_limit())

# Post a new order
# params = {'symbol': 'BTCUSDT', 'side': 'SELL', 'type': 'LIMIT', 'timeInForce': 'GTC', 'quantity': 0.002, 'price': 40000}

# response = client.new_order(**params)
# print(response)

while True:
    price = float(client.ticker_price("BTCUSDT")["price"])
    avg_price = float(client.avg_price("BTCUSDT")["price"])
    diff = price - avg_price
    diff_pct = (diff / avg_price) * 100.0
    print(f"price={price}, avg_price={avg_price}, diff={diff}, diff_pct={diff_pct}%")
    time.sleep(1)
