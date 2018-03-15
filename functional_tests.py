from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	# like finally, run even after an error
	def tearDown(self):
		self.browser.quit()

	# helper method, does not start with "test"
	# to remove duplicate code from the functional test method
	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr') # elementS - might return an empty list
		self.assertIn(row_text, [row.text for row in rows])

	# any method with test at the beginning of the name is a test
	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get('http://localhost:8000')

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
		time.sleep(1) # wait for the browser to load the page

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr') # elementS - might return an empty list

		# check that the to-do is in the list
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		#self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

		# check for another item
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
		#self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])

		self.fail('Finish the test!')

if __name__ == '__main__':

	# runs the test
	unittest.main(warnings = 'ignore')
