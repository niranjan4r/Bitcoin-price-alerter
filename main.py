import time
import yaml
from btc_tracker import get_btc_data, percentage_change_above_threshold
from email_notifier import send_email
from logger_config import setup_logger

logger = setup_logger(__name__)

def main():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    interval_in_seconds = config["interval_minutes"] * 60
    email_cfg = config["email"]
    threshold = config["threshold"]

    logger.info("Starting BTC tracker service...")

    while True:
        try:
            btc_data = get_btc_data()
            price, ath = btc_data["price"], btc_data["ath"]
            logger.info(f"BTC: ${price} (ATH: ${ath})")

            if percentage_change_above_threshold(price, ath, threshold):
                subject = f"Bitcoin {threshold}% Drop Alert!"
                body = (
                    f"BTC is at ${price}, which is below {threshold}% "
                    f"from its all-time high of ${ath}."
                )
                logger.info("Threshold breached, sending email...")
                send_email(email_cfg, subject, body)
            else:
                logger.info("No significant drop detected.")

        except Exception as e:
            logger.exception(f"Unexpected error occurred: {e}")

        time.sleep(interval_in_seconds)

if __name__ == "__main__":
    main()
