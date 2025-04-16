import time
import pytest
from datetime import datetime
from selenium.webdriver.remote.webelement import WebElement

from pages.main_page import MainPage


@pytest.fixture(scope='function')
def page(browser: WebElement) -> MainPage:
    page = MainPage(browser)
    page.open()
    return page


def test_open_game_details(page: MainPage) -> None:
    first_game = page.games[0]
    game_page = page.go_to_game(first_game)
    assert game_page.game_name == 'Tarisland', 'Открывается не та игра'


@pytest.mark.parametrize('quantity', [
    10, 
    20, 
    pytest.param(50, marks=pytest.mark.xfail(reason='BUG')), 
    100]
)
def test_change_games_qty_on_page(page: MainPage, quantity: int) -> None:
    page.select_elements_on_page(quantity)
    assert len(page.games) == quantity, (
        'Отображается неправильное кол-во игр на странице'
    )


def test_open_second_page(page: MainPage) -> None:
    page.go_to_next_page()
    assert page.current_page == 2, 'Вторая страница не открывается'


def test_open_penultimate_page(page: MainPage) -> None:
    page.go_to_page(40)
    assert page.current_page == 40, 'Предпоследняя страница не открывается'


@pytest.mark.xfail(reason='BUG')
def test_open_last_page(page: MainPage) -> None:
    page.go_to_page(40)
    page.go_to_next_page()
    assert page.current_page == 41, 'Последняя страница не открывается'


@pytest.mark.parametrize('quantity, pages', [(20, 21), (100, 5)])
def test_check_pages_quantity_with_changed_games_qty_in_page(
        page: MainPage, 
        quantity: int, 
        pages: int
    ) -> None:
    page.select_elements_on_page(quantity)
    assert page.pagination_element(pages).is_displayed()


@pytest.mark.flaky(reruns=3, reruns_delay=1)
@pytest.mark.parametrize(
    'platform, alias', 
    [('Browser', 'Web Browser'), ('PC', 'Windows')]
)
def test_game_platform_filter(
        page: MainPage, 
        platform: str, 
        alias: str
    ) -> None:
    for i in range(10):
        page.select_platform(platform)
        game_page = page.go_to_game(page.games[i])
        assert game_page.platform == alias
        game_page.browser.back()



@pytest.mark.xfail(reason='BUG')
def test_disable_platform_filter(page: MainPage) -> None:
    page.select_platform('Browser')
    page.select_platform('not chosen')
    assert page.pagination.is_displayed()


@pytest.mark.xfail(reason='BUG')
@pytest.mark.parametrize(
    'category', 
    ['mmorpg', 'shooter', 'strategy', 'moba', 'racing', 'sports', 'social']
)
def test_game_category_filter(page: MainPage, category: str) -> None:
    for i in range(10):
        # TODO: change time on webdriverwait
        time.sleep(1)
        page.select_category(category)
        game_page = page.go_to_game(page.games[i])
        assert game_page.genere.lower() == category
        game_page.browser.back()


@pytest.mark.xfail(reason='BUG')
def test_disable_category_filter(page: MainPage) -> None:
    page.select_category('mmorpg')
    page.select_category('not chosen')
    assert page.pagination.is_displayed()


def test_sort_by_release_date(page: MainPage) -> None:
    page.sort_by('Release date')
    time.sleep(5)
    release_dates = page.release_dates
    parsed_dates = []

    for release_date in release_dates:
        try:
            date_str = release_date.text.split(':')[-1].strip()
            date_obj = datetime.strptime(date_str, '%d.%m.%Y').date()
            parsed_dates.append(date_obj)
        except:
            pass

    assert sorted(parsed_dates)[::-1] == parsed_dates, (
        'Не работает сортировка по дате выхода'
    )


def test_sort_by_aplhabetical(page: MainPage) -> None:
    page.sort_by('Alphabetical')
    time.sleep(3)
    parsed_games = [page.get_game_name(game) for game in page.games]
    
    assert sorted(parsed_games) == parsed_games, (
        'Не работает сортировка по алфавиту'
    )


def test_disable_sorting(page: MainPage) -> None:
    page.sort_by('Release date')
    page.sort_by('not chosen')
    assert page.pagination.is_displayed()
 