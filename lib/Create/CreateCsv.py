# -*- coding: utf-8 -*- 
# Fixing can't encode unichar issue
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import csv
import os
from slugify import slugify	

class CreateCsv:
	def __init__(self, week, country, products):
		self.country = country
		self.week = week
		self.products = products

	def saveFile(self):
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
				fieldnames = ['sku', 'name', 'description', 'url_key', 'store_view_code', 'product_type']
				writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
				writer.writeheader()

				# iterate			
				i = 0
				for product in products:								
					writer.writerow({'sku': products[i]['sku'], 'name': products[i]['name'].encode('utf-8'), 'description': products[i]['description'].encode('utf-8'), 'url_key': slugify(products[i]['name']), 'store_view_code': country, 'product_type': 'simple' })					

					i += 1