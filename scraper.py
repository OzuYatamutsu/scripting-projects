from selenium.common.exceptions import NoSuchElementException
from browser_utils import Browser, set_element_value


def is_hyatt_available() -> bool:
    START_DATE, END_DATE = '2018-08-30', '2018-09-03'
    URL = (
        'https://www.hyatt.com/en-US/search/Hyatt%20Regency%20Atlanta?rooms=1&adults=1&'
        f'checkinDate={START_DATE}&checkoutDate={END_DATE}&'
        'rate=Standard&kids=0'
    )

    with Browser() as browser:
        browser.get(URL)

        try:
            not_available_warning = browser.find_element_by_css_selector('.alert-warn')
            print(not_available_warning.text)
        except NoSuchElementException:
            return True
        return False

def is_hilton_available() -> bool:
    START_DATE, END_DATE = '30 Aug 2018', '03 Sep 2018'
    URL = 'http://www3.hilton.com/en/hotels/georgia/hilton-atlanta-ATLAHHH/index.html'

    with Browser() as browser:
        browser.get(URL)
    
        start_date = browser.find_element_by_css_selector('[name=arrivalDate]')
        end_date = browser.find_element_by_css_selector('[name=departureDate]')
    
        set_element_value(browser, start_date, START_DATE)
        set_element_value(browser, end_date, END_DATE)
        browser.execute_script("jQuery('#frmfindHotel').submit()")
    
        try:
            not_available_warning = browser.find_element_by_css_selector('.alertBox.alert')
            print(not_available_warning.text)
        except NoSuchElementException:
            return True
        return False


def is_mariott_available() -> bool:
    raise NotImplementedError


def is_sharaton_available() -> bool:
    raise NotImplementedError


def is_westin_available() -> bool:
    raise NotImplementedError


if __name__ == '__main__':
    is_hyatt_available()
    is_hilton_available()
