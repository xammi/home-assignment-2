# coding: utf-8
__author__ = 'max'

import os
from abstract import AbstractTestCase
from page_objects.topic import CreateTopicPage, TopicPage, Tags
from page_objects.blog import BlogPage


def not_created(method):
    def wrapper(self, *args, **kwargs):
        self.topic_created = False
        return method(self, *args, **kwargs)
    return wrapper


class CreateTopicTestCase(AbstractTestCase):
    TITLE_BOUNDARY = 250

    DEFAULT_TITLE = u'Мой собственный топик'
    DEFAULT_SHORT_TEXT = u'Короткое описание'
    DEFAULT_TEXT = u'Полное описание топика'
    DEFAULT_BLOG = 2

    PATH_TO_IMAGE = os.path.dirname(__file__) + '/imgs/img.jpg'
    LINK = "http://test.ru"
    PROFILE_NAME = u'Почтмейстер'

    POLL_QUESTION = u'Вопрос для голосования'
    POLL_ANSWER_1 = u'Answer1'
    POLL_ANSWER_2 = u'Answer2'

    def setUp(self):
        super(CreateTopicTestCase, self).setUp()
        self.login()
        self.topic_created = True

    def tearDown(self):
        if self.topic_created:
            blogpage = BlogPage(self.driver)
            blogpage.open()
            blogpage.remove_upper()

        super(CreateTopicTestCase, self).tearDown()

    def test_create_ok(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(self.DEFAULT_TITLE, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, self.DEFAULT_TEXT)

        topicpage = TopicPage(self.driver)
        self.assertEqual(topicpage.get_title(), self.DEFAULT_TITLE)
        self.assertEqual(topicpage.get_content(), self.DEFAULT_TEXT)

    def test_create_title_boundary(self):
        title = 'x' * self.TITLE_BOUNDARY

        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(title, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, self.DEFAULT_TEXT)

        topicpage = TopicPage(self.driver)
        self.assertEqual(topicpage.get_title(), title)

    @not_created
    def test_create_without_blog(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(self.DEFAULT_TITLE, -1, self.DEFAULT_SHORT_TEXT, self.DEFAULT_TEXT)
        self.assertTrue(topicpage.has_error())

    @not_created
    def test_create_without_title(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(u'', self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, self.DEFAULT_TEXT)
        self.assertTrue(topicpage.has_error())

    @not_created
    def test_create_without_short_text(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(self.DEFAULT_TITLE, self.DEFAULT_BLOG, u'', self.DEFAULT_TEXT)
        self.assertTrue(topicpage.has_error())

    @not_created
    def test_create_without_text(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(self.DEFAULT_TITLE, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, u'')
        self.assertTrue(topicpage.has_error())

    @not_created
    def test_create_title_long(self):
        title = 'x' * (self.TITLE_BOUNDARY + 1)

        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(title, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, self.DEFAULT_TEXT)
        self.assertTrue(topicpage.has_error())

    def test_create_forbid_comment(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(self.DEFAULT_TITLE, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT,
                         self.DEFAULT_TEXT, comments=False)

        topicpage = TopicPage(self.driver)
        self.assertFalse(topicpage.comment_add_link_is_displayed())

    @not_created
    def test_create_publish_false(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(self.DEFAULT_TITLE, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT,
                         self.DEFAULT_TEXT, publish=False)

        topicpage = TopicPage(self.driver)
        topicpage.open_blog()

        blogpage = BlogPage(self.driver)
        self.assertNotEqual(blogpage.get_upper_topic_title(), self.DEFAULT_TITLE)

    class Meta:
        @staticmethod
        def base_test_tag(self, tag, equal=True, by_xpath=False, alert_text=None):
            topicpage = CreateTopicPage(self.driver)
            topicpage.open()
            topicpage.click_tag(tag['selector'], by_xpath)

            if alert_text:
                topicpage.set_text_to_alert(alert_text)

            if equal:
                self.assertEqual(tag['markdown'], topicpage.get_short_text())
            else:
                self.assertIn(tag['markdown'], topicpage.get_short_text())

        @staticmethod
        def base_test_create_tag(self, tag):
            topicpage = CreateTopicPage(self.driver)
            topicpage.open()
            topicpage.create(self.DEFAULT_TITLE, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, tag['text'])

            topicpage = TopicPage(self.driver)
            self.assertIn(tag['html'], topicpage.get_html_content())

    @not_created
    def test_tag_bold(self):
        self.Meta.base_test_tag(self, Tags.BOLD)

    def test_create_tag_bold(self):
        self.Meta.base_test_create_tag(self, Tags.BOLD)

    @not_created
    def test_tag_italic(self):
        self.Meta.base_test_tag(self, Tags.ITALIC)

    def test_create_tag_italic(self):
        self.Meta.base_test_create_tag(self, Tags.ITALIC)

    @not_created
    def test_tag_quotes(self):
        self.Meta.base_test_tag(self, Tags.QUOTES)

    def test_create_tag_quotes(self):
        self.Meta.base_test_create_tag(self, Tags.QUOTES)

    @not_created
    def test_tag_list(self):
        self.Meta.base_test_tag(self, Tags.LIST)

    def test_create_tag_list(self):
        self.Meta.base_test_create_tag(self, Tags.LIST)

    @not_created
    def test_tag_num_list(self):
        self.Meta.base_test_tag(self, Tags.NUM_LIST)

    def test_create_tag_num_list(self):
        self.Meta.base_test_create_tag(self, Tags.NUM_LIST)

    @not_created
    def test_tag_image(self):
        self.Meta.base_test_tag(self, Tags.IMAGE, equal=False, by_xpath=True, alert_text=self.PATH_TO_IMAGE)

    def test_tag_create_image(self):
        self.Meta.base_test_create_tag(self, Tags.IMAGE)

    @not_created
    def test_tag_link(self):
        self.Meta.base_test_tag(self, Tags.LINK, equal=False,  by_xpath=True, alert_text=self.LINK)

    def test_tag_create_link(self):
        self.Meta.base_test_create_tag(self, Tags.LINK)

    @not_created
    def test_tag_link_profile(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.click_tag(Tags.LINK_PROFILE['selector'], True)
        topicpage.set_profile(self.PROFILE_NAME)
        self.assertIn(Tags.LINK_PROFILE['markdown'], topicpage.get_short_text())

    def test_tag_create_link_profile(self):
        self.Meta.base_test_create_tag(self, Tags.LINK_PROFILE)

    def test_create_poll(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(self.DEFAULT_TITLE, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, self.DEFAULT_TEXT,
                         polls=[self.POLL_QUESTION, self.POLL_ANSWER_1, self.POLL_ANSWER_2])

        topicpage = TopicPage(self.driver)
        answers = topicpage.get_poll_answers()
        self.assertIn(answers[0], self.POLL_ANSWER_1)
        self.assertIn(answers[1], self.POLL_ANSWER_2)

    @not_created
    def test_add_poll_answer(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()

        topicpage.set_add_poll_true()
        topicpage.add_answer_for_poll()
        self.assertTrue(topicpage.new_answer_is_displayed())

        topicpage.delete_answer_for_poll()
        self.assertFalse(topicpage.new_answer_is_displayed(wait=False))


class RemoveTopicTestCase(AbstractTestCase):
    DEFAULT_TITLE = u'Топик на удаление'
    DEFAULT_SHORT_TEXT = u'Короткое описание'
    DEFAULT_TEXT = u'Полное описание топика'
    DEFAULT_BLOG = 2

    def setUp(self):
        super(RemoveTopicTestCase, self).setUp()
        self.login()

    def test_remove_topic_ok(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(self.DEFAULT_TITLE, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, self.DEFAULT_TEXT)

        blogpage = BlogPage(self.driver)
        blogpage.open()
        upper_title = blogpage.get_upper_topic_title()
        blogpage.remove_upper()

        self.assertNotEqual(blogpage.get_upper_topic_title(), upper_title)
