import six
from url_paginator import UrlPaginator
from unittest import TestCase


class UrlPaginationTest(TestCase):

    def test_pages(self):
        pager = UrlPaginator('/search', list(range(50)), 10)
        pages = pager.pages()
        self.assertEqual(4, len(pages))

        pages = pager.page(2).pages()
        self.assertEqual(5, len(pages))

        pages = pager.page(5).pages()
        self.assertEqual(4, len(pages))

    def test_no_page_on_first_page(self):
        pager = UrlPaginator('/search', list(range(50)), 10)
        first = pager.pages()[0]
        self.assertEqual("/search", first['url'])
        self.assertEqual("", first['query'])

    def test_has_page_on_non_first_page(self):
        pager = UrlPaginator('/search', list(range(50)), 10)
        second = pager.pages()[1]
        self.assertEqual("/search?page=2", second['url'])
        self.assertEqual(2, second['number'])

    def test_has_next(self):

        pager = UrlPaginator('/search', list(range(11)), 10)
        self.assertTrue(pager.has_next())

        pager = UrlPaginator('/search', object_list=list(range(10)), per_page=10)
        self.assertFalse(pager.has_next())

    def test_has_prev(self):
        pager = UrlPaginator('/search', object_list=list(range(10)), per_page=10)
        self.assertFalse(pager.has_prev())

        pager = UrlPaginator('/search', object_list=list(range(11)), per_page=10)
        self.assertTrue(pager.page(2).has_prev())

    def test_iterable(self):
        pager = UrlPaginator('/search', object_list=list(range(20)), per_page=10)
        i = iter(pager)
        self.assertEqual(0, six.next(i))



