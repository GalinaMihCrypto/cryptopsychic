# cryptopsychic/predictor.py

import requests
import numpy as np
import time

def get_binance_klines(symbol="BTCUSDT", interval="1m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    closes = [float(kline[4]) for kline in data]
    return closes

def pump_probability(symbol="BTCUSDT", interval="1m", limit=100):
    closes = get_binance_klines(symbol, interval, limit)
    arr = np.array(closes)
    returns = np.diff(arr) / arr[:-1]

    # Custom volatility index
    volatility = np.std(returns) * np.sqrt(len(returns))

    # Custom EMA slope
    ema = np.convolve(arr, np.ones(10)/10, mode='valid')
    slope = ema[-1] - ema[0]

    # Pump Probability Index formula (toy but expandable)
    ppi = max(0, min(100, (volatility * 1000 + slope * 10000)))
    return round(ppi, 2)

if __name__ == "__main__":
    while True:
        ppi = pump_probability("BTCUSDT", "1m", 100)
        print(f"🔮 [CryptoPsychic] Pump Probability Index: {ppi}%")
        time.sleep(60)
