from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# home_page function
def home_page(request):
	# return HttpResponse() # return new http response object
	return HttpResponse('''<html>
	                           <title>To-Do lists</title>
	                       </html>''') # better