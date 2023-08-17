import time
import ccxt
import RPi.GPIO as GPIO

CHOOSE_API = "Test"

if CHOOSE_API == "Test":
    api_key = '1kdPFNXCSS6k4rUxh0qBJZBQ103tL09mkQe9KcSeg3U071qUS2QY8Z0UYQPp90js'
    api_secret = 'CdJVZedmdsYksCeVnTMD5WwA02lIqwNwD8V1e3qCKBpf8sflYMs4LRjX4ihXJkkR'
else:
    api_key = '3rhghSVxptJHgpW9v3xxpW8OmqYji0q48ywRBm31YjHQMd5msBvqnPEpeXb5y0fS'
    api_secret = 'NDzpLwywWmJJXNdT2Z0GowCH7QrWEc04pnWH4LyW33WLjNT8d8LwwGkh9emVqiUC'

exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True
})

def startup():
    exchange.load_markets()
    exchange.fetch_balance()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(39, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def fetch_last_price(symbol):
    ticker_price = exchange.fetch_ticker(symbol)['last']
    return ticker_price

def bid_ask(symbol):
    ticker_bid = exchange.fetch_ticker(symbol)['bid']
    ticker_ask = exchange.fetch_ticker(symbol)['ask']
    return f"Bid: {ticker_bid} Ask: {ticker_ask}"

def high_low(symbol):
    ticker_high = exchange.fetch_ticker(symbol)['high']
    ticker_low = exchange.fetch_ticker(symbol)['low']
    return f"High: {ticker_high} Low: {ticker_low}"

def buy_advanced(symbol, amount):
    price = fetch_last_price(symbol)
    params = {
        'stopLoss': {
            'type': 'limit',
            'price': price - 10,
            'triggerPrice': price - 8,
        },
        'takeProfit': {
            'type': 'market',
            'triggerPrice': price + 20,
        }
    }
    exchange.create_order(symbol, 'limit', 'buy', amount, price, params)

def sell_advanced(symbol, amount):
    price = fetch_last_price(symbol)
    params = {
        'stopLoss': {
            'type': 'limit',
            'price': price + 10,
            'triggerPrice': price + 8,
        },
        'takeProfit': {
            'type': 'market',
            'triggerPrice': price + 15,
        }
    }
    exchange.create_order(symbol, 'limit', 'sell', amount, price, params)

def main():
    startup()
    translate = ["BTC/EUR", "BNB/EUR", "BCH/EUR"]
    ticker = 0
    layers = 0
    amount = 1

    while True:
        # BUY | Advanced Buy | Bid - Ask
        if GPIO.input(31) == GPIO.LOW:
            if layers == 0:
                buy_market(translate[ticker], amount)
            elif layers == 1:
                buy_advanced(translate[ticker], amount)
            elif layers == 2:
                bid_ask(translate[ticker])

            time.sleep(0.1)
            while GPIO.input(31) == GPIO.LOW:
                time.sleep(0.1)
            time.sleep(0.5)
        
        # SELL | Advanced Sell | High - Low
        if GPIO.input(33) == GPIO.LOW:
            if layers == 0:
                sell_market(translate[ticker], amount)
            elif layers == 1:
                sell_advanced(translate[ticker], amount)
            elif layers == 2:
                high_low(translate[ticker])

            time.sleep(0.1)
            while GPIO.input(33) == GPIO.LOW:
                time.sleep(0.1)
            time.sleep(0.5)
        
        # TICKER |
        if GPIO.input(37) == GPIO.LOW:
            if layers == 0:
                elements_number = len(translate)
                if ticker < elements_number - 1:
                    ticker += 1
                else:
                    ticker = 0
            elif layers == 1:
                # Do other thing
                pass
                
            time.sleep(0.1)
        
        # RESET TICKER
        if GPIO.input(33) == GPIO.LOW and GPIO.input(37) == GPIO.LOW:
            ticker = 0

        # HOME
        if GPIO.input(37) == GPIO.LOW and GPIO.input(39) == GPIO.LOW:
            line1 = exchange.fetch_balance()
            line2 = fetch_last_price(translate[ticker])
            # LCD Realtime information such as your Balance
        
        # Layers
        if GPIO.input(39) == GPIO.LOW:
            if layers <= 2:
                layers += 1
                # LCD code Warning that you are changing the behavior
            else:
                layers = 0
                # LCD code Warning that you are changing the behavior

if __name__ == "__main__":
    main()
