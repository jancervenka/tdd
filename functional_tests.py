from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	# like finally, run even after an error
	def tearDown(self):
		self.browser.quit()

	# any method with test at the beginning of the name is a test
	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get('http://localhost:8000')

		self.assertIn('To-Do', self.browser.title)

		self.fail('Finish the test!')

if __name__ == '__main__':

	# runs the test
	unittest.main(warnings = 'ignore')


