import csv
import os
from slugify import slugify	

class CreateCsv:
	def __init__(self, country:str, week:str, products:dict):
		self.country = country
		self.week = week
		self.products = products

	def saveFile(self) -> None:
		country = self.country
		week = self.week
		products = self.products
		# Path to save file
		path = os.getcwd() + '/import/' + week + '/' + self.country + '/'

		# DE, AT, CH
		if country.lower() == 'de':
			countries = ['de', 'at', 'ch']
		# NL, BE
		elif country.lower() == 'nl':
			countries = ['nl', 'be']
		# Single store_view
		else:
			countries = [country]
		
		# Write .csv File for each country
		for country in countries:			
			with open(path + 'week-'+week+'-'+country+'-translation.csv', 'w') as file:
				fieldnames = ['sku', 'name', 'description', 'url_key', 'store_view_code', 'product_type', 'color', 'material', 'productType', 'manName', 'devName']
				writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
				writer.writeheader()

				# iterate			
				i = 0
				for product in products:
					writer.writerow({'sku': products[i]['sku'], 'name': products[i]['name'], 'description': products[i]['description'], 'url_key': slugify(products[i]['name']), 'store_view_code': country, 'product_type': 'simple', 'color' : products[i]['attributes']['color'], 'material': products[i]['attributes']['material'], 'productType': products[i]['productType'], 'manName' : products[i]['device']['manName'], 'devName': products[i]['device']['devName'] })					
					i += 1