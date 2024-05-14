from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from .views import index

from django.test import TestCase, Client
from django.urls import reverse


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('title')
        self.assertEqual(resolve(url).func, index)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('title')

    def test_index_view_GET(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'title/index_page.html')
