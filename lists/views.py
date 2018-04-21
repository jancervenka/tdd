from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

# Create your views here.

# home_page function
def home_page(request):
	return render(request, 'home.html')

# for the '/lists/{list_id}/'
def view_list(request, list_id):
		
	list_ = List.objects.get(id = list_id)
	

	# pass the the list object to the template
	# request have the REST-ish url /lists/.+
	return render(request, 'list.html', {'list' : list_})


def new_list(request):
	# POST get the item_text data field
	# .objcets.create() is a shortand for creating new object with specified
	# attributed values as arguments and automatically calling the .save()
	# to push it to the database
	# with the text as the data from the POST request from the item_text form field
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)

	# return rediretction to GET home page to prevent duplicate form submissions
    # redirect calls the home page function and skips this if statement
	# the response rdirects to the url of the list
	return redirect(f'/lists/{list_.id}/')

# for the '/lists/{list_id}/add_item'
def add_item(request, list_id):
	# after posting item to an exting list, just redirects to the list url
	list_ = List.objects.get(id = list_id)
	# create a new item for the list with text from the POST argument
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect(f'/lists/{list_.id}/')