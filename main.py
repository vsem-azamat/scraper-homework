from unittest.mock import Mock

from logger import logger
from scrapers import AlzaItem
from services import EmailNotifierInterface, PriceTracker

logger.setLevel("DEBUG")

""">>>>> EXAMPLE USAGE <<<<<"""
logger.debug(">>> Start testing <<<")

mock_notifier = Mock(spec=EmailNotifierInterface)

tracker = PriceTracker(notifier=mock_notifier)

url_1 = "https://www.alza.cz/iphone-15-pro?dq=7927758"  # out of stock
url_2 = "https://www.alza.cz/iphone-15-pro-1tb-bily-titan-d7927767.htm"

item_1 = AlzaItem(url_1)
item_2 = AlzaItem(url_2)

tracker.add_item(item_1)
tracker.add_item(item_2)


logger.debug("Tracking prices once")
prices = tracker.track_once()
logger.debug(prices)

logger.debug("Tracking prices periodically")
idx_break = 2
for price in tracker.track_periodically(period=10):
    logger.debug(price)

    idx_break -= 1
    if idx_break == 0:
        break

logger.debug("Mock send_email call count:", mock_notifier.send_email.call_count)
