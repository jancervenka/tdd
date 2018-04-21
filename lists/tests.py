from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item, List
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

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        # check that there is no object in the database when we just request the home page
        self.assertEqual(Item.objects.count(), 0)

# item model (ORM), model = row in a database, attributes = columns
class ListAndItemModelTest(TestCase):
    # this test is touching the databse, unit test "should never" do that
    # it is an integrated test because it uses external resources (the databse)
    def test_saving_and_retrieving_items(self):
        # create and save an empty list 
        list_ = List()
        list_.save()

        # create and test a model instance
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        # assign it to the list
        first_item.list = list_
        first_item.save() # save it to the database (django api)

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        # get the saved list and check that it is the same one
        # we saved
        saved_list = List.objects.first()
        # checks that the FK is the same
        self.assertEqual(saved_list, list_)

        # query to get all the item object instances from the database table (django api)
        saved_items = Item.objects.all() # object is a class attribute
        # saved_items is a list-like object "QuerySet"
        self.assertEqual(saved_items.count(), 2) # check that there are two

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        # we check that the saved items belong to the list
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        # we want to seperate the template for the home page (input box only)
        # and for the list view
        list_ = List.objects.create()

        # each list has a specific id
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()

        # create some mock items and assign them to the list
        Item.objects.create(text = 'itemey 1', list = correct_list)
        Item.objects.create(text = 'itemey 2', list = correct_list)

        # create a second list with some items
        other_list = List.objects.create()
        Item.objects.create(text = 'other list itemey 1', list = other_list)
        Item.objects.create(text = 'other list itemey 2', list = other_list)


        # get the view of the first list
        response = self.client.get(f'/lists/{correct_list.id}/')

        # check that only the items from the first list are in the response content
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list itemey 1')
        self.assertNotContains(response, 'other list itemey 2')

    def passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        # testing new http request with POST sending "A new List item" as item_text to the server
        response = self.client.post('/lists/new', data = {'item_text' : 'A new List item'})
        
        # we check that one Item model instance has been saved to the databse
        self.assertEqual(Item.objects.count(), 1)

        # we retrieve the first object stored in the database
        new_item = Item.objects.first()
        
        # we check that the text in the instance matches with the text we sent in the POST request
        self.assertEqual(new_item.text, 'A new List item')

    def test_redirects_after_POST(self):
        # testing new http request with POST sending "A new List item" as item_text to the server
        response = self.client.post('/lists/new', data = {'item_text' : 'A new List item'})

        # POST request should be redirected to a GET request to prevent duplicate form submissions
        # https://en.wikipedia.org/wiki/Post/Redirect/Get

        
        # check that the redirected response has the correct REST-ish url
        new_list = List.objects.first()

        # combines the previous two asserts
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        # post new item to the existing correct list
        self.client.post(f'/lists/{correct_list.id}/add_item',
            data = {'item_text' : 'A new item for an existing list'})


        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()

        # check that the first item in the db matches to the item we posted
        self.assertEqual(new_item.text, 'A new item for an existing list')
        # check that the new item FK is the correct list
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        # post new item to the existing correct list
        response = self.client.post(f'/lists/{correct_list.id}/add_item',
            data = {'item_text' : 'A new item for an existing list'})

        # check that the post redirects to the list view for the correct list
        self.assertRedirects(response, f'/lists/{correct_list.id}/')





