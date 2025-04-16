from dataclasses import dataclass
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


@dataclass(frozen=True)
class GameDetailsPageSelectors:
    GAME_NAME = (By.CSS_SELECTOR, 'h2')
    PLATFORM = (
        By.XPATH, 
        '//span[text()="Platform"]/following-sibling::*[1]'
    )
    GENERE = (
        By.XPATH,
        '//span[text()="Genre"]/following-sibling::*[1]'
    )


class GameDetailsPage(BasePage):
    def __init__(self, browser: WebDriver, timeout: int = 5) -> None:
        super().__init__(browser, timeout)

    @property
    def game_name(self) -> str:
        return self.find(*GameDetailsPageSelectors.GAME_NAME).text

    @property
    def platform(self) -> str:
        return self.find(*GameDetailsPageSelectors.PLATFORM).text

    @property
    def genere(self) -> str:
        return self.find(*GameDetailsPageSelectors.GENERE).text
