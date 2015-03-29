__author__ = 'max'


from selenium.webdriver.support.wait import WebDriverWait
import urlparse


class AbstractPage(object):
    BASE_URL = "http://ftest.stud.tech-mail.ru"
    TIMEOUT = 10
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