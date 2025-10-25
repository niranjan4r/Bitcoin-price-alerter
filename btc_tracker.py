import requests

def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    response = requests.get(url)
    data = response.json()
    return {
        "price": data["market_data"]["current_price"]["usd"],
        "ath": data["market_data"]["ath"]["usd"]
    }

def percentage_change_above_threshold(price, ath, threshold_percent):
    percentage_difference  = ((ath - price) / price ) * 100
    return percentage_difference >= threshold_percent
