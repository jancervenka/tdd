from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.

# home_page function
def home_page(request):
	# item = Item()
	
	# save the data from the POST reques to the item model text attribute
	# item.text = request.POST.get('item_text', '')
	# push it to the databse
	# item.save()
	# problem - we are saving an empty item with every home page request

	# the third argument passes the POST parameter to template (name of the form input), 
	# the render function takes a dictionary
	# which maps the template variable names to their values
	# we are using dict.get() so that we can return empty string to the template 
	# when there is no POST request
	# this takes the value from the item_text field in the POST request
	# and displays it in the new_item_text {{}} brackets in the table
	# return render(request, 'home.html',
	#	           {'new_item_text' : request.POST.get('item_text', '')})
	

	# if POST get the item_text data field
	if request.method == 'POST':
		# .objcets.create() is a shortand for creating new object with specified
		# attributed values as arguments and automatically calling the .save()
		# to push it to the database
		# we create the new object only for POST requests
		# with the text as the data from the POST request from the item_text form field
		Item.objects.create(text = request.POST['item_text'])

		# return rediretction to GET home page to prevent duplicate form submissions
		# redirect calls the home page function and skips this if statement
		# the response rdirects to the url of the list
        # we only support one list (= one url) now
		return redirect('/lists/the-only-list-in-the-world/')

	# Not a POST, just return the home page
	# do not show list
	return render(request, 'home.html')

# for the '/lists/the-only-list-in-the-world/' url (or any other list url)
def view_list(request):
	# get all the items from the database
	items = Item.objects.all()
	# and render them inside the template tag

	# render the items from te db to the items list in the {% for %} tag which displays their .text
	# attribute in the template
	# request have the REST-ish url /lists/.+
	return render(request, 'list.html', {'items' : items})