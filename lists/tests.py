from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item
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
        
        # we check that one Item model instance has been saved to the databse
        self.assertEqual(Item.objects.count(), 1)

        # we retrieve the first object stored in the database
        new_item = Item.objects.first()
        
        # we check that the text in the instance matches with the text we sent in the POST request
        self.assertEqual(new_item.text, 'A new List item')

    def test_redirects_after_POST(self):
        # testing new http request with POST sending "A new List item" as item_text to the server
        response = self.client.post('/', data = {'item_text' : 'A new List item'})

        # POST request should be redirected to a GET request to prevent duplicate form submissions
        # https://en.wikipedia.org/wiki/Post/Redirect/Get
        # check that the http response is redirection (302 code)
        self.assertEqual(response.status_code, 302)
        
        # check that the redirected response has the correct REST-ish url
        # we only support one list (= one url) now
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        # check that there is no object in the database when we just request the home page
        self.assertEqual(Item.objects.count(), 0)

# item model (ORM), model = row in a database, attributes = columns
class ItemModelTest(TestCase):
    # this test is touching the databse, unit test "should never" do that
    # it is an integrated test because it uses external resources (the databse)
    def test_saving_and_retrieving_items(self):
        # create and test a model instance
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save() # save it to the database (django api)

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        # query to get all the item object instances from the database table (django api)
        saved_items = Item.objects.all() # object is a class attribute
        # saved_items is a list-like object "QuerySet"
        self.assertEqual(saved_items.count(), 2) # check that there are two

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        # we want to seperate the template for the home page (input box only)
        # and for the list view
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):

        # create some mock items
        Item.objects.create(text = 'itemey 1')
        Item.objects.create(text = 'itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        # check that the items are in the response content
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')


