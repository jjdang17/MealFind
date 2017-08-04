#Program to track meal information
#cd C:\Users\John\Google Drive\TAMU\MealFind

import time
import numpy as npy
import requests
import json
import csv
import keys

def getdate():
	## 12 hour format ##
	return time.strftime("%d/%m/%Y")
	

def usda(food):
	key = keys.APP_KEY
	param1 = {"api_key": key, "q": food, "ds": "Standard Reference", "max": "5", "format": "json"}
	search = requests.get("https://api.nal.usda.gov/ndb/search", params = param1)
	names = []
	ndbno = []	
	if search.status_code == 200:
		
		
		data = json.loads(search.content)
		for a in range(0,len(data['list']['item'])):
			names.append(data['list']['item'][a]['name'])
			ndbno.append(data['list']['item'][a]['ndbno'])
		print("Which of these did you eat?")
		for b in range(0,len(names)):
			print(str(b) + " " + names[b] )
		answer = input("number: ")
		#ndbno for chosen food
		foodID = []
		foodID.append(ndbno[int(answer)])
		param2 = {"ndbno": ",".join(foodID), "type": "b", "format": "json","api_key": key}
		report = requests.get("https://api.nal.usda.gov/ndb/reports/", params = param2)
		print(report.url)
		if report.status_code == 200:
			reportData = json.loads(report.content)
			print (reportData)
			nutrientNum = len(reportData['report']['food']['nutrients'])
			name = []
			unit = []
			value = []
			for y in range(0,nutrientNum):
				name.append(reportData['report']['food']['nutrients'][y]['name'])
				value.append(reportData['report']['food']['nutrients'][y]['value'])
				unit.append(reportData['report']['food']['nutrients'][y]['unit'])
			d = [name, unit, value]	
		else:
			print("Error!")
			print(report.text)
	else:
		print("Error!")
	return d
		
def parsemeal(hold):
	hnew = []
	index = []
	b = hold != "a"
	
	hold = hold[b]
	
	for t in range(0, len(hold)):
		if hold[t] == "and" or hold[t] == "with" or hold[t] == "on" or hold[t] == "in":
			index.append(t)
			
	counter = 0 
	
	
	if index != []:
		for k in range(0,len(index)):
			combine = ""
			postcombine = ""
				
			if index[k] == 1:
				combine = hold[0]
				counter = 2
				hnew.append(combine)
			else:
				for n in range(counter,index[k]):
					combine += hold[n]
					
					if n<index[k]-1:

						combine += " "
					
				counter = index[k]+1	
				hnew.append(combine)
			
		for w in range(index[k]+1,len(hold)):
			postcombine += hold[w]
			if w<len(hold) - 1:

				postcombine += " "
		hnew.append(postcombine)
	else:
		
		combine = ""
		for h in range(0,len(hold)):
			combine += hold[h]
			if h<len(hold):
				combine += " "
				
		hnew.append(combine)
	
	return hnew
	
def ask():
	
	print("Hello there! Welcome to MealFind...")
	time.sleep(1)
	print("What did you eat today?")
	meals = ["Breakfast", "Lunch", "Dinner", "Snacks"]
	
	full = []
	for m in range(0,len(meals)):
		eaten = input(meals[m] + ": ").split()
		hold = npy.array(eaten)
		
		hnew = parsemeal(hold)
		for q in range(0,len(hnew)):
			full.append(hnew[q])
	print(full)
	return full
	

if __name__ == "__main__":
	#Get user input
	foods = ask()
	
	#access database info
	lists = []
	for h in range(0,len(foods)):
		list = usda(foods[h])
		if h == 0:
			lists = list
		else:
			for j in range(0,len(list[0])):
				lists[0].append(list[0][j])
				lists[1].append(list[1][j])
				lists[2].append(list[2][j])
	print(lists)
	
	import os.path
	 
	filename = 'foodData.csv'
	
	if os.path.isfile(filename):
		mode = 'a'
	else:
		mode = 'w'
	val = []
	counter = 0
	for u in range(0,len(foods)):
		lister = []
		lister = lists[2][counter:counter+31]
		counter += 32
		lister.append(foods[u])
		lister = lister[-1:] + lister[:-1]
		val.append(lister)
	
	names = list[0]
	names.append(" ")
	names = names[-1:] + names[:-1]
	units = list[1]
	units.append(" ")
	units = units[-1:] + units[:-1]
	
	with open(filename, mode, newline='') as csvfile:
		daywriter = csv.writer(csvfile, delimiter=' ')
		daywriter.writerow(getdate())
		spamwriter = csv.writer(csvfile, delimiter = ',')
		spamwriter.writerow(names)
		spamwriter.writerow(units)
		
		for y in range(0,len(foods)):
			spamwriter.writerow(val[y])
	csvfile.close()	
	
	#---------------------------------------------------

		#if not able to find on database attempt web scrape
		
		
		#---------------------------------------------------
	#Sum macros from each food
	
	#Access file with user info
	
	#Organize and send to csv file
	#with open('eggs.csv', 'wb') as csvfile: