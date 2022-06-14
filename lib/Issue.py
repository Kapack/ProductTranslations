import os
from common.Constants import LOG_PATH, BGCOLORS

class Issue:
	def __init__(self, products:dict = None, country:str = None):		
		self.products = products
		self.country = country

	def checkForEmptyManAndDevName(self) -> None:
		products = self.products
		skus = []
		# Loop Through produts
		for product in products:
			if len(products[product]['device']['manName']) == 0 or len(products[product]['device']['devName']) == 0:
				skus.append(products[product]['sku'])
		
		textfile = open("log/missingManDevName.txt", "w")
		for sku in skus:
			textfile.write(sku + "\n")
		textfile.close()


	def doubleSpace(self) -> None:
		products = self.products
		skus = []

		for product in products:
			if '  ' in products[product]['description']:
				skus.append(products[product]['sku'])				

		textfile = open("log/doubleDash.txt", "w")
		for sku in skus:
			textfile.write(sku + "\n")
		textfile.close()
	
	def clearLogFile(self) -> None:		
		if len(os.listdir(LOG_PATH)) >= 0:
			for file in os.listdir(LOG_PATH):
				os.remove(LOG_PATH + '/' + file)

	def checkForLogFiles(self) -> None:	
		if len(os.listdir(LOG_PATH)) >= 0:
			print(BGCOLORS['WARNING'] + 'Logfiles has been created!' + BGCOLORS['ENDC'])