__author__ = 'max'

import os
import AbstractTest
from page_objects.MainPage import MainPage


class MainTestCase(AbstractTest):
    def test_auth_ok(self):
        username = "ftest%s@tech-mail.ru" % 18
        password = os.environ.get(self.PASSWORD_LOC)

        mainpage = MainPage(self.driver)
        mainpage.open()

        item = mainpage.login(username, password)
        self.assertEqual(username, item.text)