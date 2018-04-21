from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time

# we have created app functional_tests
# with test file functional_tests/tests.py
# we run the tests using python manage.py test functional_tests
# We change the NewVisitorTest inheritence (unittest.TestCase) to django.test.LiveServerTestCase
# LiveServerTestCase creates a test database and runs a development server so we don't have to
# run the server manually and we also don't have té flush the production databse after each
# functional test run

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    # like finally, run even after an error
    def tearDown(self):
        self.browser.quit()

    # helper method, does not start with "test"
    # to remove duplicate code from the functional test method
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()

        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                # elementS - might return an empty list
                rows = table.find_elements_by_tag_name('tr') 
                self.assertIn(row_text, [row.text for row in rows])
                # we return from the loop if the assertion passes
                return # return None - but exit the loop

            # if we get exception (AssertionError or WebDriverException)
            # AssertionError might be cause because the table is not reloaded
            # we wait 0.5 second and try again
            # if the code still fails and MAX_WAIT has elapsed we raise the error
            # and let it bubble up tu our test
            # then we escape the loop 
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e

                time.sleep(0.5)
        

    # any method with test at the beginning of the name is a test
    def test_can_start_a_list_for_one_user(self):
        #self.browser.get('http://localhost:8000') # old unittest version
        self.browser.get(self.live_server_url) # attribute with url to access the development server

        # notice the to-do title
        self.assertIn('To-Do', self.browser.title)
        # returns one element, raises exception when none is found
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # invite to enter to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item' )

        # type a to-do item into a textbox
        # Selenium obects have send_keys() to enter string to boxes
        inputbox.send_keys('Buy peacock feathers')
        # After pressing enter, the page updates a saves the item to 
        # the list
        inputbox.send_keys(Keys.ENTER) # press enter
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        
        # the input box is still there
        inputbox = self.browser.find_element_by_id('id_new_item')

        # type in another item
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER) # press enter
        # check that the to-do is in the list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        #self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

        # check for another item
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        #self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        # -> next test

    def test_multiple_users_can_start_lists_at_different_url(self):
        # same as the previous test
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # get the current url
        edith_list_url = self.browser.current_url

        # check that the url match the regex with our REST-ish url
        self.assertRegex(edith_list_url, '/lists/.+')

        # edith closes the brwoser
        self.browser.quit()

        # francis comes alogn
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        
        # check that the previous list is not there
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # new list for francis
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        
        #check that the urls are different
        self.assertNotEqual(francis_list_url, edith_list_url)        

        page_text = self.browser.find_element_by_tag_name('body').text
        # check that the previous list is not there but the new one is
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)




#if __name__ == '__main__':
#
#    # runs the test
#    unittest.main(warnings = 'ignore')
