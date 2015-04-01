__author__ = 'max'


from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urlparse


class AbstractPage(object):
    BASE_URL = "http://ftest.stud.tech-mail.ru"
    TIMEOUT = 30
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()

    def wait(self, condition):
        waiter = WebDriverWait(self.driver, self.TIMEOUT)
        return waiter.until(condition)

    def set_text_to_alert(self, text):
        self.wait(EC.alert_is_present())
        alert = self.driver.switch_to_alert()
        alert.send_keys(text)
        alert.accept()