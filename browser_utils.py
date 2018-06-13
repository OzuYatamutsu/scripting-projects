from selenium.webdriver.firefox.options import Options
from selenium import webdriver


class Browser:
    def __init__(self):
        # self.browser = webdriver.Chrome()
        self.options = Options()
        self.options.set_headless(headless=True)
        self.browser = webdriver.Firefox(firefox_options=self.options)
    
    def __enter__(self):
        return self.browser

    def __exit__(self, *exc_details):
        self.browser.close()


def set_element_value(driver, element, value):
    driver.execute_script(f"arguments[0].value = '{value}'", element)


def set_element_text(driver, element, value):
    driver.execute_script(f"arguments[0].innerText = '{value}'", element)
