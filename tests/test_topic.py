# coding: utf-8
from page_objects.blog import BlogPage

__author__ = 'max'

from abstract import AbstractTestCase
from page_objects.topic import CreateTopicPage, TopicPage, Tags


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

    @not_created
    def test_tag_bold(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.click_tag(Tags.BOLD['selector'])
        self.assertEqual(topicpage.get_short_text(), Tags.BOLD['markup'])

    def test_create_tag_bold(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(self.DEFAULT_TITLE, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, Tags.BOLD['text'])

        topicpage = TopicPage(self.driver)
        self.assertIn(Tags.BOLD['html'], topicpage.get_html_content())

    @not_created
    def test_tag_italic(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.click_tag(Tags.ITALIC['selector'])
        self.assertEqual(topicpage.get_short_text(), Tags.ITALIC['markup'])

    def test_create_tag_italic(self):
        topicpage = CreateTopicPage(self.driver)
        topicpage.open()
        topicpage.create(self.DEFAULT_TITLE, self.DEFAULT_BLOG, self.DEFAULT_SHORT_TEXT, Tags.ITALIC['text'])

        topicpage = TopicPage(self.driver)
        self.assertIn(Tags.ITALIC['html'], topicpage.get_html_content())


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
