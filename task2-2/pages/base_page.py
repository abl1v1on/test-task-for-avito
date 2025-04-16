from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from config import settings


class BasePage:
    def __init__(self, browser: WebDriver, timeout: int = 5) -> None:
        self.browser = browser
        self.url = settings.page.base_url
        self.browser.implicitly_wait(timeout)

    def open(self) -> None:
        self.browser.get(self.url)
    
    def find(
            self, 
            by: str, 
            value: str, 
            many: bool = False
        ) -> WebElement | list[WebElement]:
        if many:
            return self.browser.find_elements(by, value)
        return self.browser.find_element(by, value)
