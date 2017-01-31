"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from app.views import home
from django.http import HttpRequest
from htmlvalidator.client import ValidatingClient

# TODO: Configure your database in settings.py and sync before running tests.


class HomePageTests(TestCase):
    """UnitTests for the home page application view"""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(HomePageTests, cls).setUpClass()
            django.setup()

    def setUp(self):
        super(HomePageTests, self).setUp()
        self.client = ValidatingClient()

    def test_home_url_resolves_to_home_page_view(self):
        """Dummy one test! Just for experience"""
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_returns_correct_html(self):
        """Check that home page url returns valid HTML page
        html validator used - ValidatingClient
        (https://github.com/peterbe/django-html-validator)"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_render_correct_template(self):
        request = HttpRequest()
        response = home(request)
        expected_html = render_to_string('app/index.html')
        self.assertEqual(response.content.decode(), expected_html)

    # def test_home(self):
    #     """Tests the home page."""
    #     response = self.client.get('/')
    #     self.assertContains(response, 'Home Page', 1, 200)
    #
    # def test_contact(self):
    #     """Tests the contact page."""
    #     response = self.client.get('/contact')
    #     self.assertContains(response, 'Contact', 3, 200)
    #
    # def test_about(self):
    #     """Tests the about page."""
    #     response = self.client.get('/about')
    #     self.assertContains(response, 'About', 3, 200)
