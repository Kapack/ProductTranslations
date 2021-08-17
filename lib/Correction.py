# coding=utf-8
import sys
import re
# Fixing can't encode unichar issue
reload(sys)
sys.setdefaultencoding('utf8')
from db.Select import Select

class Correction:
	def __init__(self, country):
		self.country = country

	def formatName(self, products):
		select = Select(self.country)		
		prepositions = select.prepositions()

		for product in products:
			newName = str('')

			# Split name
			name = products[product]['name'].split(" ")
			# Loop trough each word
			for word in name:						

				# If word is lower, capitalize
				if word.islower():
					word = word.capitalize()

				# Brands
				if word.lower() == 'caseme':
					word = 'CaseMe'
				
				if word.lower() == 'dg.ming':
					word = 'DG.Ming'

				if word.lower() == 'Lc.imeeke':
					word = 'LC.Imeeke'
				
				# Translated Prepositions with lowercase
				if word.lower() in prepositions.values():
					word = word.lower()

				# Append word to new name
				newName += word + ' '

			# Let name be newName where spaced at end is stripped away
			products[product]['name'] = newName.strip()

		return products

	def formatDeviceName(self, products):
		select = Select(self.country)
		deviceList = select.deviceList()

		for product in products:
			# if devName in lowercase exists in productName string in lowercase
			if products[product]['devName'].lower() in products[product]['name'].lower():
				src_str = re.compile(products[product]['devName'], re.IGNORECASE)
				products[product]['name'] = src_str.sub(products[product]['devName'], products[product]['name'])

		return products