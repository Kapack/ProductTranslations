import csv
import os	

class OpenCsv:
	def __init__(self, weekInput, countryInput):		
		self.weekInput = weekInput
		self.countryInput = countryInput				

	# Products iteration, sku and name into a dict
	def initFile(self):		
		with open(os.getcwd() + '/import.csv', 'r') as file:
			reader = csv.DictReader(file, delimiter=';')

			products = {}
			# Iteration as primary key
			i = 0
			for key in reader:
				products[i] = {'sku': key['sku'], 'name': key['name'], 'description': key['description'], 'manName': '', 'devName': '', 'template': ''}
				i += 1

			return products