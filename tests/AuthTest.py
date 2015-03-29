# coding: utf-8
__author__ = 'max'

import os
from AbstractTest import AbstractTestCase
from page_objects.IndexPage import IndexPage


class AuthTestCase(AbstractTestCase):
    def test_auth_ok(self):
        email = "ftest%s@tech-mail.ru" % 18
        username = u'Господин Почтмейстер'
        password = os.environ.get(self.PASSWORD_LOC)

        mainpage = IndexPage(self.driver)
        mainpage.open()

        item = mainpage.login(email, password)
        self.assertEqual(username, item.text)