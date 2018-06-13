from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class Browser:
    def __init__(self):
        self.options = Options()
        self.options.set_headless(headless=True)
        self.browser = webdriver.Chrome(chrome_options=self.options)
    
    def __enter__(self):
        return self.browser

    def __exit__(self, *exc_details):
        self.browser.close()


def set_element_value(driver, element, value):
    driver.execute_script(f"arguments[0].value = '{value}'", element)


def set_element_text(driver, element, value):
    driver.execute_script(f"arguments[0].innerText = '{value}'", element)
