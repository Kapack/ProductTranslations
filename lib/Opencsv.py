import csv
import os	

class OpenCsv:
	def __init__(self, weekInput:str, countryInput:str):		
		self.weekInput = weekInput
		self.countryInput = countryInput				

	# Products iteration, sku and name into a dict
	def initFile(self) -> dict:		
		with open(os.getcwd() + '/import.csv', 'r') as file:
			reader = csv.DictReader(file, delimiter=';')

			products = {}
			# Iteration as primary key
			i = 0
			for key in reader:				
				products[i] = {'sku': key['sku'], 'name': key['name'], 'description': key['description'], 'template': '', 'productType': '', 'attributes': {'color' : [], 'material' : '', 'feature' : '' }, 'sizes' : {'size' : '', 'length': '', 'width': '', 'circumference' : ''}, 'device' : {'manName': '', 'devName': ''} }
				i += 1

			return products