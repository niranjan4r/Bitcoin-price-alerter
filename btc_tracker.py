import requests

def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    response = requests.get(url)
    data = response.json()
    return {
        "price": data["market_data"]["current_price"]["usd"],
        "ath": data["market_data"]["ath"]["usd"]
    }

def is_below_threshold(price, ath, threshold_percent):
    return price < ath * (1 - threshold_percent / 100)
