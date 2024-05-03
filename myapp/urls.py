from django.urls import path 
from . import views
from myapp import views

urlpatterns = [
    path('teste', views.mysite, name='mysite'), 
]