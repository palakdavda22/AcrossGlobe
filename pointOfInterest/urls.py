from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
	path('findPlaces/', views.findPlaces, name="findPlaces"),
	path('places/', views.places, name="places"),
	path('daywise/',views.daywise,name = "daywise"),
	# path('shopping/', views.shopping, name="shopping")
]

