# coding=utf-8
import sys
# Fixing can't encode unichar issue
reload(sys)
sys.setdefaultencoding('utf8')
from db.Select import Select

class Correction:

	def formatName(self, country, products):
		select = Select(country)
		productMaterials = select.productMaterials()

		#print productMaterials.lower().values()

		for product in products:
			newName = str('')

			# Split name
			name = products[product]['name'].split(" ")
			# Loop trough each word
			for word in name:						

				# If word is lower, capitalize
				if word.islower():
					word = word.capitalize()		

				# Special Cases
				# Apple
				if word.lower() == 'iphone':					
					word = 'iPhone'
				
				if word.lower() == 'ipad':
					word = 'iPad'

				# Append word to new name
				newName += word + ' '

			# Let name be newName where spaced at end is stripped away
			products[product]['name'] = newName.strip()

		return products
