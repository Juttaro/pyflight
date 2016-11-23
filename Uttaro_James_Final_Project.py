# James Uttaro - Final Project - CSC 113
#
#
#This Project is designed to simulate a High Level Idea of a website idea I have for trip planning. 
# In this project uses the google QPX API to search for cheap round trip flights between two cities 
# It queries the google server, we recieve back a Json file which we parse through to give the user
# the Price, Date-Time and Flight Number. 
# The Idea for this project was to implement an algorthim that will use the information from google flights
# and information from a Hotel/Hostel/Rental service to provide cheap options for someone that wants to 
# travel to another country. For example if a person had 10 days off in a given month the algorithm would
# find the best 10 days to go at the best price within that month. 
# The issue I ran into was finding a Housing api that i could access and get the data I wanted.
# Because I couldn't get access to what I wanted and It would have been a much longer project, 
# I decided that I could use this project as a learning point to learn API's and working with JSON
#
#
#
#

import urllib2
import json
from Tkinter import Tk , Label , X , Y , BOTH, Button, Entry, TOP, BOTTOM, RIGHT, TOP
from Tkinter import *


def Flight_Inputs(origin , destination , date, retdate, passengercount):
	code = {
	  "request": {
		"passengers": {
		  "adultCount": passengercount
		},
		"slice": [
		  {
			"origin": origin,
			"destination": destination,
			"date" :date
		  },
		  {
			"origin": destination,
			"destination": origin,
			"date": retdate
		  }
		],
		 "refundable": "false",
		 "solutions": 10
	  }

	}
	return code



def getFlightInfo():
	Result_String = 'Flight List '+ getPrices()
	return Result_String


def getTimes(count):
	OpenFlightsJson = open('FlightText.json', 'r')
	JsonString = ''
	for i in OpenFlightsJson:
		JsonString = JsonString + i
	
	OpenFlightsJson.close()
	
	ParsedFlightsJson = JsonString
	parsed_json = json.loads(ParsedFlightsJson)
	
	Result_String = ""
	
	segcount = 0
	while segcount < 2:
		Result_String = Result_String + '\n \n Duration : ' + str(parsed_json['trips']['tripOption'][count]['slice'][segcount]['segment'][0]['duration'])
		Result_String = Result_String + '\n Arrival Time : ' + parsed_json['trips']['tripOption'][count]['slice'][segcount]['segment'][0]['leg'][0]['arrivalTime']
		Result_String = Result_String + '\n Departure Time :' + parsed_json['trips']['tripOption'][count]['slice'][segcount]['segment'][0]['leg'][0]['departureTime']
		Result_String = Result_String + '\n Flight Number : ' + parsed_json['trips']['tripOption'][count]['slice'][segcount]['segment'][0]['flight']['carrier'] +'-'+ str (parsed_json['trips']['tripOption'][count]['slice'][segcount]['segment'][0]['flight']['number'])
		segcount = segcount + 1
	return Result_String


def getPrices():
	OpenFlightsJson = open('FlightText.json', 'r')
	JsonString = ''
	for i in OpenFlightsJson:
		JsonString = JsonString + i
		
	OpenFlightsJson.close()
	ParsedFlightsJson = JsonString
	parsed_json = json.loads(ParsedFlightsJson)
	Result_String= ""
	count = 0
	while count < 5:
		Result_String = Result_String + '\n \nPrice : ' + parsed_json['trips']['tripOption'][count]['saleTotal']
		Result_String = Result_String + getTimes(count)
		count = count + 1
	return Result_String 



