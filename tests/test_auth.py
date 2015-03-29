# coding: utf-8
__author__ = 'max'

import os
from abstract import AbstractTestCase


class AuthTestCase(AbstractTestCase):
    def test_auth_ok(self):
        email = "ftest%s@tech-mail.ru" % 18
        username = u'Господин Почтмейстер'
        password = os.environ.get(self.PASSWORD_LOC)

        item = self.authenticate(email, password)
        self.assertEqual(username, item.text)