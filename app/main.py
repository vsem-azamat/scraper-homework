from app.logger import logger
from app.scrapers.alza import AlzaItem
from app.services import EmailNotifierInterface, PriceTracker

def main():
    logger.setLevel("INFO")

    notifier = EmailNotifierInterface()

    tracker = PriceTracker(notifier=notifier)

    url_1 = "https://www.alza.cz/iphone-15-pro?dq=7927758"  # out of stock
    url_2 = "https://www.alza.cz/iphone-15-pro-1tb-bily-titan-d7927767.htm"

    item_1 = AlzaItem(url_1)
    item_2 = AlzaItem(url_2)

    tracker.add_item(item_1)
    tracker.add_item(item_2)

    idx_break = 2
    for price in tracker.track_periodically(period=10):
        logger.info(price)

        idx_break -= 1
        if idx_break == 0:
            break

if __name__ == "__main__":
    main()
