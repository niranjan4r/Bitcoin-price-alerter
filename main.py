import time
import yaml
from btc_tracker import get_btc_data, get_percentage_difference_from_ath
from email_notifier import send_email
from cache_object import alertCache
from logger_config import setup_logger

logger = setup_logger(__name__)


def main():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    interval_in_seconds = config["interval_minutes"] * 60
    thresholds = sorted(
        config["alert_threshold_percent"], reverse=True
    )
    email_cfg = config["email"]
    alert_cache = alertCache()
    logger.info("Starting BTC tracker service...")

    while True:
        try:
            btc_data = get_btc_data()
            price, ath = btc_data["price"], btc_data["ath"]
            logger.info(f"BTC: ${price} (ATH: ${ath})")
            alert_cache.reset_week() 
            for threshold in thresholds:
                calculated_percentage_difference = get_percentage_difference_from_ath(price, ath)
                if threshold > (
                alert_cache.last_threshold if alert_cache.last_threshold else 0
                ) and calculated_percentage_difference >= threshold:
                    logger.info(f"Threshold breached at {calculated_percentage_difference}")
                    subject = f"Bitcoin {threshold}% Drop Alert!"
                    body = (
                        f"BTC is at ${price}, which is below {threshold}% "
                        f"from its all-time high of ${ath}."
                        f"Calculated percentage difference is ${calculated_percentage_difference}"
                    )
                    alert_cache.last_threshold = threshold
                    if email_cfg["is_feature_enabled"] is True:
                        logger.info("Email feature enabled, email will be sent for alert")
                        send_email(email_cfg, subject, body)
                    else:
                        logger.info("Email feature disabled, no email will be sent for alert")
                    break

                else:
                    logger.info("No significant drop detected.")

        except Exception as e:
            logger.exception(f"Unexpected error occurred: {e}")

        logger.info(f"Sleeping for {interval_in_seconds} seconds")
        time.sleep(interval_in_seconds)



if __name__ == "__main__":
    main()
