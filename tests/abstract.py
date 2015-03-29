__author__ = 'max'

import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from page_objects.index import IndexPage


class AbstractTestCase(unittest.TestCase):
    BROWSER_LOC = "TTHA2BROWSER"
    PASSWORD_LOC = "TTHA2PASSWORD"
    EMAIL = "ftest%s@tech-mail.ru" % 18

    def setUp(self):
        browser = os.environ.get(self.BROWSER_LOC, 'CHROME')

        self.driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=getattr(DesiredCapabilities, browser).copy(),
        )

    def authenticate(self, email, password):
        indexpage = IndexPage(self.driver)
        indexpage.open()
        return indexpage.login(email, password)

    def login(self):
        password = os.environ.get(self.PASSWORD_LOC)
        self.authenticate(self.EMAIL, password)

    def tearDown(self):
        self.driver.quit()