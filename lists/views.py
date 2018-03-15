from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# home_page function
def home_page(request):
	# the third argument passes the POST parameter to template (name of the form input), 
	# the render function takes a dictionary
	# which maps the template variable names to their values
	# we are using dict.get() so that we can return empty string to the template 
	# when there is no POST request
	# this takes the value from the item_text field in the POST request (written first in the input form)
	# and displays it in the new_item_text {{}} brackets in the table
	return render(request, 'home.html',
		          {'new_item_text' : request.POST.get('item_text', '')})