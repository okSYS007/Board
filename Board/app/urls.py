from django.urls import path
from django.contrib import admin
from .views import ProfileListView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', ProfileListView.as_view()),
]