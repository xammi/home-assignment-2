# coding: utf-8
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

__author__ = 'max'

from abstract import AbstractPage


class Tags:
    BOLD = {
        'selector': '.markdown-editor-icon-bold',
        'text': u'**Жирный текст**',
        'markdown': u'****',
        'html': u'<strong>Жирный текст</strong>'
    }
    ITALIC = {
        'selector': '.markdown-editor-icon-italic',
        'text': u'*Курсив*',
        'markdown': u'**',
        'html': u'<em>Курсив</em>'
    }
    QUOTES = {
        'selector': '.markdown-editor-icon-quote',
        'text': u'> Цитата',
        'markdown': u'> ',
        'html': u'&gt; Цитата'
    }
    LIST = {
        'selector': '.markdown-editor-icon-unordered-list',
        'text': u'* Список',
        'markdown': u'* ',
        'html': u'<ul>\n<li>Список</li>\n</ul>'
    }
    NUM_LIST = {
        'selector': '.markdown-editor-icon-ordered-list',
        'text': u'1. Нумерованный список',
        'markdown': u'1. ',
        'html': u'<ol>\n<li>Нумерованный список</li>\n</ol>'
    }


class CreateTopicPage(AbstractPage):
    PATH = '/blog/topic/create/'

    TITLE_INP = u'//input[@name="title"]'
    SHORT_TEXT_INP = u'//*[@id="content"]/div/div[1]/form/div/div[3]'
    SHORT_TEXT_GET = u'//div[@class="CodeMirror-code"]/pre'
    TEXT_INP = u'//*[@id="content"]/div/div[1]/form/div/div[6]'
    SUBMIT_BTN = u'//button[@type="submit"]'

    BLOG_SELECT = '#id_blog_chzn>.chzn-single'
    BLOG_OPTION = '#id_blog_chzn .active-result:nth-child(%s)'

    ERROR_CLASS = '.system-message-error'
    FORBID_COMMENT_CHB = '#id_forbid_comment'
    PUBLISH_CHB = '#id_publish'

    def __init__(self, driver):
        super(CreateTopicPage, self).__init__(driver)

    def click_tag(self, selector):
        self.driver.find_element_by_css_selector(selector).click()

    def _select_blog_by_id(self, blog_id):
        if blog_id > 0:
            self.driver.find_element_by_css_selector(self.BLOG_SELECT).click()
            self.driver.find_element_by_css_selector(self.BLOG_OPTION % blog_id).click()

    def create(self, title, blog_id, short_text, text, comments=True, publish=True):
        self._select_blog_by_id(blog_id)
        self.driver.find_element_by_xpath(self.TITLE_INP).send_keys(title)

        self.driver.find_element_by_xpath(self.SHORT_TEXT_INP).click()
        ActionChains(self.driver).send_keys(short_text).perform()

        self.driver.find_element_by_xpath(self.TEXT_INP).click()
        ActionChains(self.driver).send_keys(text).perform()

        if not comments:
            self.driver.find_element_by_css_selector(self.FORBID_COMMENT_CHB).click()

        if not publish:
            self.driver.find_element_by_css_selector(self.PUBLISH_CHB).click()

        self.driver.find_element_by_xpath(self.SUBMIT_BTN).submit()

    def has_error(self):
        return self.wait(
            lambda driver: driver.find_element_by_css_selector(self.ERROR_CLASS).is_displayed()
        )

    def get_short_text(self):
        return self.wait(
            lambda driver: driver.find_element_by_xpath(self.SHORT_TEXT_GET).text
        )


class TopicPage(AbstractPage):
    DELETE_BTN = u'//a[@class="actions-delete"]'
    DELETE_CONFIRM = u'//input[@value="Удалить"]'

    TOPIC_TITLE = 'topic-title'
    TOPIC_CONTENT = 'topic-content'
    TOPIC_BLOG = 'topic-blog'

    COMMENT_ADD_LINK = 'comment-add-link'

    def __init__(self, driver):
        super(TopicPage, self).__init__(driver)

    def get_title(self):
        return self.driver.find_element_by_class_name(self.TOPIC_TITLE).text

    def get_content(self):
        return self.driver.find_element_by_class_name(self.TOPIC_CONTENT).text

    def get_html_content(self):
        return self.driver.find_element_by_class_name(self.TOPIC_CONTENT).get_attribute('innerHTML')

    def open_blog(self):
        self.driver.find_element_by_class_name(self.TOPIC_BLOG).click()

    def delete(self):
        self.driver.find_element_by_xpath(self.DELETE_BTN).click()
        self.driver.find_element_by_xpath(self.DELETE_CONFIRM).click()

    def comment_add_link_is_displayed(self):
        try:
            self.driver.find_element_by_class_name(self.COMMENT_ADD_LINK)
        except NoSuchElementException:
            return False
        return True