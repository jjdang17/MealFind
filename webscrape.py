#Scrape food websites for ingredients
#look into hrecipe
#http://microformats.org/wiki/hrecipe

import IPython
from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import keys
import urllib
import json
import sys


def search(recipe):
	if recipe == '' or recipe == ' ':
		raise ValueError("Error! Need recipe name.")
		
	else:
		#Credit rjdang for google search code
		search = recipe
		site = "food network"
		search_string = site + ' ' + search
		url = "https://www.google.com/search?" 
		query_encoded = urllib.parse.urlencode({"q":search_string})
		query = url + query_encoded
		
		#spaces %20
		#apostrophe %27

		url_request = Request(query, headers = {"User-Agent": "Mozilla/5.0"})
		uclient = uReq(url_request)
		response = uclient.read()
		uclient.close()
		page_soup = soup(response)
		red = page_soup.find_all('a')
		
		
		IPython.embed()

		
				
				
def webscrape(myurl):
	#open connection and grab page
	uClient = uReq(myurl)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	container = page_soup.find("div",{"class":"o-Ingredients__m-Body"})
	hold = container.ul.findAll('li')
	ingredients = []
	for c in range(0,len(hold)):
		ingredients.append(hold[c].label.string)
	return ingredients
	# groceryList = []
	# quantity = []
	# for d in range(0,len(ingredients)):
		# ingredient = ingredients[d].split()	
		# groceryList.append(ingredient[len(ingredient)-1])
		# amount = []
		# for y in range(0,len(ingredient)-1):
			# amount.append(ingredient[y])
		# quantity.append(amount)
	# return (groceryList, quantity)
	
if __name__ == "__main__":
	recipe = "shepherd's pie"
	search(recipe)
	#vals = webscrape(keys.myurl)
	