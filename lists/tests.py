from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        # for root url ('/') resolve django function returns home_page function
        found = resolve('/') 
        self.assertEqual(found.func, home_page)

    #def test_home_page_returns_correct_html(self):
    #    
    #    # create dummy http request object
    #    request = HttpRequest()
    #    
    #    # pass the request to the home_page function which returns a response
    #    response = home_page(request)
    #
    #    # extract the html content of the response and convert
    #    # the raw bytes to string
    #    html = response.content.decode('utf-8')
    #
    #    # return a string of html based on the html file
    #    expected_html = render_to_string('home.html')
    #    self.assertEqual(html, expected_html)

    def test_home_template(self):
        
        # instead of manual HttpRequest object we just specify
        # what url we want
        response = self.client.get('/') 
        
        # test that the response coresponds to the home.html template
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        # testing new http request with POST sending "A new List item" as item_text to the server
        response = self.client.post('/', data = {'item_text' : 'A new List item'})
        # test that the data "A new List item" are somewhere in the html returned by the response
        self.assertIn('A new List item', response.content.decode())
        # test that the correct template is used
        self.assertTemplateUsed(response, 'home.html')