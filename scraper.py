from selenium.common.exceptions import NoSuchElementException
from browser_utils import Browser, set_element_value, set_element_text
from logging import getLogger, StreamHandler
from time import sleep
from sys import stdout

log = getLogger(__name__)
log.addHandler(StreamHandler(stdout))
TIMEOUT_SECS = 10


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
            sleep(TIMEOUT_SECS)
            not_available_warning = browser.find_element_by_css_selector('.alert-warn')
        except NoSuchElementException:
            return True, "AVAILABLE"
        finally:
            browser.save_screenshot('final_state.png')
            with open('.url', 'w') as f:
                f.write(browser.current_url)
        return False, not_available_warning.text


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
            sleep(TIMEOUT_SECS)
            not_available_warning = browser.find_element_by_css_selector('.alertBox.alert')
        except NoSuchElementException:
            return True, "AVAILABLE"
        finally:
            browser.save_screenshot('final_state.png')
            with open('.url', 'w') as f:
                f.write(browser.current_url)
        return False, not_available_warning.text

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
            sleep(TIMEOUT_SECS)
            not_available_warning = browser.find_element_by_class_name('l-error-Container')
        except NoSuchElementException:
            # Might be available. Check for "SOLD OUT" as well
            try:
                not_available_warning = browser.find_element_by_css_selector('[data-marsha="ATLMQ"] > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > .l-sold-out')

            except NoSuchElementException:
                # Available. Get price below:
                try:
                    lowest_rate = float(browser.find_element_by_css_selector(
                        '[href="/reservation/availabilitySearch.mi?propertyCode=ATLMQ&isSearch=true&currency="] '
                        '> .rate-block > .price-night > .t-price'
                    ).text.strip())
                except Exception:
                    lowest_rate = 9999.9
                return True, f"${lowest_rate:.2f}/night" if lowest_rate != 9999.9 else "AVAILABLE"
        finally:
            browser.save_screenshot('final_state.png')
            with open('.url', 'w') as f:
                f.write(browser.current_url)
        return False, not_available_warning.text
        

def is_sharaton_available() -> tuple:
    START_DATE, END_DATE = '08/30/2018'.replace('/', '%2F'), '09/03/2018'.replace('/', '%2F')
    URL = (
        'https://www.starwoodhotels.com/preferredguest/room/index.html?propertyID=1144&language=en_US&'
        'localeCode=en_US&ES=LPS_1144_EN_SI_BOOKWIDGET_SOUTH_NAD&'
        f'arrivalDate={START_DATE}&departureDate={END_DATE}&'
        'rp=RC:DFRLM,RP:SPG,RP:SPGCPN,PC-SN-COMBO:253151'
    )

    with Browser() as browser:
        browser.get(URL)
    
        try:
            sleep(TIMEOUT_SECS)
            not_available_warning = browser.find_element_by_class_name('altAvailabilityMsg')
        except NoSuchElementException:
            # Available. Get price below:
            lowest_rate = 9999.9
            for rate in browser.find_elements_by_class_name('roomRate'):
                rate = float(rate.text.replace('USD', '').strip())
                if rate < lowest_rate:
                    lowest_rate = rate
            return True, f"${lowest_rate:.2f}/night" if lowest_rate != 9999.9 else "AVAILABLE"
        finally:
            browser.save_screenshot('final_state.png')
            with open('.url', 'w') as f:
                f.write(browser.current_url)
        return False, not_available_warning.text


def is_westin_available() -> tuple:
    START_DATE, END_DATE = '08/30/2018'.replace('/', '%2F'), '09/03/2018'.replace('/', '%2F')
    URL = (
        'https://www.starwoodhotels.com/preferredguest/room/index.html?propertyID=1023&language=en_US&'
        'localeCode=en_US&ES=LPS_1023_EN_SI_BOOKWIDGET_SOUTH_NAD&'
        f'arrivalDate={START_DATE}&departureDate={END_DATE}&'
        'rp=RC:DFRLM,RP:SPG,RP:SPGCPN,PC-SN-COMBO:253151'
    )

    with Browser() as browser:
        browser.get(URL)
    
        try:
            sleep(TIMEOUT_SECS)
            not_available_warning = browser.find_element_by_class_name('altAvailabilityMsg')
        except NoSuchElementException:
            # Available. Get price below:
            sleep(TIMEOUT_SECS)
            lowest_rate = 9999.9
            for rate in browser.find_elements_by_class_name('roomRate'):
                rate = float(rate.text.replace('USD', '').strip())
                if rate < lowest_rate:
                    lowest_rate = rate
            return True, f"${lowest_rate:.2f}/night" if lowest_rate != 9999.9 else "AVAILABLE"
        finally:
            browser.save_screenshot('final_state.png')
            with open('.url', 'w') as f:
                f.write(browser.current_url)
        return False, not_available_warning.text


def is_hotel_indigo_available() -> tuple:
    # Month, day
    START_DATE, END_DATE = ('72018', '30'), ('82018', '3')
    URL = (
        'https://www.ihg.com/hotelindigo/hotels/us/en/find-hotels/hotel/list?qDest=Atlanta,%20GA,%20United%20States&'
        f'qCiMy={START_DATE[0]}&qCiD={START_DATE[1]}&qCoMy={END_DATE[0]}&qCoD={END_DATE[1]}&'
        'qAdlt=1&qChld=0&qRms=1&qRtP=6CBARC&qCpid=100857558&qAkamaiCC=US&qSrt=sBR&'
        'qBrs=ic.ki.ul.in.cp.vn.hi.ex.cv.rs.va.cw.sb.ma&qAAR=6CBARC&srb_u=0&qRad=30'
    )

    with Browser() as browser:
        browser.get(URL)
    
        try:
            sleep(TIMEOUT_SECS)
            not_available_warning = browser.find_element_by_class_name('rate')\
                .find_element_by_class_name('noAvailabilityContainer')
        except NoSuchElementException:
            # Available. Get price below:
            sleep(TIMEOUT_SECS)
            dollars = browser.find_elements_by_class_name('[data-slnm-ihg="rateValue"]').text
            try:
                cents = browser.find_elements_by_class_name('[data-slnm-ihg="rateDecimalValue"]').text 
            except Exception as e:
                cents = '0'
            lowest_rate = f'{dollars}.{cents}'
            return True, f"${lowest_rate:.2f}/night" if lowest_rate != 9999.9 else "AVAILABLE"
        finally:
            browser.save_screenshot('final_state.png')
            with open('.url', 'w') as f:
                f.write(browser.current_url)
        return False, not_available_warning.text


if __name__ == '__main__':
    print(' - '.join([str(value) for value in is_hyatt_available()]))
    print(' - '.join([str(value) for value in is_hilton_available()]))
    print(' - '.join([str(value) for value in is_mariott_available()]))
    print(' - '.join([str(value) for value in is_sharaton_available()]))
    print(' - '.join([str(value) for value in is_westin_available()]))
    print(' - '.join([str(value) for value in is_hotel_indigo_available()]))
