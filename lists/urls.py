"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from lists import views

urlpatterns = [
    url(r'^new$', views.new_list, name = 'new_list'),
    # regex capture group, the chars between the '/' will get passed to the view
    # as an argument. if we go to url lists/aa/, the argument aa is passed along with the request
    # argument to the view list function view_list(request, 'aa') so it knows which lists
    # to display
    url(r'^(\d+)/$', views.view_list, name = 'view_list'),
    url(r'^(\d+)/add_item$', views.add_item, name = 'add_item')
]