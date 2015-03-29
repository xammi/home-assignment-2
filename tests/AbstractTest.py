__author__ = 'max'

import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class AbstractTestCase(unittest.TestCase):
    BROWSER_LOC = "TTHA2BROWSER"
    PASSWORD_LOC = "TTHA2PASSWORD"

    def setUp(self):
        browser = os.environ.get(self.BROWSER_LOC, 'CHROME')

        self.driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=getattr(DesiredCapabilities, browser).copy(),
        )

    def tearDown(self):
        self.driver.quit()