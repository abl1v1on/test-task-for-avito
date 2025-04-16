from dataclasses import dataclass
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.game_details_page import GameDetailsPage


@dataclass(frozen=True)
class MainPageSelectors:
    FILTER_BY_PLATFORM = (
        By.XPATH, 
        '//div[text()="Filter by platform"]/following-sibling::*[1]'
    )
    FILTER_BY_CATEGORY = (
        By.XPATH, 
        '//div[text()="Filter by category"]/following-sibling::*[1]'
    )
    SORT_BY = (By.XPATH, '//div[text()="Sort by"]/following-sibling::*[1]')
    GAMES = (By.CSS_SELECTOR, '.ant-card-body')
    ELEMENTS_ON_PAGE = (By.CSS_SELECTOR, '.ant-pagination-options div')
    PAGINATION = (By.CSS_SELECTOR, 'ul.ant-pagination')
    PAGINATION_ELEMENT = lambda page: (
        By.CSS_SELECTOR,
        f'li.ant-pagination-item[title="{page}"]'
    )
    CURRENT_PAGE = (By.CSS_SELECTOR, '.ant-pagination-item-active a')
    NEXT_PAGE_BTN = (By.CSS_SELECTOR, 'li.ant-pagination-next')
    LAST_PAGE = (By.CSS_SELECTOR, 'li.ant-pagination-jump-next + li')
    RELEASE_DATES = (By.XPATH, '//div[contains(text(), "Release")]')
    OPTION = lambda option: (
        By.XPATH, 
        f'//div[@class="ant-select-item-option-content" and text()="{option}"]'
    )


class MainPage(BasePage):
    """
    - не работает фильтр по категориям (только для шутеров)
    - при выборе not chosen в фильтре по платформе появляется ошибка
    - при выборе not chosen в фильтре по категории появляется ошибка
    - на странице с ошибкой при выборе not chosen 
        в фильтрах не работает кнопка возвращения на главную
    - при выборе платформы browser и категории 
        mmorpg пропадает выбор кол-ва элементов на странице
    - не дает выбрать 50 элементов на странице
    - не переходит на последнюю страницу
    - при возвращении с карточки игры, фильтры, 
        страница и кол-во элементов на странице сбрасывается
    - при изменении фильров кол-во элементов на странице сбрасывается
    - не понятно как именно система фильтрует игры по популярности
    - не работает сортировка по актуальности
    """
    def __init__(self, browser: WebDriver, timeout: int = 5) -> None:
        super().__init__(browser, timeout)

    @property
    def filter_by_platform_select(self) -> WebElement:
        return self.find(*MainPageSelectors.FILTER_BY_PLATFORM)

    @property
    def filter_by_category_select(self) -> WebElement:
        return self.find(*MainPageSelectors.FILTER_BY_CATEGORY)
    
    @property
    def sort_by_select(self) -> WebElement:
        return self.find(*MainPageSelectors.SORT_BY)
    
    @property
    def pagination(self) -> WebElement:
        return self.find(*MainPageSelectors.PAGINATION)
    
    @property
    def current_page(self) -> int:
        return int(self.find(*MainPageSelectors.CURRENT_PAGE).text)

    @property
    def next_page_btn(self) -> WebElement:
        return self.find(*MainPageSelectors.NEXT_PAGE_BTN)

    @property
    def last_page(self) -> int:
        return int(self.find(*MainPageSelectors.LAST_PAGE).text)

    @property
    def elements_on_page_select(self) -> WebElement:
        return self.find(*MainPageSelectors.ELEMENTS_ON_PAGE)

    @property
    def release_dates(self) -> list[WebElement]:
        return self.find(*MainPageSelectors.RELEASE_DATES, many=True)

    @property
    def games(self) -> list[WebElement]:
        return self.find(*MainPageSelectors.GAMES, many=True)

    def option(self, value: str) -> WebElement:
        """
        Универсальный метод для выбора 
        любых элементов списка на странице
        """
        return self.find(*MainPageSelectors.OPTION(value))
    
    def pagination_element(self, page: int) -> WebElement:
        return self.find(*MainPageSelectors.PAGINATION_ELEMENT(page))
    
    def go_to_next_page(self) -> None:
        """Перейти на следующую страницу"""
        self.next_page_btn.click()

    def go_to_page(self, page: int) -> None:
        """Перейти на выбранную страницу"""
        while self.current_page != page:
            self.go_to_next_page()

    def go_to_game(self, game: WebElement) -> GameDetailsPage:
        game.click()
        return GameDetailsPage(self.browser)

    def select_platform(self, value: str) -> None:
        """Выбор платформы"""
        self.filter_by_platform_select.click()
        self.option(value).click()

    def select_category(self, value: str) -> None:
        """Выбор категории"""
        self.filter_by_category_select.click()
        self.option(value).click()

    def sort_by(self, value: str) -> None:
        """Выбор сортировки"""
        self.sort_by_select.click()
        self.option(value).click()
    
    def select_page(self, page: int) -> None:
        self.pagination_element(page).click()

    def select_elements_on_page(self, elements_qty: int) -> None:
        """Выбор кол-ва элементов на странице"""
        self.elements_on_page_select.click()
        self.option(f'{elements_qty} / page').click()

    def get_game_name(self, game: WebElement) -> str:
        return game.find_element(By.CSS_SELECTOR, 'h1').text
