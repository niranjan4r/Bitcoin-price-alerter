import time
import yaml
from btc_tracker import get_btc_data, is_below_threshold
from email_notifier import send_email

def main():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    interval = config["interval_minutes"] * 60
    thresholds = sorted(config["alert_threshold_percent"])  # e.g., [5, 10, 20]
    email_cfg = config["email"]

    while True:
        btc_data = get_btc_data()
        price, ath = btc_data["price"], btc_data["ath"]
        print(f"BTC: ${price} (ATH: ${ath})")

        for threshold in thresholds:
            if is_below_threshold(price, ath, threshold):
                subject = f"Bitcoin {threshold}% Drop Alert!"
                body = (
                    f"BTC is at ${price}, which is below {threshold}% "
                    f"from its all-time high of ${ath}."
                )
                send_email(email_cfg, subject, body)

        time.sleep(interval)

if __name__ == "__main__":
    main()
