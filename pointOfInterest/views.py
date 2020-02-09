from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import requests
import io
import sys
from pandas import read_csv
from matplotlib import pyplot as pp
from django.contrib.auth.decorators import login_required
# Create your views here.


def findPlaces(request):
	return render(request, 'places.html')


def places(request):
	searchplace = request.POST.get('place')
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={x}+country+point+of+interest&language=en&key=AIzaSyA3W-x4zqHwfCJ2xgzLvuO1MVPlWwp_XJI".format(x=searchplace)
	urlData = requests.get(url).json()
	
	urlData = urlData['results']
	places = []
	for item in urlData:
		places.append(item['name'])
	shoppingPlace = shopping(searchplace)
	print("shoppppingggg: " +shoppingPlace)
	places.append(shoppingPlace)
	origin=places.pop(0)
	dest = '|'.join(places)
	places = removeDestination(origin,dest,places)
	print("New places: " ,places)
	route = []

	placeOrig = []
	for i in places:
		placeOrig.append(i)
	route.append(origin)
	for i in placeOrig:
		# print("Called: ", i)
		dest = '|'.join(places)
		smallest = smallestDistance(origin,dest)

		if(smallest != -1):
			route.append(places[smallest])
			origin = places.pop(smallest)
	print("Route: " ,route)
	
	return render(request, 'places.html')

def removeDestination(origin,dest,places):
	urlroute = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={o}&destinations={d}&key=AIzaSyA3W-x4zqHwfCJ2xgzLvuO1MVPlWwp_XJI".format(o=origin, d = dest)
	urlData2 = requests.get(urlroute).json()
	urlData2 = urlData2['rows']
	if(len(urlData2) > 0):
		urlData2 = urlData2[0]
		urlData2 = urlData2['elements']
		placesDistance = []
		counter = 0
		print("oriignal list", places)
		for item in urlData2:
			if 'distance' in item.keys():
				placesDistance.append(item['distance'].get("text"))
				print("found :" , item)
				counter += 1
			else:
				places.pop(counter)
				print("not found: ", item , "counter:  ",counter)
			print("hence the list: ",places)
	
	return places
	
def smallestDistance(origin,dest):
	urlroute = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={o}&destinations={d}&key=AIzaSyA3W-x4zqHwfCJ2xgzLvuO1MVPlWwp_XJI".format(o=origin, d = dest)
	urlData2 = requests.get(urlroute).json()
	urlData2 = urlData2['rows']
	if(len(urlData2) > 0):
		urlData2 = urlData2[0]
		urlData2 = urlData2['elements']
		placesDistance = []
		for item in urlData2:
			if 'distance' in item.keys():
				placesDistance.append(item['distance'].get("text"))
			else:
				placesDistance.append(0)
		print("places::: " ,placesDistance)
		placesDistance = list(map(str, placesDistance))
		newplaces = []
		for i in placesDistance:
			str1 = i.replace(",","")
			
		
			str1 = str1[:-3]
			
			if len(str1) == 0:
				newplaces.append(sys.maxsize)
			else:
				newplaces.append(str1)
		print("Origin:  ", origin)
		print("Destination " , dest)
		print(newplaces)
		newplaces = list(map(float, newplaces))
		if(min(newplaces) != 9223372036854775807):
			smallest = newplaces.index(min(newplaces))
		else:
			smallest = -1
		print("smallest: ", smallest)


		return smallest
	return -1


def shopping(place):
	url = "https://maps.googleapis.com/maps/api/geocode/json?address={p}&key=AIzaSyA3W-x4zqHwfCJ2xgzLvuO1MVPlWwp_XJI".format(p=place)
	urlData = requests.get(url).json()
	urlData = urlData['results']
	urlData = urlData[0]
	urlData = urlData['geometry']
	urlData = urlData['location']
	lat = urlData['lat']
	lng  = urlData['lng']
	print(lat)
	print(lng)
	urlshopping = "https://places.ls.hereapi.com/places/v1/discover/explore?at={lat}%2C{lng}&cat=shopping&apiKey=YBUkUmS-az27BtOzplNgDsOwzR5TNWJSDhc7TbZHco0".format(lat=lat,lng=lng)
	shoppingData = requests.get(urlshopping).json()
	shoppingData = shoppingData['results']
	shoppingData = shoppingData['items']
	shoppingPlace= ""
	for item in shoppingData:
		shoppingCheck = item['category']
		if(shoppingCheck['id'] == "mall"):
			shoppingPlace = item['title']
	return shoppingPlace


	



