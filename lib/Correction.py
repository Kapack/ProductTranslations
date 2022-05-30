import re
from db.Select import Select

class Correction:
	def __init__(self, country:str):
		self.country = country

	def formatName(self, products:dict) -> dict:
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

				if word.lower() == 'lc.imeeke':
					word = 'LC.Imeeke'

				if word.lower() == 'mofi':
					word = 'MOFi'
				
				if word.lower() == 'imak':
					word = 'IMAK'

				if word.lower() == 'iml':
					word = 'IML'										

				if word.lower() == 'tpu':
					word = 'TPU'

				if word.lower() == 'lcd':			
					word = 'LCD'

				if word.lower() == 'usb':
					word = 'USB'

				if word.lower() == 'fhd':
					word = 'FHD'
			
				if word.lower() == 'hd':
					word = 'HD'
					
				if word.lower() == 'iphone':
					word = 'iPhone'

				if word.lower() == 'ipad':
					word = 'iPad'

				if word.lower() == 'tgvi\'s':
					word = 'TGVI\'S'

				if word.lower() == 'etrex':
					word = 'eTrex'
								
				# Translated Prepositions with lowercase
				if word.lower() in prepositions.values():
					word = word.lower()

				# Append word to new name
				newName += word + ' '

			# Let name be newName where spaced at end is stripped away
			products[product]['name'] = newName.strip()

		return products

	def formatDeviceName(self, products:dict) -> dict:
		for product in products:
			# if devName in lowercase exists in productName string in lowercase
			if products[product]['device']['devName'].lower() in products[product]['name'].lower() or products[product]['device']['manName'].lower() in products[product]['name'].lower():

				# Format manName
				src_str = re.compile(products[product]['device']['manName'], re.IGNORECASE)
				products[product]['name'] = src_str.sub(products[product]['device']['manName'], products[product]['name'])

				# Format devName
				src_str = re.compile(products[product]['device']['devName'], re.IGNORECASE)
				products[product]['name'] = src_str.sub(products[product]['device']['devName'], products[product]['name'])				

		return products
	
	# If description starts with a space (Due to missing variable).
	def startsWithSpace(self, products:dict) -> dict:
		for product in products:
			if product['description'].startswith(' '):
				# Remove space
				product['description'] = product['description'].lstrip(' ')
		
		return product