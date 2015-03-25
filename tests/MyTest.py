__author__ = 'max'

import unittest
import os
from selenium import webdriver


class MyTestCase(unittest.TestCase):
    ROOT_URL = "https://ftest.stud.tech-mail.ru"
    LOGIN = "ftest%s@tech-mail.ru" % 18
    PASSWORD_LOC = "TTHA2BROWSER"

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test(self):
        authpage = self.driver.get(self.ROOT_URL)
        password = os.environ(self.PASSWORD_LOC)

    def tearDown(self):
        self.driver.quit()