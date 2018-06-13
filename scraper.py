from selenium.common.exceptions import NoSuchElementException
from browser_utils import Browser, set_element_value, set_element_text
from logging import getLogger, StreamHandler
from time import sleep
from sys import stdout

log = getLogger(__name__)
log.addHandler(StreamHandler(stdout))


def is_hyatt_available() -> tuple:
    START_DATE, END_DATE = '2018-08-30', '2018-09-03'
    URL = (
        'https://www.hyatt.com/en-US/search/Hyatt%20Regency%20Atlanta?rooms=1&adults=1&'
        f'checkinDate={START_DATE}&checkoutDate={END_DATE}&'
        'rate=Standard&kids=0'
    )

    with Browser() as browser:
        browser.get(URL)

        try:
            sleep(3)
            not_available_warning = browser.find_element_by_css_selector('.alert-warn')
            return False, not_available_warning.text
        except NoSuchElementException:
            return True, "AVAILABLE"
        return False

def is_hilton_available() -> tuple:
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
            sleep(3)
            not_available_warning = browser.find_element_by_css_selector('.alertBox.alert')
            return False, not_available_warning.text
        except NoSuchElementException:
            return True, "AVAILABLE"


def is_mariott_available() -> tuple:
    START_DATE, END_DATE = '08/30/2018'.replace('/', '%2F'), '09/03/2018'.replace('/', '%2F')
    URL = (
        'https://www.marriott.com/search/default.mi?roomCount=1&'
        f'fromDate={START_DATE}&toDate={END_DATE}&'
        'numAdultsPerRoom=1&propertyCode=atlmq&'
        'destinationAddress.location=265+Peachtree+Center+Avenue%2C+Atlanta%2C+GA%2C+30303%2C+US'
    )

    with Browser() as browser:
        browser.get(URL)
        browser.find_element_by_id('edit-search-form').submit()
        try:
            sleep(3)
            not_available_warning = browser.find_element_by_class_name('l-error-Container')
            return False, not_available_warning.text
        except NoSuchElementException:
            # Available. Get price below:
            try:
                lowest_rate = float(browser.find_element_by_css_selector(
                    '[href="/reservation/availabilitySearch.mi?propertyCode=ATLMQ&isSearch=true&currency="] '
                    '> .rate-block > .price-night > .t-price'
                ).text.strip())
            except Exception:
                lowest_rate = 9999.9
            return True, f"${lowest_rate}/night" if lowest_rate != 9999.9 else "AVAILABLE"
        

def is_sharaton_available() -> tuple:
    START_DATE, END_DATE = '08/30/2018'.replace('/', '%2F'), '09/03/2018'.replace('/', '%2F')
    URL = (
        'https://www.starwoodhotels.com/preferredguest/room/index.html?propertyID=1144&language=en_US&'
        'localeCode=en_US&ES=LPS_1144_EN_SI_BOOKWIDGET_SOUTH_NAD&'
        f'arrivalDate={START_DATE}&departureDate={END_DATE}'
    )

    with Browser() as browser:
        browser.get(URL)
    
        try:
            sleep(3)
            not_available_warning = browser.find_element_by_class_name('altAvailabilityMsg')
            return False, not_available_warning.text
        except NoSuchElementException:
            # Available. Get price below:
            lowest_rate = 9999.9
            for rate in browser.find_elements_by_class_name('roomRate'):
                rate = float(rate.text.replace('USD', '').strip())
                if rate < lowest_rate:
                    lowest_rate = rate
            return True, f"${lowest_rate}/night" if lowest_rate != 9999.9 else "AVAILABLE"


def is_westin_available() -> tuple:
    START_DATE, END_DATE = '08/30/2018'.replace('/', '%2F'), '09/03/2018'.replace('/', '%2F')
    URL = (
        'https://www.starwoodhotels.com/preferredguest/room/index.html?propertyID=1023&language=en_US&'
        'localeCode=en_US&ES=LPS_1023_EN_SI_BOOKWIDGET_SOUTH_NAD&'
        f'arrivalDate={START_DATE}&departureDate={END_DATE}'
    )

    with Browser() as browser:
        browser.get(URL)
    
        try:
            sleep(3)
            not_available_warning = browser.find_element_by_class_name('altAvailabilityMsg')
            return False, not_available_warning.text
        except NoSuchElementException:
            # Available. Get price below:
            sleep(1)
            lowest_rate = 9999.9
            for rate in browser.find_elements_by_class_name('roomRate'):
                rate = float(rate.text.replace('USD', '').strip())
                if rate < lowest_rate:
                    lowest_rate = rate
            return True, f"${lowest_rate}/night" if lowest_rate != 9999.9 else "AVAILABLE"


if __name__ == '__main__':
    print(' - '.join([str(value) for value in is_hyatt_available()]))
    print(' - '.join([str(value) for value in is_hilton_available()]))
    print(' - '.join([str(value) for value in is_mariott_available()]))
    print(' - '.join([str(value) for value in is_sharaton_available()]))
    print(' - '.join([str(value) for value in is_westin_available()]))
