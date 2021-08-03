# coding=utf-8
import sys
from db.Select import Select
from itertools import permutations
from lib.Helper import Helper
from lib.Issue import Issue
#
from lib.Translate.TranslateBeforeLastDash import TranslateBeforeLastDash
#from lib.Translate.TranslateAfterLastDash import TranslateAfterLastDash

# Fixing can't encode unichar issue
reload(sys)
sys.setdefaultencoding('utf8')

class Translate:
	def __init__(self, country, products):		
		self.country = country		
		self.products = products

	# Before Last Dash
	def makeBeforeAfterLastDash(self):
		translateBeforeLastDash = TranslateBeforeLastDash()
		products = self.products

		for product in products:
			if products[product]['productType'] == 'cover' or products[product]['productType'] == 'case':
				products[product]['name'] = translateBeforeLastDash.make(products[product]['name'], self.country)

			print products[product]['name']
		#


	
	# # After Last Dash
	# def makeAfterLastDash(self):
	# 	translateAfterLastDash = TranslateAfterLastDash()
	# 	translateAfterLastDash.make()
		



	# Replacing / Translate Prepositions (with, in, and, for)
	def productPrepositions(self):
		products = self.products		
		select = Select(self.country)
		prepositions = select.prepositions()
		helper = Helper()

		for key in products:
			if products[key]['productType'] == 'cover' or products[key]['productType'] == 'case':
				# Split all words in lastDash lists.
				beforeLastDash = products[key]['name'].split(' - ')[0]								
				afterLastDash = products[key]['name'].split(' - ')[-1].lower()						

				# AfterLastDash
				i = 0
				for currentWord in afterLastDash.split(' '):
					# If currentWord exists as a dict.key and has a translated version
					if currentWord in prepositions.keys() and prepositions[currentWord]:						
						products[key]['name'] = beforeLastDash + ' - ' + afterLastDash.replace(' ' + currentWord + ' ', ' ' + prepositions[currentWord] + ' ')
					i += 1

			if products[key]['productType'] == 'screenprotector':
				# Check if prepositionsKey is in name, and replace
				products[key]['name'] = helper.dictKeyInString(prepositions, products[key]['name'])

		# Done
		return products

	# Replacing / Translatin Verbs (holding, wearing)
	def productVerbs(self):		
		products = self.products		
		select = Select(self.country)
		verbs = select.verbs()
		helper = Helper()				

		i = 0
		for key in products:
			if products[i]['productType'] == 'cover' or products[i]['productType'] == 'case':				
				# Break up name
				beforeAndAfterLastDash = helper.beforeAndAfterLastDash(products[i]['name'])
				beforeLastDash = beforeAndAfterLastDash[0]
				afterLastDash = beforeAndAfterLastDash[1]

				# Loop through each word in afterLastDash
				ii = 0
				for currentWord in afterLastDash:					
					# if currentWord exists as verb and there is a translated version
					if currentWord in verbs.keys() and verbs[currentWord]:
						# replace currentWord with translated verb
						afterLastDash[ii] = verbs[currentWord]						

					ii += 1 # Current word iterator
								
				# Converting [afterLastDash] to a String				
				afterLastDashString = ' '.join([str(elem) for elem in afterLastDash])
				# Creating the new name	
				products[i]['name'] = helper.createName(beforeLastDash, afterLastDashString)							

			i += 1 # Product iterator

		return products
	
	# SINGULAR LOOK WORDS: (Single Mofif words)
	def productSingularMotifAndColor(self):
		products = self.products		
		select = Select(self.country)
		helper = Helper()
		# Looks
		lookWords = select.lookWords()
		lookSingularWords = lookWords[0]		
		# Colors
		colorWords = select.colorWords()
		colorSingularWords = colorWords[0]
		# Adjectives
		adjectiveWords = select.adjectives()		
		adjectives = adjectiveWords[0]		

		i = 0
		for key in products:			
			if products[i]['productType'] == 'cover' or products[i]['productType'] == 'case':				
				# Before and After last dash
				beforeAndAfterLastDash = helper.beforeAndAfterLastDash(products[i]['name'])
				beforeLastDash = beforeAndAfterLastDash[0]
				afterLastDash = beforeAndAfterLastDash[1]
								
				# Loops trough every word afterLastDashList				
				ii = 0
				for currentWord in afterLastDash:					
					currentWord = afterLastDash[ii]
					previousWord = afterLastDash[ii - 1]									
					
					# If currentword exists in lookPluralWords					
					if currentWord in lookSingularWords.keys():
						# Replace word in afterLastDash at current index						
						afterLastDash[ii] = lookSingularWords[currentWord]['local']

						# Check if previousWord is a color and there is a translated version						
						if previousWord in colorSingularWords.keys() and colorSingularWords[previousWord]:							
							# Get the indefinite_article of current word, is it 2 use color_neutrum
							if lookSingularWords[currentWord]['indefinite_article'] == '2':
								# replace with neutrum color																								
								afterLastDash[ii - 1] = colorSingularWords[previousWord]['neutrum']
							else:
								afterLastDash[ii - 1] = colorSingularWords[previousWord]['local']

						# If previousWord exists as adjective
						if previousWord in adjectives.keys():
							afterLastDash[ii - 1] = adjectives[previousWord]['singular']
					ii += 1
								
				# Converting [afterLastDash] to a String								
				afterLastDashString = ' '.join([str(elem) for elem in afterLastDash])				
				# Creating the new name	
				products[i]['name'] = helper.createName(beforeLastDash, afterLastDashString)
				
			i += 1
		# Done
		return products

	# PLURAL LOOK WORDS: (Plural Mofif words)		
	def productPluralMotifAndColor(self):
		products = self.products		
		select = Select(self.country)
		helper = Helper()
		# Looks
		lookWords = select.lookWords()		
		lookPluralWords = lookWords[1]
		# Colors
		colorWords = select.colorWords()		
		colorPluralWords = colorWords[1]
		# Adjectives
		adjectiveWords = select.adjectives()		
		adjectives = adjectiveWords[1]
		
		i = 0
		for key in products:			
			if products[i]['productType'] == 'cover' or products[i]['productType'] == 'case':				
				# Before and After last dash
				beforeAndAfterLastDash = helper.beforeAndAfterLastDash(products[i]['name'])
				beforeLastDash = beforeAndAfterLastDash[0]
				afterLastDash = beforeAndAfterLastDash[1]
				
				# Loops trough every word afterLastDashList				
				ii = 0
				for currentWord in afterLastDash:

					currentWord = afterLastDash[ii]
					previousWord = afterLastDash[ii - 1]									
					
					# If currentword exists in lookPluralWords					
					if currentWord in lookPluralWords:
						# Replace word in afterLastDash at current index
						afterLastDash[ii] = lookPluralWords[currentWord]

						# If previousWord exists in colorPluralWords. 						
						if previousWord in colorPluralWords.keys():
							# Replace with plural color
							afterLastDash[ii - 1] = colorPluralWords[previousWord]

						# If previousWord exists as adjective
						if previousWord in adjectives.keys():							
							afterLastDash[ii - 1] = adjectives[previousWord]
							
					ii += 1
								
				# Converting [afterLastDash] to a String				
				afterLastDashString = ' '.join([str(elem) for elem in afterLastDash])
				# Creating the new name	
				products[i]['name'] = helper.createName(beforeLastDash, afterLastDashString)				

			i += 1
	
		# Done		 		
		return products
	
	# Replace Colors after last dash in product name (Where afterLastDash only exists of colors, and not motif)
	def productNameColor(self):
		products = self.products
		select = Select(self.country)
		# colors is used for Cover and Cases, This should be refactored, so we only use ColorWords
		#colors = select.colors()
		colors = select.colorWords()
		colorSingularWords = colors[0]		
		helper = Helper()
		issue = Issue()						

		# Iterate through products 
		i = 0
		for key in products:			
			# Change For Only Covers/Cases,watchstrap
			if products[i]['productType'] == 'cover' or products[i]['productType'] == 'case' or products[i]['productType'] == 'watchstrap':
				# Getting beforeLastdash and afterLastdash
				beforeAndAfterLastDash = helper.beforeAndAfterLastDash(products[i]['name'])
				beforeLastDash = beforeAndAfterLastDash[0]
				afterLastDash = beforeAndAfterLastDash[1]

				# Convert AfterLastDash to a string, with space between elements
				afterLastDashString = ''
				for ele in afterLastDash:
					afterLastDashString += ele + ' '

				## Translate After Last Dash
				# If words has a space, and exists as a key in colorSingularWords			
				if len(afterLastDash) > 1 and ' '.join(afterLastDash) in colorSingularWords.keys():
					# If translated version exists
					if colorSingularWords[' '.join(afterLastDash)]['local']:
						afterLastDash = colorSingularWords[' '.join(afterLastDash)]['local']					
					# Else give a error message (If transled color missing)
					else:
						issue.criticalErrorMsg(''.join(afterLastDash) + ' Missing Translated Version')	

					# Converting [afterLastDash] to a String				
					afterLastDashString = ''.join([str(elem) for elem in afterLastDash])

				# If afterLastDash is separated with spaces
				if '/' in afterLastDash:
					# Split afterLastDashToString with /
					afterLastDashSplit = afterLastDashString.split(' / ')
					for string in afterLastDashSplit:
						# Strip away spaces around the word
						string = string.strip()
						# If string exists as a key
						if string in colorSingularWords.keys():
							# If translated version exist
							if colorSingularWords[string]['local']:								
								# Replace current index with translated word
								afterLastDashString = afterLastDashString.replace(string, colorSingularWords[string]['local'])
							# Else give a error message (If transled color missing)
							else:
								issue.criticalErrorMsg(''.join(afterLastDash) + ' Missing Translated Version')																

				# Translate Single Words				
				# If afterLastDash contains a single word And exists as a color keys
				if len(afterLastDash) == 1 and ''.join(afterLastDash) in colorSingularWords.keys():															
					# If there is a translated version.
					if colorSingularWords[''.join(afterLastDash)]['local']:						
						# Replace first index, with translated color					
						afterLastDash[0] = colorSingularWords[''.join(afterLastDash)]['local']
					# Else give a error message (If translated color missing)
					else:
						issue.criticalErrorMsg(''.join(afterLastDash) + ' Missing Translated Version')

					# Converting [afterLastDash] to a String				
					afterLastDashString = ''.join([str(elem) for elem in afterLastDash])

				# Creating the new name	
				products[i]['name'] = helper.createName(beforeLastDash, afterLastDashString)

			# Product Iterator
			i += 1
			
		# Return products
		return products
		
	# Product Material
	def productMaterial(self):
		products = self.products
		select = Select(self.country)		
		productMaterials = select.productMaterials()		
		helper = Helper()
		#issue = Issue()

		i = 0
		for key in products:
			beforeAndAfterLastDash = helper.beforeAndAfterLastDash(products[i]['name'])
			beforeLastDash = beforeAndAfterLastDash[0]
			afterLastDash = beforeAndAfterLastDash[1]
			
			if products[i]['productType'] == 'cover' or products[i]['productType'] == 'case' or products[i]['productType'] == 'watchstrap':							
				# if material exist in beforeLastDash
				beforeLastDash = helper.dictKeyInString(productMaterials, beforeLastDash)							
				# Converting [afterLastDash] to a String				
				afterLastDashString = ' '.join([str(elem) for elem in afterLastDash])
				# Create Name
				products[i]['name'] = helper.createName(beforeLastDash, afterLastDashString)

			i += 1

		return products		

	# Product Feature
	def productFeature(self):
		products = self.products
		select = Select(self.country)
		productFeatures = select.productFeatures()
		helper = Helper()

		i = 0
		for key in products:
			beforeAndAfterLastDash = helper.beforeAndAfterLastDash(products[i]['name'])
			beforeLastDash = beforeAndAfterLastDash[0]
			afterLastDash = beforeAndAfterLastDash[1]

			if products[i]['productType'] == 'cover' or products[i]['productType'] == 'case' or products[i]['productType'] == 'watchstrap':	
				# if feature exist in beforeLastDash
				beforeLastDash = helper.dictKeyInString(productFeatures, beforeLastDash)

				# Converting [afterLastDash] to a String				
				afterLastDashString = ' '.join([str(elem) for elem in afterLastDash])
				# Create Name
				products[i]['name'] = helper.createName(beforeLastDash, afterLastDashString)

			i += 1

		return products



	# Replace productType / Flip case, Cover, Leather flip case etc.
	def productNameType(self):
		products = self.products
		select = Select(self.country)
		productTypes = select.productTypes()	
		helper = Helper()
		issue = Issue()		

		i = 0
		for key in products:
			# Getting beforeLastdash and afterLastdash
			beforeAndAfterLastDash = helper.beforeAndAfterLastDash(products[i]['name'])
			beforeLastDash = beforeAndAfterLastDash[0]
			afterLastDash = beforeAndAfterLastDash[1]			

			# Change For Only Covers and Cases
			if products[i]['productType'] == 'cover' or products[i]['productType'] == 'case':
				# before last dash
				beforeLastDash = ' - '.join(products[i]['name'].split(' - ')[:-1])				
				# Loop trough product types keys. Sorted by length of key, so flip case will get translated first
				for productType in sorted(productTypes.keys(), key=len, reverse=True):															
					# If productTypes.keys() exists as a substring in name (Last three words, beforelastdash)										
					if productType in ' '.join(beforeLastDash.split()[3:]).lower():						
						# If there is a translated version as productTypes.value():
						if productTypes[productType] != '':							
							# Replace substring, with spaces " MAN DEV Xcover Case - Red"						
							products[i]['name'] = products[i]['name'].replace(' ' + productType + ' ', ' ' + productTypes[productType].capitalize() + ' ')	

			# If producttype is screenprotector			
			if products[i]['productType'] == 'screenprotector':
				# Each permutation of name
				for permutation in permutations(products[i]['name'].lower().split( ), 2):
					# Let permutation be string
					permutation = str(' '.join(permutation))					
					# If Permutation exist as a productType key, and translated version exists
					if permutation in productTypes.keys() and productTypes[permutation] != '':
						# Replace permuation in name with productTypes[value] 																								
						products[i]['name'] = products[i]['name'].lower().replace(permutation, productTypes[permutation])

					## ERROR MSG
					# If permutation exists but translated version is empty
					if permutation in productTypes.keys() and productTypes[permutation] == '':
						issue.criticalErrorMsg(permutation + ' missing translated version')						

			# if productType is watchstrap
			if products[i]['productType'] == 'watchstrap':				
				# if productType exist in beforeLastDash
				beforeLastDash = helper.dictKeyInString(productTypes, beforeLastDash)		
				
				# Converting [afterLastDash] to a String				
				afterLastDashString = ' '.join([str(elem) for elem in afterLastDash])
				# Create Name
				products[i]['name'] = helper.createName(beforeLastDash, afterLastDashString)	

			# Products iteration
			i += 1

		# Return product
		return products	

	# All Done
	def done(self):
		products = self.products
		return products