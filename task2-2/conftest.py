import pytest
from typing import Generator
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope='session')
def service() -> Service:
    return Service(ChromeDriverManager().install())


@pytest.fixture(scope='session')
def options() -> Options:
    chrome_options = Options()
    # add options
    return chrome_options


@pytest.fixture(scope='function')
def browser(service: Service, options: Options) -> Generator[Chrome, None]:
    browser = Chrome(service=service, options=options)
    yield browser
    browser.quit()
