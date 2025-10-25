import time
import yaml
from btc_tracker import get_btc_data, is_below_threshold
from email_notifier import send_email
from cache_object import alertCache
import random
def main():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    interval = config["interval_minutes"] * 60
    thresholds = sorted(config["alert_threshold_percent"],reverse=True)  # e.g., [5, 10, 20]
    email_cfg = config["email"]
    alert_cache=alertCache() #object for storing last threshold and last week
    while True:
        btc_data = get_btc_data()
        price , ath = btc_data["price"], btc_data["ath"]
        print(f"BTC: ${price} (ATH: ${ath})")
        alert_cache.reset_week() #checks for new week in every iteration
        for threshold in thresholds:
            #if threshold is greater than last threshold and price is below threshold from ath, send email
            if threshold > (alert_cache.last_threshold if alert_cache.last_threshold else 0) and is_below_threshold(price, ath, threshold):
                subject = f"Bitcoin {threshold}% Drop Alert!"
                body = (
                    f"BTC is at ${price}, which is below {threshold}% "
                    f"from its all-time high of ${ath}."
                )
                alert_cache.last_threshold=threshold
                send_email(email_cfg, subject, body)
                break
        time.sleep(interval)

if __name__ == "__main__":
    main()
