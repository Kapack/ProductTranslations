from db.Select import Select
from itertools import permutations
from lib.Helper import Helper

# Analyse Skus
class Append:	
	def __init__(self, country:str, products:dict):
		self.country = country
		self.products = products

	# Getting Product type from SKU.
	# Returning attributes in a new dict
	def productType(self) -> dict:
		products = self.products
		# Loop trough products dict
		i = 0
		for key in products:			
			products[i]['productType'] = 'unknown'
			# Cover and Cases / If a sku starts with LC and has a digit in the third place, It's a cover or case
			if products[i]['sku'][0:2].upper() == 'LC' and products[i]['sku'][2:3].isdigit():                
				if products[i]['sku'].split('-')[2][0] == '1':
					products[i]['productType'] = 'cover'					
				# If skus is == LCXX-XX-5XXX-X it's a case
				elif products[i]['sku'].split('-')[2][0] == '5' and products[i]['sku'].split('-')[0] != 'LC40' and products[i]['sku'].split('-')[0] != 'LC41':	
					products[i]['productType'] = 'case'

				# LC40-XX-XX
				elif products[i]['sku'].split('-')[0] == 'LC40':
					products[i]['productType'] = 'pouch'
                
				# LC41-XX-XXXX-X
				elif products[i]['sku'].split('-')[0] == 'LC41':
					products[i]['productType'] = 'armband'

			# Screen protector
			elif products[i]['sku'][0:3].upper() == 'LCS' and products[i]['sku'][4:5].isdigit():
				products[i]['productType'] = 'screenprotector'

			# Watchstrap
			elif products[i]['sku'][0:3].upper() == 'LCW' and products[i]['sku'][4:5].isdigit():
				products[i]['productType'] = 'watchstrap'
            
			# Camera
			elif products[i]['sku'][0:3].upper() == 'LCC' and products[i]['sku'][4:5].isdigit():
				products[i]['productType'] = 'camera'                     

			# Speaker
			elif products[i]['sku'][0:3].upper() == 'LCM' and products[i]['sku'][4:5].isdigit():
				products[i]['productType'] = 'speaker'
            
			# Fidget Spinner
			elif products[i]['sku'][0:3].upper() == 'LCF' and products[i]['sku'][4:5].isdigit():
				products[i]['productType'] = 'fidgetspinner'

			# Headphone
			elif products[i]['sku'][0:5].upper() == 'LCA10' and products[i]['sku'][7:8].isdigit():
				products[i]['productType'] = 'headphone'

			# Charger
			elif products[i]['sku'][0:5].upper() == 'LCA15' and products[i]['sku'][7:8].isdigit():
				products[i]['productType'] = 'charger'                

			# Stands & Holders
			elif products[i]['sku'][0:5].upper() == 'LCA25' and products[i]['sku'][7:8].isdigit():
				products[i]['productType'] = 'standHolder'                                

			# Car Holder
			elif products[i]['sku'][0:5].upper() == 'LCA35' and products[i]['sku'][7:8].isdigit():
				products[i]['productType'] = 'carholder'

			# Bike Holder
			elif products[i]['sku'][0:5].upper() == 'LCA36' and products[i]['sku'][7:8].isdigit():
				products[i]['productType'] = 'bikeholder'       

			# Mini speaker
			elif products[i]['sku'][0:5].upper() == 'LCA45' and products[i]['sku'][7:8].isdigit():
				products[i]['productType'] = 'miniSpeaker'

			# Cables and Adapters
			elif products[i]['sku'][0:6].upper() == 'LCA555' and products[i]['sku'][8:9].isdigit():
				products[i]['productType'] = 'cablesAdapter'                                                          

			# Accessories
			elif products[i]['sku'][0:5].upper() == 'LCA65' and products[i]['sku'][7:8].isdigit():
				products[i]['productType'] = 'accessories'

			# Sparepart
			elif products[i]['sku'][0:3].upper() == 'LCP' and products[i]['sku'][5:6].isdigit():
				products[i]['productType'] = 'sparepart'

			# Sparepart
			elif products[i]['sku'][0:3].upper() == 'LCT' and products[i]['sku'][5:6].isdigit():
				products[i]['productType'] = 'tool' 
							
			i += 1
		
		return products

	def deviceAndModel(self) -> dict:
		products = self.products
		select = Select(self.country)
		deviceList = select.deviceList()
					

		i = 0
		# Loop trough Products		
		for product in products:			
			ii = 0
			# Loop trough DeviceList
			for device in deviceList:
				
				# Default manSku and DevSku.
				# Will Get overwrited if exists, othervise will stay empty
				manSku = ''
				devSku = ''

				# Assigning manSku and devSku
				# If Cover and Cases - For LCXX-XX, Where XX is numbers (Meaning no Accessories etc.)
				if products[i]['productType'] == 'cover' or products[i]['productType'] == 'case':
					# Get Product Manufacturer and Device SKUs
					manSku = products[i]['sku'].split('-')[0][2:4]
					devSku = products[i]['sku'].split('-')[1]

				# If screen protectors
				elif products[i]['productType'] == 'screenprotector':
					manSku = products[i]['sku'].split('-')[0][3:5]
					devSku = products[i]['sku'].split('-')[1]

				# If watchstrap
				elif products[i]['productType'] == 'watchstrap':
					manSku = products[i]['sku'].split('-')[0][3:5]					
					devSku = products[i]['sku'].split('-')[1]			
								
				# Assigning Correct Man and Dev Names
				# If manSku has a match in deviceList
				if manSku == deviceList[ii]['manSku']:
					products[i]['device']['manName'] = deviceList[ii]['manName']
				
				# Assign devName, "out" from mansku
				if manSku == deviceList[ii]['manSku'] and devSku == deviceList[ii]['devSku']:
					products[i]['device']['devName'] = deviceList[ii]['devName']

				# Device list iterator
				ii += 1
			# product list iterator
			i += 1

		return products

	# Appending products{... 'attributes' : {...} }
	# Colors
	def attributeColor(self) -> dict:
		products = self.products
		helper = Helper()
		select = Select(self.country)
		colors = select.colors()
		singularColors = colors[0]

		for product in products:			
			# Break up name
			beforeAndAfterLastDash = helper.beforeAndAfterLastDash(products[product]['name'])
			afterLastDash = beforeAndAfterLastDash[1]
								
			# If single Color
			if len(afterLastDash) == 1:				
				if afterLastDash[0] in singularColors.keys():
					products[product]['attributes']['color'].append(afterLastDash[0])
			
			# If colors is seperated by dash
			if '/' in afterLastDash:
				for word in afterLastDash:
					if word in singularColors:
						products[product]['attributes']['color'].append(word)		
		# Return
		return products					


	# Material
	def attributeMaterial(self) -> dict:
		products = self.products
		helper = Helper()
		select = Select(self.country)
		materials = select.productMaterials()
		# Sort materials.keys() by length so we will overwrite product{..attribute{'material' : ''}} leather with genuine leather
		materialsList = sorted(materials.keys(), key=len)

		for product in products:
    		# Break up name
			beforeAndAfterLastDash = helper.beforeAndAfterLastDash(products[product]['name'])
			beforeLastDash = beforeAndAfterLastDash[0]
			# Convert beforeLastDash into a list
			beforeLastDashList = beforeLastDash.lower().split()
			# Loop trough materials
			for material in materialsList:				
				# If material is beforeLastDash string
				if beforeLastDash.find(material) != -1:
					products[product]['attributes']['material'] = material		
		# Return
		return products					

	# Features
	def attributeFeature(self) -> dict:
		products = self.products
		helper = Helper()
		select = Select(self.country)
		features = select.productFeatures()
		featuresList = sorted(features.keys(), key=len)

		for product in products:			
    		# Break up name
			beforeAndAfterLastDash = helper.beforeAndAfterLastDash(products[product]['name'])
			beforeLastDash = beforeAndAfterLastDash[0]
			# Convert beforeLastDash into a list
			beforeLastDashList = beforeLastDash.lower().split()
			# Loop trough features
			for feature in featuresList:
				# If feature is beforeLastDash string
				if beforeLastDash.find(feature) != -1:
					products[product]['attributes']['feature'] = feature
		# Return
		return products					
	
	# Product Size
	def attributeSize(self) -> dict:		
		products = self.products

		for product in products:			
			# Product sizes for Watchstraps 
			if products[product]['productType'] == 'watchstrap':
				# Split the description up
				descList = products[product]['description'].lower().split()					
				
				# Iterate
				i = 0
				for word in descList:
					# Only create nextWord, if possible (Out of range)
					if int(i + 1) < len(descList):
						nextWord = descList[i+1]

					# If desc. contains
					if word == 'length:' or word == 'length':						
						# If next word contains mm or cm (To elimate possible errors)
						if nextWord.find('cm') != -1 or nextWord.find('mm') != -1:
							products[product]['sizes']['length'] = nextWord

					if word == 'width:' or word == 'width':
						if nextWord.find('cm') != -1 or nextWord.find('mm') != -1:
							products[product]['sizes']['width'] = nextWord

					if word == 'size:' or word == 'size':
						if nextWord.find('cm') != -1 or nextWord.find('mm') != -1:
							products[product]['sizes']['size'] = nextWord

					if word == 'circumference:' or word == 'circumference':
						if nextWord.find('cm') != -1 or nextWord.find('mm') != -1:
							products[product]['sizes']['circumference'] = nextWord

					i += 1
		
		# Return products back
		return products
				
	# Product Templates
	def product2021Template(self) -> dict:
		# Templates for productTypes?
		products = self.products
		select = Select(self.country)
		helper = Helper()
		product2021Templates = select.product2021Templates()

		# Loop trough producs
		i = 0
		for product in products:
			beforeAndAfterLastDash = helper.beforeAndAfterLastDash(products[product]['name'])
			beforeLastDash = beforeAndAfterLastDash[0]			
			
			# Looping trough each key
			for key in product2021Templates:
				# if key exists in part of beforeLastDash
				if key in beforeLastDash.lower():
					# Assign key to productDict
					products[i]['template'] = key
			i += 1
		
		# Return products
		return products

	# Decides which product template to use
	def product2020Template(self) -> dict:
		products = self.products
		select = Select(self.country)
		product2020Templates = select.product2020Templates()		

		# Get all templateKeys length (We need this for permuations later)
		templateKeyLen = []
		for templateKey in product2020Templates.keys():
			templateKeyLen.append(len(templateKey.split()))

		# Get highest int, and remove duplicates
		templateKeyLen = list(dict.fromkeys(templateKeyLen))
		
		# Loop trough each product name template
		i = 0
		for key in products:
			beforeLastDash = products[i]['name'].split(' - ')[0].lower()
			# templateKey = ''
			
			# For Covers and Cases Only and not template has been assigned
			if products[i]['productType'] == 'cover' or products[i]['productType'] == 'case' or products[i]['productType'] == 'screenprotector' and products[i]['template'] != '':
				# For each max length in templateKeyLen. Plus one because it counts from 0
				for tempKeyLen in range(max(templateKeyLen) + 1):					
					# Every permuation of beforeLastDash. Second argument is length of permuation.
					for permutation in permutations(beforeLastDash.split( ), tempKeyLen):						
						# If permutation exists as a productTemplates_keys					
						if ' '.join(permutation) in product2020Templates.keys():						
							# Give product the template key
							products[i]['template'] = ' '.join(permutation)
			i += 1
		
		# Return
		return products