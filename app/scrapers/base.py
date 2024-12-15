import os
import re
from typing import Generator
from abc import ABC, abstractmethod
from contextlib import contextmanager
from webdriver import WebDriverManager

from app.exceptions import ErrorParsingInt


class ShopItem(ABC):
    """
    Abstract class for shop items with defined interfaces for child classes
    """

    shop_name = "ShopABC"

    def __init__(self, url: str) -> None:
        self.url = url
        self.driver_manager = WebDriverManager()

    def _get_driver(self):
        return self.driver_manager.get_driver()

    def open(self, implicitly_wait: int = 3) -> None:
        driver = self._get_driver()
        driver.get(self.url)
        driver.implicitly_wait(implicitly_wait)

    def _parse_int(self, text: str) -> int:
        try:
            return int(re.sub(r"[^\d]", "", text))
        except:
            raise ErrorParsingInt("Error parsing integer from text")

    def __repr__(self) -> str:
        return f"Item({self.shop_name}, {os.path.basename(self.url)})"

    @abstractmethod
    @contextmanager
    def get_price(self) -> Generator[int, None, None]:
        raise NotImplementedError

    @abstractmethod
    def _check_out_of_stock(self) -> bool:
        """
        Check if product is out of stock.
        This method is optional and can be implemented in child classes.
        """
        pass

    def __eq__(self, value: "object") -> bool:
        if not isinstance(value, ShopItem):
            return False
        return self.url == value.url
