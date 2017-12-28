from django.test import TestCase

# Create your tests here.

# just test that automatic manage.py testing works
class SmokeTest(TestCase):

	def test_bad_maths(self):
		self.assertEqual(1 + 1, 3)