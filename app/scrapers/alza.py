from typing import Generator
from contextlib import contextmanager
from selenium.webdriver.common.by import By

from app.scrapers import ShopItem
from app.exceptions import ErrorParsing, OutOfStockException


class AlzaItem(ShopItem):
    shop_name = "Alza"

    def _check_out_of_stock(self) -> bool:
        try:
            driver = self._get_driver()
            dialog = driver.find_element(
                by=By.CSS_SELECTOR, value="div.archiveDetailDailog.titled"
            )
            title_content = dialog.find_element(by=By.CLASS_NAME, value="titleContent")
            text = "Prodej skončil"
            return text.lower().strip() in title_content.text.lower().strip()
        except:
            return False

    @contextmanager
    def get_price(self) -> Generator[int, None, None]:
        with self.driver_manager.driver_context():
            self.open()
            if self._check_out_of_stock():
                raise OutOfStockException("Product is out of stock")
            try:
                price = self._get_driver().find_element(
                    by=By.CLASS_NAME, value="price-box__price"
                )
                yield self._parse_int(price.text)
            except ErrorParsing:
                raise ErrorParsing("Error parsing price")
