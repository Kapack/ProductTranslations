from db.Select import Select
from itertools import permutations
from lib.Helper import Helper

# Analyse Skus
class Append:	
	def __init__(self, country, products):
		self.country = country
		self.products = products

	# Getting Product type from SKU.
	# Returning attributes in a new dict
	def productType(self):
		products = self.products
		# Loop trough products dict
		i = 0
		for key in products:
			# Cover and Cases / If a sku starts with LC and has a digit in the third place, It's a cover or case
			if products[i]['sku'][0:2].upper() == 'LC' and products[i]['sku'][2:3].isdigit():
				# If skus is == LCXX-XXX-1XXX-X it's a cover
				if products[i]['sku'].split('-')[2][0] == '1':
					products[i]['productType'] = 'cover'					
				# If skus is == LCXX-XX-5XXX-X it's a case
				elif products[i]['sku'].split('-')[2][0] == '5':	
					products[i]['productType'] = 'case'

			# Screen protector
			elif products[i]['sku'][0:3].upper() == 'LCS' and products[i]['sku'][4:5].isdigit():
				products[i]['productType'] = 'screenprotector'

			# Watchstrap
			elif products[i]['sku'][0:3].upper() == 'LCW' and products[i]['sku'][4:5].isdigit():
				products[i]['productType'] = 'watchstrap'
			
			# If productType is unknown
			else:
				products[i]['productType'] = 'other'			
			i += 1

	def deviceAndModel(self):
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
				if manSku == deviceList[ii]['manSku'] and devSku == deviceList[ii]['devSku']:					
					products[i]['manName'] = deviceList[ii]['manName']
					products[i]['devName'] = deviceList[ii]['devName']

				# Device list iterator
				ii += 1
			# product list iterator
			i += 1

		return products

	def product2021Template(self):
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
				if key in beforeLastDash:
					# Assign key to productDict
					products[i]['template'] = key

			i += 1
		
		# Return products
		return products

	# Decides which product template to use
	def product2020Template(self):
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

	# Return final dict
	def done(self):
		products = self.products
		return products