def getLowestPriceFlight():
	OpenFlightsJson = open('FlightText.json', 'r')
	JsonString = ''
	for i in OpenFlightsJson:
		JsonString = JsonString + i
	
	OpenFlightsJson.close()
	
	ParsedFlightsJson = JsonString
	parsed_json = json.loads(ParsedFlightsJson)
	
	Result_String = "\n Lowest Priced Flight " + "\n Price : " + parsed_json['trips']['tripOption'][0]['saleTotal']
	
	
	segcount = 0
	while segcount < 2:
		Result_String = Result_String + '\n \n Duration : ' + str(parsed_json['trips']['tripOption'][0]['slice'][segcount]['segment'][0]['duration']) + ' Minutes'
		Result_String = Result_String + '\n Arrival Time : ' + parsed_json['trips']['tripOption'][0]['slice'][segcount]['segment'][0]['leg'][0]['arrivalTime']
		Result_String = Result_String + '\n Departure Time :' + parsed_json['trips']['tripOption'][0]['slice'][segcount]['segment'][0]['leg'][0]['departureTime']
		Result_String = Result_String + '\n Flight Number : ' + parsed_json['trips']['tripOption'][0]['slice'][segcount]['segment'][0]['flight']['carrier'] +'-'+ str (parsed_json['trips']['tripOption'][0]['slice'][segcount]['segment'][0]['flight']['number'])
		segcount = segcount + 1
	return Result_String





#Main

container = Tk()

#url is required, has been taken out as it requires a private key for google flight API 



#Heading label
Heading_label = Label(container, text= "Flight Finder", bg = '#80d5ff' , width = 40)
Heading_label.pack(side = TOP, fill = BOTH)

# Entry Box A Origin

A_label = Label(container, text="Origin (ex. LAX, JFK) : " )
A_label.pack(side=TOP )

A_entry = Entry(container)
A_entry.pack(side = TOP)


# Entry Box B Destination

B_label = Label(container, text="Destination (ex. GVA, MXP) : ")
B_label.pack(side=TOP)

B_entry = Entry(container)
B_entry.pack(side = TOP)


# Entry Box C Departure Date

C_label = Label(container, text="Departure Date (ex. YYYY-MM-DD) : ")
C_label.pack(side=TOP)

C_entry = Entry(container)
C_entry.pack(side = TOP)


# Entry Box D Return Date

D_label = Label(container, text="Return Date (ex. YYYY-MM-DD) : ")
D_label.pack(side=TOP)

D_entry = Entry(container)
D_entry.pack(side = TOP)



#callback functions

def Search_callback():
    result  =  getFlightInfo()
    listbox.delete (0, 250)
    for i in result.splitlines():
    	listbox.insert(END,str(i))

	

def Lowest_callback():
    result = str(getLowestPriceFlight())
    listbox.delete (0, 250 )
    for i in result.splitlines():
    	listbox.insert(END,str(i))

def getCode():
	url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=AIzaSyDXCtcYePUNCFxa6NDhbm9_nQoBCpQ2R4o"
	print A_entry.get()
	code = Flight_Inputs(A_entry.get(),B_entry.get(),str(C_entry.get()),str(D_entry.get()),1)
	jsonreq = json.dumps(code, encoding = 'utf-8')
	req = urllib2.Request(url, jsonreq, {'Content-Type': 'application/json'})
	flight = urllib2.urlopen(req)
	response = flight.read()
	flight.close()
	FlightTextFile = open('FlightText.json', 'w')
	FlightTextFile.write(response)
	FlightTextFile.close()
	listbox.insert(END,"Information was loaded Now you can use")
	listbox.insert(END,"Flight List and Lowest Price Buttons")
	print code






#Buttons
Load_button = Button(container, text = "Load (must load info before using next buttons)", command=getCode)
Load_button.pack(side = TOP)

Search_button = Button(container, text = "Get Flight List", command=Search_callback)
Search_button.pack(side = TOP)

Lowest_button = Button(container, text = "Get Lowest Price Flight", command=Lowest_callback)
Lowest_button.pack(side = TOP)


# Results Box Scroll
scrollbar = Scrollbar(container)
listbox = Listbox(container, yscrollcommand=scrollbar.set )
listbox.pack(side=BOTTOM, fill=BOTH)
scrollbar.config(command=listbox.yview)


container.mainloop()




# 
# jsonreq = json.dumps(code, encoding = 'utf-8')
# req = urllib2.Request(url, jsonreq, {'Content-Type': 'application/json'})
# flight = urllib2.urlopen(req)
# response = flight.read()
# flight.close()
# FlightTextFile = open('FlightText.json', 'w')
# FlightTextFile.write(response)
# FlightTextFile.close()
