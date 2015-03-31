# coding: utf-8
from selenium.webdriver import ActionChains

__author__ = 'max'

from abstract import AbstractPage


class CreateTopicPage(AbstractPage):
    PATH = '/blog/topic/create/'

    TITLE_INP = u'//input[@name="title"]'
    SHORT_TEXT_INP = u'//*[@id="content"]/div/div[1]/form/div/div[3]'
    TEXT_INP = u'//*[@id="content"]/div/div[1]/form/div/div[6]'
    SUBMIT_BTN = u'//button[@type="submit"]'

    BLOG_SELECT = '#id_blog_chzn>.chzn-single'
    BLOG_OPTION = '#id_blog_chzn .active-result:nth-child(%s)'

    ERROR_CLASS = 'system-message-error'

    def __init__(self, driver):
        super(CreateTopicPage, self).__init__(driver)

    def _select_blog_by_id(self, blog_id):
        if blog_id > 0:
            self.driver.find_element_by_css_selector(self.BLOG_SELECT).click()
            self.driver.find_element_by_css_selector(self.BLOG_OPTION % blog_id).click()

    def create(self, title, blog_id, short_text, text):
        self._select_blog_by_id(blog_id)
        self.driver.find_element_by_xpath(self.TITLE_INP).send_keys(title)

        self.driver.find_element_by_xpath(self.SHORT_TEXT_INP).click()
        ActionChains(self.driver).send_keys(short_text).perform()

        self.driver.find_element_by_xpath(self.TEXT_INP).click()
        ActionChains(self.driver).send_keys(text).perform()

        self.driver.find_element_by_xpath(self.SUBMIT_BTN).submit()

    def has_error(self):
        return self.wait(
            lambda driver: driver.find_element_by_class_name(self.ERROR_CLASS).is_displayed()
        )


class TopicPage(AbstractPage):
    DELETE_BTN = u'//a[@class="actions-delete"]'
    DELETE_CONFIRM = u'//input[@value="Удалить"]'

    TOPIC_TITLE = 'topic-title'
    TOPIC_CONTENT = 'topic-content'
    TOPIC_BLOG = 'topic-blog'

    def __init__(self, driver):
        super(TopicPage, self).__init__(driver)

    def get_title(self):
        return self.driver.find_element_by_class_name(self.TOPIC_TITLE).text

    def get_content(self):
        return self.driver.find_element_by_class_name(self.TOPIC_CONTENT).text

    def open_blog(self):
        self.driver.find_element_by_class_name(self.TOPIC_BLOG).click()

    def delete(self):
        self.driver.find_element_by_xpath(self.DELETE_BTN).click()
        self.driver.find_element_by_xpath(self.DELETE_CONFIRM).click()