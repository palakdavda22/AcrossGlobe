from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	path('findPlaces/', views.findPlaces, name="findPlaces"),
	path('places/', views.places, name="places"),
	path('daywise/',views.daywise,name = "daywise"),
	path('days/', views.DaysForRoute, name="places"),
	path('days/day_wise/<int:vId>/', views.dayWiseRoutes),
	#path('histtemp', views.history),
    #path('newpage/', views.new_page, name="my_function")
    


	# path('shopping/', views.shopping, name="shopping")
]


