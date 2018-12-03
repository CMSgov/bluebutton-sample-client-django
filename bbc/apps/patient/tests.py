from django.test import TestCase

from .views import paging_params, query_params


class paging_paramsTestCase(TestCase):
    def test_no_qd(self):
        """
        paging_params receives no value
        """
        result = paging_params()

        expect = {}

        self.assertEqual(result, expect)

    def test_qd_1(self):
        """
        paging params receives a dict
        1. with startIndex

        :return:
        """

        result = paging_params({'startIndex': "0"})
        expect = {'startIndex': "0"}

        self.assertEqual(result, expect)

    def test_qd_2(self):
        """
        paging params receives a dict

        2. with count
        :return:
        """

        result = paging_params({'count': "10"})
        expect = {'count': "10"}

        self.assertEqual(result, expect)

    def test_qd_3(self):
        """
        paging params receives a dict
        3. with count and startIndex
        :return:
        """

        result = paging_params({'startIndex': "0", 'count': "10"})
        expect = {'startIndex': "0", 'count': "10"}

        self.assertEqual(result, expect)

    def test_qd_4(self):
        """
        paging params receives a dict
        4. dict but no count or startIndex
        :return:
        """

        result = paging_params({'_format': "json"})
        expect = {}

        self.assertEqual(result, expect)


class url_query_TestCase(TestCase):
    def test_no_url(self):
        """
        Test when no url is passed
        :return:
        """

        result = query_params()
        expect = {}

        self.assertEqual(result, expect)

    def test_url_no_query(self):
        """
        Test when url with no query parameters
        :return:
        """
        url = "http://example.com/my/path/folder"

        result = query_params(url)
        expect = {}

        self.assertEqual(result, expect)

    def test_url_with_query(self):
        """
        Test when url with query parameters
        :return:
        """
        url = "http://example.com/my/path/folder?query_item=2"

        result = query_params(url)
        expect = {'query_item': "2"}

        self.assertEqual(result, expect)
