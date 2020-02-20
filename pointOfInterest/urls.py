from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
	path('findPlaces/', views.findPlaces, name="findPlaces"),
	path('places/', views.places, name="places"),
<<<<<<< HEAD
	path('daywise/',views.daywise,name = "daywise"),
=======
	path('days/', views.DaysForRoute, name="places"),

>>>>>>> 97b022d04881f7f14e4d46a88b18132da68f9d94
	# path('shopping/', views.shopping, name="shopping")
]

