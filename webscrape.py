#Scrape food websites for ingredients

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

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
	myurl = 'http://www.foodnetwork.com/recipes/ina-garten/roasted-summer-vegetables-2303527'
	vals = webscrape(myurl)
	print(vals)