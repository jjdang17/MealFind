import numpy as np
import pandas as pd
import IPython 

def readUntil(strg):
	if strg == '0':
		splitStr = 0 
	else:
		grab = 0 
		for i, c in enumerate(strg):
			if c == ',':
				grab = i
		x = strg[2:grab-1]
		y = strg[grab+3:len(strg)-2]
		splitStr = [x,y]
	return splitStr
		

def convert(group):
	try:
		if group != 0:
			val = float(group[1])
			if group[0] == 'mg':
				val = float(group[1])/100
			elif group[0] == 'µg':
				val = float(group[1])/1e6
		else:
			val = 0
	except:
		print(group)
		IPython.embed()
	return val	

	
def totally(nutFile, foodFile):
	v = pd.read_csv(foodFile)
	foods = []
	for h in range(0,len(v.iloc[:,:])):
		foods.append(v.iloc[h,:][0])
	foods_log = np.array(foods)	
	q = pd.read_csv(nutFile, encoding = "ISO-8859-1")
	food_dict = {}
	for i in range(0,len(q)):
		hold = np.array(q.iloc[i,:])
		name = hold[0]
		vals = hold[1:]

		for b, val in enumerate(vals):
			#print(b)
			#print(val)
			
			
			vals[b] = convert(readUntil(val))
			
		food_dict[name] = vals
	logged_food = {}
	for snack in foods_log:
		logged_food[snack] = food_dict[snack]
	#logged_food is all the foods in the log, still needs to be summed

		
	
	

if __name__ == "__main__":
	totally('foodData.csv','foodLog.csv')