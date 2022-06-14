# import random
# Adding Template Description
from db.Select import Select
from lib.Translate.Description.Smartphone import Smartphone
from lib.Translate.Description.Watchstrap import Watchstrap
# Constants
from common.Constants import ATTRIBUTES_VARIABLES

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
		product = watchstrap.initTemplate(product = product, country = country)
		product = watchstrap.attrText(product = product, country = country)
		product = watchstrap.sizeText(product = product, country = country)
		product = watchstrap.endingText(product = product, country = country)					
		return product
	
	# Replace variables descriptions
	def replaceDescriptionVariables(self, product:dict) -> dict:
		select = Select(self.country)
		colors = select.colors()
		colorSingle = colors[0]
		materials = select.productMaterials()

		for ATTRIBUTES_VARIABLE in ATTRIBUTES_VARIABLES:
			# If a attribute exists in the text			
			if ATTRIBUTES_VARIABLE in product['description']:				
				# Getting the translated Attribute
				translatedAttr = ''
				# Replace [VARIALBE] in Text
				if ATTRIBUTES_VARIABLE == '[COLOR]':
					# Get translated color		
					for color in product['attributes']['color']:				
						try:
							translatedAttr = ''.join(colorSingle[color]['local'])
						except Exception as e:
							print(e)

				if ATTRIBUTES_VARIABLE == '[COLOR_NEUTRUM]':
					for color in product['attributes']['color']:				
						try:
							translatedAttr = ''.join(colorSingle[color]['neutrum'])	
						except Exception as e:
							print(e)
				
				if ATTRIBUTES_VARIABLE == '[MATERIAL]':
					try:
						translatedAttr = materials[product['attributes']['material']]						
					except Exception as e:
						print(e)
				
				if ATTRIBUTES_VARIABLE == '[DEVICE NAME]':
					try:
						translatedAttr = product['device']['manName'] + ' ' + product['device']['devName']											
					except Exception as e:
						print(e)
				
				# Replace Variable							
				product['description'] = product['description'].replace(ATTRIBUTES_VARIABLE, translatedAttr)											

		# return product
		return product