#Program to track meal information
#cd C:\Users\John\Google Drive\TAMU\MealFind

import time
import numpy as np
import requests
import json
import csv
import keys
import pandas as pd




def getdate():
	## 12 hour format ##
	date = '#' + time.strftime("%m/%d/%Y")
	return date
	

def usda(food):
	
	
	try:
		key = keys.APP_KEY
	except ValueError:
		#raise ValueError: 
		print("API KEY not found. You need to generate one here: link.to.api.key.generator.com")
	
	param1 = {"api_key": key, "q": food, "ds": "Standard Reference", "max": "5", "format": "json"}
	search = requests.get("https://api.nal.usda.gov/ndb/search", params = param1)
	names = []
	ndbno = []	
	if search.status_code == 200:
		
		try:
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
			
				nutrientNum = len(reportData['report']['food']['nutrients'])
				name = []
				unit = []
				value = []
				for y in range(0,nutrientNum):
					name.append(reportData['report']['food']['nutrients'][y]['name'])
					value.append(reportData['report']['food']['nutrients'][y]['value'])
					unit.append(reportData['report']['food']['nutrients'][y]['unit'])
				
				d = [name, unit, value]	
				fn = names[int(answer)]
				method = 1
			else:
				print("Error!")
				print(report.text)
				method = 0
		except:
			print("Unable to find, going to try webscraping.")
			d = ['name','unit','value']
			fn = 'scrape'
			method = 2
	else:
		print("Error!")
		method = 0
	return (d, fn, method)
		
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
		hold = np.array(eaten)
		
		hnew = parsemeal(hold)
		for q in range(0,len(hnew)):
			full.append(hnew[q])
	print(full)
	return full
	

if __name__ == "__main__":
	#Get user input
	foods = ask()
	
	#access database info
	
	
	stat = {}
	names = []
	p = 1
	for h in range(0,len(foods)):
		just_in = usda(foods[h])
		new = just_in[0]
		name = just_in[1]
		names.append(name)
		method = just_in[2]
		
		if not name  in stat:
			name = name
		else:
			name += str(p)
			p += 1
	
		stat[name] = {new[0][0]: [new[1][0], new[2][0]]}
	
		for b in range(1,len(new[0])):
			stat[name][new[0][b]] = [new[1][b], new[2][b]]

	
#********************************************************************************************************************	
#instead of writing everything to one file, make a file that has the nutrition info for unique foods. Update whenever
#a new food is found. Then make a separate file of just the foods eaten that day
#********************************************************************************************************************	
	#Check if files exists
	import os.path
	safestat = stat.copy()
	names = np.array(names)
	filename = 'foodData.csv'
	
	if os.path.isfile(filename):
		#File exists, append to it
		currentInfo = pd.read_csv(filename,encoding = "ISO-8859-1")
		currentNames = currentInfo.iloc[:,0]
		for j in range(0,len(currentNames)):
			remove = names[names == currentNames[j]]
			for r in range(0,len(remove)):
				del safestat[remove[r]]
		newInfo = pd.DataFrame(safestat)
		newInfo = pd.DataFrame.transpose(newInfo)
		newInfo = newInfo.fillna(0)
		newInfo.to_csv(path_or_buf = filename,mode = 'a',header=False)
	else:
		#File does not exist, let's make one!
		newInfo = pd.DataFrame(stat)
		newInfo = pd.DataFrame.transpose(newInfo)
		newInfo = newInfo.fillna(0)
		newInfo.to_csv(path_or_buf = filename,mode = 'w')
	
	#Check if file exists
	filename2 = 'foodLog.csv'
	if os.path.isfile(filename2):
	#File exists, append to it
		mode = 'a'
	else:
	#File does not exist, let's make one!
		mode = 'w'
	
	with open(filename2, mode, newline='') as csvfile:
		daywriter = csv.writer(csvfile, delimiter=' ')
		daywriter.writerow(getdate())
		spamwriter = csv.writer(csvfile, delimiter = ',')
		for f in range(0,len(names)):
			spamwriter.writerow([names[f]])
	
	
	
	# data = pd.DataFrame(stat)
	# data = pd.DataFrame.transpose(data)
	# data = data.fillna(0)
	# print(data)
	
	
	# # Make sure the file exists and if not, make one	
	# import os.path
	 
	# filename = 'foodData.csv'
	
	# if os.path.isfile(filename):
		# mo = 'a'
	# else:
		# mo = 'w'
# #	Append new data to .csv file
	# data.to_csv(path_or_buf = filename,mode = mo)		
	
	#---------------------------------------------------

		#if not able to find on database attempt web scrape
		
		
		#---------------------------------------------------
	#Sum macros from each food

	
