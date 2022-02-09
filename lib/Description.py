import random

# Adding Template Description
from db.Select import Select

class Description:
	def __init__(self, country, products):
		self.country = country
		self.products = products

	# Decides on template
	def loopProducts(self):
		products = self.products
		for product in products:
			
			# ## WIP
			# if products[product]['productType'] == 'watchstrap':
			# 	products[product] = self.watchStrapTemplate(products[product])

			# If product has a template attribute
			if products[product]['template'] != '':
				products[product] = self.productTemplate(products[product])

			# # WIP REPLACE VARIABLES	
			products[product] = self.replaceDescriptionVariables(products[product])

		# Return products back
		return products
				
	def productTemplate(self, product):		
		select = Select(self.country)
		product2021Templates = select.product2021Templates()
		product2020Templates = select.product2020Templates()		
		# Find correct template value, from productTemplates[key]. Searching for 
		template = product2020Templates.get(product['template']) or product2021Templates.get(product['template'])
		# Replace [DEVICE NAME] with Product Device name in template
		# template = template.replace('[DEVICE NAME]', product['device']['manName'] + ' ' + product['device']['devName'])
		# Assign correct template description
		product['description'] = template
		return product

	# Watchstraps templates / WIP
	def watchStrapTemplate(self, product):
		select = Select(self.country)	
		watchstrapTemplates = select.watchstrapTemplates()
		watchTemplate = []
		materialTemplates = select.watchstrapMaterialTemplates()
		matTemplate = []
		featureTemplates = select.watchstrapFeatureTemplates()
		fetTemplate = []
		sizeTemplates = select.watchstrapSizeTemplates()

		# First watchstrapTemplates
		i = 1
		for template in watchstrapTemplates:
			# Pick where has Attribute
			# Append templates to a list
			watchTemplate.append(watchstrapTemplates[i])
			# Pick a random, from above created list, and make it first element of our description
			product['description'] = random.choice(watchTemplate) + ' '			
			i += 1	

		# Insert material texts
		i = 1
		for materialTemplate in materialTemplates:
			# If product has a material attribute, matches materialTemplate and translated version exists
			if materialTemplates[i]['material'] == product['attributes']['material'] and materialTemplates[i]['template'] != '' :
				# Append matching templates to a list
				matTemplate.append(materialTemplates[i]['template'])
			i += 1

		# Pick a random, from above created list
		if matTemplate:							
			product['description'] += random.choice(matTemplate)
		
		# Inserting Feature Text		
		i = 1
		for featureTemplate in featureTemplates:
			# print featureTemplates[i]['template']
			if featureTemplates[i]['feature'] == product['attributes']['feature'] and featureTemplates[i]['feature'] != '' :								
				# Append matching templates to a list
				fetTemplate.append(featureTemplates[i]['template'])
			i += 1			
		
		# Pick a random, from above created list
		if fetTemplate:	
			product['description'] += random.choice(fetTemplate)		
		
		# Sizes
		# if translated sizeTemplates exists
		if sizeTemplates:
			# Split template into list, so we can find current/previous word and replace
			sizeTemplateList = sizeTemplates['template'].split()
			# Loop through all keys
			for dictKey in product['sizes']:
				# Check if product Key does not has value (If attribute is empty)
				if bool(product['sizes'][dictKey]) == False:					
					# If product does not have any value, remove variable string - eg. Width: [WIDTH] - from description					
					if sizeTemplates['template'].find('[' + dictKey.upper() + ']') != -1:
						# Find the index in the sizeTemplateList, where we have dictkey
						currentWordIndex = int(sizeTemplateList.index('[' + dictKey.upper() + '].')) # Notice the dot
						previousWordIndex = int(currentWordIndex - 1)
						# Remove current and previewous word
						sizeTemplateList.remove(sizeTemplateList[currentWordIndex])
						sizeTemplateList.remove(sizeTemplateList[previousWordIndex])
				
				# If currentProudct has attribute, replace variable in list with attribute
				else:
					sizeTemplateList = [word.replace('[' + dictKey.upper() + '].', product['sizes'][dictKey] + '.') for word in sizeTemplateList]
			
			# If sizeTemplateList only consists of one word, we don't want to use it
			if len(sizeTemplateList) != 1:
				# Make sizeTemplateList	back to a string and append to description.
				sizeTemplate = ' '.join([str(elem) for elem in sizeTemplateList])
				product['description'] += sizeTemplate

		# Compatibility
		# Package Included:		
		# Package included:
		# 1 x Watch Band
		# 1 x Screwdriver
		# Other items not included
		return product
	
	# Replace variables descriptions
	def replaceDescriptionVariables(self, product):
		select = Select(self.country)
		colors = select.colors()
		colorSingle = colors[0]

		# Replacing variables [COLOR] in text
		if product['description'].find('[COLOR]') != -1:
			# Get translated color
			descColor = ''
			for color in product['attributes']['color']:				
				descColor = ''.join(colorSingle[color]['local'])				
				print descColor
			# Replace variable in description			
			product['description'] = product['description'].replace('[COLOR]', descColor)

		# Replacing variables [MATERIAL] in text		
		if product['description'].find('[MATERIAL]') != -1:
			product['description'] = product['description'].replace('[MATERIAL]', product['attributes']['material'])

		# Replace [DEVIE NAME]
		if product['description'].find('[DEVICE NAME]') != -1:
			product['description'] = product['description'].replace('[DEVICE NAME]', product['device']['manName'] + ' ' + product['device']['devName'])
		
		# return product base
		return product