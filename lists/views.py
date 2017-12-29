from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# home_page function
def home_page(request):
	return render(request, 'home.html')