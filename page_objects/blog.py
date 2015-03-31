# coding: utf-8
__author__ = 'max'

from abstract import AbstractPage


class BlogPage(AbstractPage):
    PATH = '/blog/show/2544/fludilka/'

    TOPIC_TITLE = u'//h1[@class="topic-title"]/a'
    TOPIC_REMOVE = u'//a[text()="Удалить"]'
    EXACTLY_REMOVE = u'//input[@value="Удалить"]'

    def __init__(self, driver):
        super(BlogPage, self).__init__(driver)

    def get_upper_topic_title(self):
        return self.driver.find_element_by_xpath(self.TOPIC_TITLE).text

    def remove_upper(self):
        self.driver.find_element_by_xpath(self.TOPIC_REMOVE).click()
        self.wait(
            lambda driver: driver.find_element_by_xpath(self.EXACTLY_REMOVE).is_displayed()
        )
        self.driver.find_element_by_xpath(self.EXACTLY_REMOVE).submit()