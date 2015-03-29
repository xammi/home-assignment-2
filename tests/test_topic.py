# coding: utf-8
__author__ = 'max'

from abstract import AbstractTestCase
from page_objects.topic import CreateTopicPage, TopicPage


class TopicTestCase(AbstractTestCase):
    TITLE_BOUNDARY = 250

    DEFAULT_TITLE = u'Мой собственный топик'
    DEFAULT_SHORT_TEXT = u'Короткое описание'
    DEFAULT_TEXT = u'Полное описание топика'
    DEFAULT_BLOG = 2

    def setUp(self):
        super(TopicTestCase, self).setUp()
        self.login()

    def test_create_ok(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(self.DEFAULT_TITLE, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, self.DEFAULT_TEXT)

        topicpage = TopicPage(self.driver)
        self.assertEqual(topicpage.get_title(), self.DEFAULT_TITLE)
        self.assertEqual(topicpage.get_content(), self.DEFAULT_TEXT)

    # def test_create_title_boundary(self):
    #     title = 'x' * self.TITLE_BOUNDARY
    #
    #     topicpage = CreateTopicPage(self.driver)
    #     topicpage.open()
    #     topicpage.create(title, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, self.DEFAULT_TEXT)
    #
    #     self.assertEqual(topicpage.get_title(), title)
    #
    # def test_create_without_blog(self):
    #     topicpage = CreateTopicPage(self.driver)
    #     topicpage.open()
    #     topicpage.create(self.DEFAULT_TITLE, -1, self.DEFAULT_SHORT_TEXT, self.DEFAULT_TEXT)
    #     self.assertTrue(topicpage.has_error())
    #
    # def test_create_without_title(self):
    #     topicpage = CreateTopicPage(self.driver)
    #     topicpage.open()
    #     topicpage.create(u'', self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, self.DEFAULT_TEXT)
    #     self.assertTrue(topicpage.has_error())
    #
    # def test_create_without_short_text(self):
    #     topicpage = CreateTopicPage(self.driver)
    #     topicpage.open()
    #     topicpage.create(self.DEFAULT_TITLE, self.DEFAULT_BLOG, u'', self.DEFAULT_TEXT)
    #     self.assertTrue(topicpage.has_error())
    #
    # def test_create_without_text(self):
    #     topicpage = CreateTopicPage(self.driver)
    #     topicpage.open()
    #     topicpage.create(self.DEFAULT_TITLE, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, u'')
    #     self.assertTrue(topicpage.has_error())
    #
    # def test_create_title_long(self):
    #     title = 'x' * (self.TITLE_BOUNDARY + 1)
    #
    #     topicpage = CreateTopicPage(self.driver)
    #     topicpage.open()
    #     topicpage.create(title, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, self.DEFAULT_TEXT)
    #     self.assertTrue(topicpage.has_error())
