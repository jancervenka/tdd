from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        # for root url ('/') resolve django function returns home_page function
        found = resolve('/') 
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        
        # create dummy http request object
        request = HttpRequest()
        
        # pass the request to the home_page function which returns a response
        response = home_page(request)

        # extract the html content of the response and convert
        # the raw bytes to string
        html = response.content.decode('utf-8')

        # check that the html looks ok
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))