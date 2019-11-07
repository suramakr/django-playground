from django.urls import path
from . import views

# views.index,  which is the function named index() in the views.py file.
urlpatterns = [
    path('', views.index, name='index'),
]
