from selenium import webdriver

from typing import Generator
from contextlib import contextmanager


class WebDriverManager:
    """
    Singleton manager for WebDriver instance to ensure only one browser is running
    """

    _instance = None
    _driver = None

    def __new__(cls) -> "WebDriverManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_driver(self) -> webdriver.Chrome:
        if self._driver is None:
            self._driver = webdriver.Chrome()
        return self._driver

    def close_driver(self) -> None:
        if self._driver is not None:
            self._driver.quit()
            self._driver = None

    @contextmanager
    def driver_context(self) -> Generator[webdriver.Chrome, None, None]:
        try:
            driver = self.get_driver()
            yield driver
        except Exception as e:
            self.close_driver()
            raise e
