import requests

def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    response = requests.get(url)
    data = response.json()
    return {
        "price": data["market_data"]["current_price"]["usd"],
        "ath": data["market_data"]["ath"]["usd"]
    }

def get_percentage_difference_from_ath(price, ath):
    return ((ath - price) / price ) * 100
