# coding: utf-8
__author__ = 'max'

from AbstractPage import AbstractPage


class IndexPage(AbstractPage):
    LOGIN_BTN = u'//a[text()="Вход для участников"]'
    LOGIN_INP = u'//input[@name="login"]'
    PASSWORD_INP = u'//input[@name="password"]'
    SUBMIT_BTN = u'//span[text()="Войти"]'
    USERNAME = u'//a[@class="username"]'

    def __init__(self, driver):
        super(IndexPage, self).__init__(driver)

    def _show_login_form(self):
        self.driver.find_element_by_xpath(self.LOGIN_BTN).click()

    def login(self, username, password):
        self._show_login_form()

        self.driver.find_element_by_xpath(self.LOGIN_INP).send_keys(username)
        self.driver.find_element_by_xpath(self.PASSWORD_INP).send_keys(password)
        self.driver.find_element_by_xpath(self.SUBMIT_BTN).submit()

        return self.wait(
            lambda driver: driver.find_element_by_xpath(self.USERNAME)
        )