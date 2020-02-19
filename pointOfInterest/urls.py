from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
	path('findPlaces/', views.findPlaces, name="findPlaces"),
	path('places/', views.places, name="places"),
	path('days/', views.DaysForRoute, name="places"),
	path('days/day_wise/<int:vId>/', views.dayWiseRoutes),


	# path('shopping/', views.shopping, name="shopping")
]