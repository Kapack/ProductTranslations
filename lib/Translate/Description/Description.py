# import random
# Adding Template Description
from db.Select import Select
from lib.Translate.Description.Smartphone import Smartphone
from lib.Translate.Description.Watchstrap import Watchstrap


class Description:
	def __init__(self, country:str, products:dict):
		self.country = country
		self.products = products

	# Decides on template
	def loopProducts(self) -> dict:
		products = self.products
		for product in products:			
			
			# SMARTWATCHES WIP
			if products[product]['productType'] == 'watchstrap':
				products[product] = self.watchStrapDesc(products[product], self.country)

			# Smartphones and if product has a template attribute		
			if products[product]['productType'] == 'cover' or products[product]['productType'] == 'case' and products[product]['template'] != '':
				products[product] = self.smartphoneDesc(products[product], self.country)				

			# WIP REPLACE VARIABLES	
			products[product] = self.replaceDescriptionVariables(products[product])

		# Return products back
		return products

	# Smartphone				
	def smartphoneDesc(self, product:dict, country:str) -> dict:		
		smartphone = Smartphone()
		product = smartphone.assignTemplate(product, country)
		return product

	# Watchstraps templates / WIP
	def watchStrapDesc(self, product:dict, country:str) -> dict:
		watchstrap = Watchstrap()		
		product = watchstrap.initTemplate(product, country)
		product = watchstrap.attrText(product, country)
		product = watchstrap.sizeText(product, country)
		product = watchstrap.endingText(product, country)					
		return product
	
	# Replace variables descriptions
	def replaceDescriptionVariables(self, product:dict) -> dict:
		select = Select(self.country)
		colors = select.colors()
		colorSingle = colors[0]
		materials = select.productMaterials()

		# Replacing variables [COLOR] in text
		if product['description'].find('[COLOR]') != -1:
			# Get translated color
			descColor = ''
			for color in product['attributes']['color']:				
				descColor = ''.join(colorSingle[color]['local'])				

			# Replace variable in description			
			product['description'] = product['description'].replace('[COLOR]', descColor)
		
		if product['description'].find('[COLOR_NEUTRUM]') != -1:
			# Get translated color
			descColor = ''
			for color in product['attributes']['color']:				
				descColor = ''.join(colorSingle[color]['color_neutrum'])				

			# Replace variable in description			
			product['description'] = product['description'].replace('[COLOR_NEUTRUM]', descColor)

		# Replacing variables [MATERIAL] in text		
		if product['description'].find('[MATERIAL]') != -1:
			try:
				product['description'] = product['description'].replace('[MATERIAL]', materials[product['attributes']['material']])
			except Exception as e:
				print(e)

		# Replace [DEVICE NAME]
		if product['description'].find('[DEVICE NAME]') != -1:			
			product['description'] = product['description'].replace('[DEVICE NAME]', product['device']['manName'] + ' ' + product['device']['devName'])
		
		# If description starts with a space (Due to missing variable).
		if product['description'].startswith(' '):
			# Remove space
			product['description'] = product['description'].lstrip(' ')
					
		# return product base
		return product