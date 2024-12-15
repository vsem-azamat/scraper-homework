import time
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Union, Generator

from app.logger import logger
from app.scrapers.alza import ShopItem
from webdriver import WebDriverManager
from app.exceptions import ErrorParsing, OutOfStockException

from app.services import EmailNotifierInterface


@dataclass(frozen=True)
class PriceTrack:
    item: ShopItem
    price: Union[int, Exception]
    updated_at: datetime = field(default_factory=datetime.now)

    def is_successful(self) -> bool:
        return not isinstance(self.price, Exception)

    def __repr__(self) -> str:
        return f"PriceTrack(item={self.item}, price={self.price}, updated_at={self.updated_at})"


class PriceTracker:
    def __init__(
        self,
        items: list[ShopItem] = [],
        notifier: Optional[EmailNotifierInterface] = None,
    ) -> None:
        self.items = items
        self.prices: list[PriceTrack] = []
        self.notifier = notifier
        self.driver_manager = WebDriverManager()

    def __del__(self) -> None:
        self.driver_manager.close_driver()

    def add_item(self, item: ShopItem) -> None:
        self.items.append(item)

    def remove_item(self, item: ShopItem) -> None:
        self.items.remove(item)

    def _track_item(self, item: ShopItem) -> PriceTrack:
        try:
            with item.get_price() as price:
                return PriceTrack(item, price)
        except OutOfStockException as e:
            return PriceTrack(item, e)
        except ErrorParsing as e:
            return PriceTrack(item, e)
        except Exception as e:
            return PriceTrack(item, e)

    def track_once(self) -> list[PriceTrack]:
        """Tracks price of all items once and returns the prices."""
        prices = []
        for item in self.items:
            track = self._track_item(item)
            prices.append(track)
            if self.notifier:
                subject = f"Price Update for {item.shop_name}"
                body = f"The price of {item.shop_name} item at {item.url} is {track.price} as of {track.updated_at}"
                self.notifier.send_email(subject, body)

        self.prices.extend(prices)
        return prices

    def track_periodically(
        self, period: int = 3600
    ) -> Generator[list[PriceTrack], None, None]:
        """
        Tracks price periodically and sends email notifications on each track.
        Args:
            period (int): Time in seconds to wait between each track.
        """
        try:
            while True:
                prices = self.track_once()
                yield prices
                logger.info(f"Prices tracked at {datetime.now()}")
                time.sleep(period)
        finally:
            self.driver_manager.close_driver()
