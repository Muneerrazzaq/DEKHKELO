from . import views
from django.urls import path
from . import forms

urlpatterns = [
    path('',views.index,name='index'),
    path('brands',views.brands,name='brands'),
    path('categories',views.categories,name='categories'),
    path('new_index',views.new_index,name='new_index'),
    path('about',views.about,name='about'),
    path('contact',views.add_contact,name='contact'),
]