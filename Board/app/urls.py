from django.urls import path
from django.contrib import admin
#from .views import ProfileDetailView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('profile/<int:pk>', ProfileDetailView.as_view()),
]