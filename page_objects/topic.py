# coding: utf-8
__author__ = 'max'

from abstract import AbstractPage
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
    IMAGE = {
        'selector': '//*[contains(@class, "markdown-editor-icon-image")][1]',
        'text': '![](image.png)',
        'markdown': '![](',
        'html': '<img'
    }
    LINK = {
        'selector': '//*[contains(@class, "markdown-editor-icon-link")][1]',
        'text': '[name](http://test.ru "title")',
        'markdown': '[](http://test.ru)',
        'html': '<a href="http://test.ru'
    }
    LINK_PROFILE = {
        'selector': '//*[contains(@class, "markdown-editor-icon-link")][2]',
        'text': u'[Господин Почтмейстер](/profile/g.pochtmejster/)',
        'markdown': '[Господин Почтмейстер](/profile/g.pochtmejster/)',
        'html': '<a href="/profile/g.pochtmejster/">'
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

    SEARCH_USER_INP = '#search-user-login-popup'
    USER_PROFILE_LINK = '.realname>.user_profile_path'

    ADD_POLL_CHB = '//*[@name="add_poll"]'
    POLL_QUESTION_INP = '#id_question'
    POLL_ANSWER1_INP = '#id_form-0-answer'
    POLL_ANSWER2_INP = '#id_form-1-answer'
    POLL_ANSWER3_INP = '//*[contains(@id, "id_form-2-answer")][2]'
    ADD_POLL_ANSWER = '.add-poll-answer'
    DELETE_POLL_ANSWER = '//*[@id="question_list"]/li[3]/a'

    def __init__(self, driver):
        super(CreateTopicPage, self).__init__(driver)

    def click_tag(self, selector, by_xpath):
        if by_xpath:
            self.driver.find_element_by_xpath(selector).click()
        else:
            self.driver.find_element_by_css_selector(selector).click()

    def _select_blog_by_id(self, blog_id):
        if blog_id > 0:
            self.driver.find_element_by_css_selector(self.BLOG_SELECT).click()
            self.driver.find_element_by_css_selector(self.BLOG_OPTION % blog_id).click()

    def create(self, title, blog_id, short_text, text, comments=True, publish=True, polls=None):
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

        self.set_add_poll_true()
        if polls:
            self.driver.find_element_by_css_selector(self.POLL_QUESTION_INP).send_keys(polls[0])
            self.driver.find_element_by_css_selector(self.POLL_ANSWER1_INP).send_keys(polls[1])
            self.driver.find_element_by_css_selector(self.POLL_ANSWER2_INP).send_keys(polls[2])

        self.driver.find_element_by_xpath(self.SUBMIT_BTN).submit()

    def has_error(self):
        return self.wait(
            lambda driver: driver.find_element_by_css_selector(self.ERROR_CLASS).is_displayed()
        )

    def get_short_text(self):
        return self.wait(
            lambda driver: driver.find_element_by_xpath(self.SHORT_TEXT_GET).text
        )

    def set_profile(self, profile_name):
        self.driver.find_element_by_css_selector(self.SEARCH_USER_INP).send_keys(profile_name)
        self.wait(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.USER_PROFILE_LINK)))
        self.wait(
            lambda driver: driver.find_element_by_css_selector(self.USER_PROFILE_LINK).is_displayed()
        )
        self.driver.find_element_by_css_selector(self.USER_PROFILE_LINK).click()

    #--------------polls----------------------

    def set_add_poll_true(self):
        self.driver.find_element_by_xpath(self.ADD_POLL_CHB).click()

    def add_answer_for_poll(self):
        self.driver.find_element_by_css_selector(self.ADD_POLL_ANSWER).click()

    def delete_answer_for_poll(self):
        self.driver.find_element_by_xpath(self.DELETE_POLL_ANSWER).click()

    def new_answer_is_displayed(self, wait=True):
        try:
            if wait:
                return self.wait(
                    lambda driver: driver.find_element_by_xpath(self.POLL_ANSWER3_INP).is_displayed()
                )
            else:
                return self.driver.find_element_by_xpath(self.POLL_ANSWER3_INP).is_displayed()

        except Exception:
            return False


class TopicPage(AbstractPage):
    DELETE_BTN = u'//a[@class="actions-delete"]'
    DELETE_CONFIRM = u'//input[@value="Удалить"]'

    TOPIC_TITLE = 'topic-title'
    TOPIC_CONTENT = 'topic-content'
    TOPIC_BLOG = 'topic-blog'

    COMMENT_ADD_LINK = 'comment-add-link'

    ANSWER_1_LBL = '//*[@class=("poll-vote")]/li[1]/label'
    ANSWER_2_LBL = '//*[@class=("poll-vote")]/li[2]/label'

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

    def get_poll_answers(self):
        return [
            self.driver.find_element_by_xpath(self.ANSWER_1_LBL).text,
            self.driver.find_element_by_xpath(self.ANSWER_2_LBL).text,
        ]