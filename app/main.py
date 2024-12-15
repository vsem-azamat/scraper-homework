from app.config import cnfg
from app.logger import logger
from app.utils import get_links_from_csv
from app.scrapers.alza import AlzaItem
from app.services import EmailNotifierInterface, PriceTracker


def main():
    logger.setLevel("INFO")

    notifier = EmailNotifierInterface(
        smtp_server=cnfg.Email.SMTP_SERVER,
        smtp_port=cnfg.Email.SMTP_PORT,
        smtp_password=cnfg.Email.SMTP_PASSWORD,
        sender_email=cnfg.Email.SENDER_EMAIL,
        receiver_email=cnfg.Email.RECEIVER_EMAIL
    )

    tracker = PriceTracker(notifier=notifier)

    links = get_links_from_csv(cnfg.FILE_LINKS_PATH)
    for link in links:
        item = AlzaItem(link)
        tracker.add_item(item)

    for idx, price in enumerate(tracker.track_periodically(period=cnfg.PERIOD_TRACKING)):
        logger.info(f"Cycle {idx+1}: {price}")


if __name__ == "__main__":
    main()
