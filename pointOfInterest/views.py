from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.template import loader
import pandas as pd
import requests
import io
import sys
from pandas import read_csv
from matplotlib import pyplot as pp
from django.contrib.auth.decorators import login_required
# Create your views here.


def history(request):
    return render(request, 'index.html')

# @login_required(login_url="/login/")
def new_page(request):
    loc = request.GET['city']
    startdate = request.GET['sdate']
    enddate = request.GET['edate']
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?&dateTimeFormat=yyyy-MM-dd'T'HH%3Amm%3Ass&startDateTime={x}T00%3A00%3A00&endDateTime={y}T00%3A00%3A00&dayStartTime=0%3A0%3A00&dayEndTime=0%3A0%3A00&aggregateHours=24&collectStationContribution=false&maxDistance=80467&maxStations=3&unitGroup=us&locations={z}&key=8IW5BKDHCIDJ5KY1PHHL4W7WR".format(
        x=startdate, y=enddate, z=loc)
    urlData = requests.get(url).content
    rawData = pd.read_csv(io.StringIO(urlData.decode('utf-8')))
    print(rawData.head)
    # series = read_csv('/home/anisha/Downloads/data_1999.csv', header=0, index_col=0)
    # print(series.head())
    temp = rawData['Temperature']
    date = rawData['Date time']
    pp.plot(date, temp)
    pp.xticks(date, date, rotation='vertical')
    data = pp.show()
    return render(request, 'plot.html', {'city': loc, 'startdate': startdate, 'enddate': enddate, 'data': data})

day_wise = {}
day_wise_latlng = []
counting = []

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
	# print("New places: " ,places)
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


	today = []
	
	total_time = 3
	counter = 1

	# #dividing the routes according to the dates
	for i in range(len(route)-1):
		place1 = route[i]
		place2=route[i+1]
		
		urlitenary = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={o}&destinations={d}&key=AIzaSyA3W-x4zqHwfCJ2xgzLvuO1MVPlWwp_XJI".format(o=place1, d = place2)
		urlitenary = requests.get(urlitenary).json()
		urlitenary = urlitenary['rows']
		print(urlitenary)
		if (len(urlitenary) > 0):
			urlitenary = urlitenary[0]
			urlitenary = urlitenary['elements']
			placesDistance = ""
			traveling = ""
			for item in urlitenary:
				if 'distance' in item.keys():
					placesDistance = (item['duration'].get("text"))
					if "day" in placesDistance:
						total_time = 10
						print("total time day : ", total_time)
					elif "hours" in placesDistance:
						hour = float(placesDistance[:2])
						# print("hour:     " , hour)
						traveling = ""
						placesDistance = placesDistance[8:]
						placesDistance = placesDistance.replace(" mins","")
						placesDistance = placesDistance.replace(" min","")
						
						placesDistance = float(placesDistance)/60
						# print("places: ",placesDistance)
						hour += placesDistance
						print("in hours before: ", total_time)
						# print("hour: ",hour)
						total_time += hour
						total_time += 1.5
						print("in hours after: ", total_time)

					elif "hour" in placesDistance:
						hour = float(placesDistance[:2])
						# print("hour:     " , hour)
						traveling = ""
						placesDistance = placesDistance[8:]
						placesDistance = placesDistance.replace(" mins","")
						placesDistance = placesDistance.replace(" min","")
						placesDistance = float(placesDistance)/60
						hour += placesDistance
						print("in hour before: ", total_time)
						total_time += hour
						total_time += 1.5
						print("in hour after: ", total_time)
					else:
						# print("in elsse")
						
						total_time += 1.5
						print("in else : ", total_time)
					print(route[i])
					print(total_time)
					today.append(route[i])
					if total_time >= 10 :
						day_wise[counter]=today
						print("dayyy: " ,today)
						today = []
						total_time = 3
						counter+=1
						
	print("Summary: " ,day_wise)	
	day_wise_latlng = placeToLatlng(day_wise)
	return render_to_response('card.html', {'day_wise':day_wise,"counting":counting})


def daywise(request):
   #d = {'one':' itemone ', 'two':' itemtwo ', 'three':' itemthree '}
   day_wise_latlng = placeToLatlng(day_wise)
   print("latitude longitude: ", day_wise_latlng)
   return render(request, 'todaysRoute.html',{"day_wise":day_wise_latlng,"counting":counting})


def placeToLatlng(day_wise):
	i = 0
	for day in day_wise.values():
	
		today = []
		for place in day:
			placeLatlng = {}
			url = "https://maps.googleapis.com/maps/api/geocode/json?address={p} India &key=AIzaSyA3W-x4zqHwfCJ2xgzLvuO1MVPlWwp_XJI".format(p=place)
			urlData = requests.get(url).json()
			urlData = urlData['results']
			urlData = urlData[0]
			urlData = urlData['geometry']
			urlData = urlData['location']
			lat = urlData['lat']
			lng  = urlData['lng']
			placeLatlng["latitude"] = lat
			placeLatlng["longitude"]=lng
			today.append(placeLatlng)
		day_wise_latlng.append(today)
		i+=1
	return day_wise_latlng
			
def removeDestination(origin,dest,places):
	urlroute = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={o}&destinations={d}&key=AIzaSyA3W-x4zqHwfCJ2xgzLvuO1MVPlWwp_XJI".format(o=origin, d = dest)
	urlData2 = requests.get(urlroute).json()
	urlData2 = urlData2['rows']
	if(len(urlData2) > 0):
		urlData2 = urlData2[0]
		urlData2 = urlData2['elements']
		placesDistance = []
		counter = 0
		# print("oriignal list", places)
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
		# print("Origin:  ", origin)
		# print("Destination " , dest)
		# print(newplaces)
		newplaces = list(map(float, newplaces))
		if(min(newplaces) != 9223372036854775807):
			smallest = newplaces.index(min(newplaces))
		else:
			smallest = -1
		# print("smallest: ", smallest)


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


def DaysForRoute(request):
	number = len(day_wise)
	counting = []
	for i in range(number):
		counting.append(int(i)+1)
	return render(request, 'daysRoute.html',{"counting":counting})

def dayWiseRoutes(request,vId):
	day = day_wise_latlng[vId-1]
	return render(request,'todaysRoute.html',{"value":day})






