from db.Select import Select
from lib.Helper import Helper
from lib.Issue import Issue
import re

"""
Translates all words BEFORE last dash (Material, feature etc.)
Translated Product Types: Covers and Cases.
"""

class CoverCaseBeforeLastDash:
	def make(self, productName, country, product=None):
		helper = Helper()
		# Break up name
		beforeAndAfterLastDash = helper.beforeAndAfterLastDash(productName)
		beforeLastDash = beforeAndAfterLastDash[0]
		afterLastDash = beforeAndAfterLastDash[1]

		# Go Trough Translations methods				
		beforeLastDash = self.productNameType(beforeLastDash, country, product)
		beforeLastDash = self.productFeature(beforeLastDash, country, product)
		beforeLastDash = self.productMaterial(beforeLastDash, country, product)			
		beforeLastDash = self.productPrepositions(beforeLastDash, country)
			
		# Converting [afterLastDash] to a String				
		afterLastDashString = ' '.join([str(elem) for elem in afterLastDash])
		# Create new name
		productName = helper.createName(beforeLastDash, afterLastDashString)
		# Return new name		
		return productName
		
	# Replace productType / Flip case, Cover, Leather flip case etc.
	def productNameType(self, beforeLastDash, country, product):				
		select = Select(country)
		productTypes = select.productTypes()
		issue = Issue()

		# Loop through productTypes, start with the longest (word count) productType key
		for productType in sorted(productTypes, key=len, reverse=True):			

			# Check if translated version exists
			if productTypes[productType] != '':				
				# if productType is in beforeLastDash, and type is not part of the device dev name (LG Style 3) (regular expression, r"\b" word boundaries)
				if re.search(r"\b" + re.escape(productType.lower()) + r"\b", beforeLastDash.lower()) and productType not in product['device']['devName'].lower():				
					# Replace translated productType in beforeLastDash
					beforeLastDash = beforeLastDash.lower().replace(productType, productTypes[productType])			
			else:
				issue.warningErrorMsg('Missing Translated productType: ' + productType)				
		
		return beforeLastDash

	# Product Feature
	def productFeature(self, beforeLastDash, country, product):
		helper = Helper()
		select = Select(country)
		productFeatures = select.productFeatures()

		# if feature exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(productFeatures, beforeLastDash, product)

		return beforeLastDash

	# Product Material
	def productMaterial(self, beforeLastDash, country, product):
		helper = Helper()
		select = Select(country)		
		productMaterials = select.productMaterials()				

		# if material exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(productMaterials, beforeLastDash, product)		

		return beforeLastDash


	# Replace productType / Flip case, Cover, Leather flip case etc.
	def productNameType(self, beforeLastDash, country, product):				
		select = Select(country)
		productTypes = select.productTypes()
		issue = Issue()

		# Loop through productTypes, start with the longest (word count) productType key
		for productType in sorted(productTypes, key=len, reverse=True):

			# Check if translated version exists
			if productTypes[productType] != '':				
				# if productType is in beforeLastDash, and type is not part of the device dev name (LG Style 3) (regular expression, r"\b" word boundaries)
				if re.search(r"\b" + re.escape(productType.lower()) + r"\b", beforeLastDash.lower()) and productType not in product['device']['devName'].lower():				
					# Replace translated productType in beforeLastDash
					beforeLastDash = beforeLastDash.lower().replace(productType, productTypes[productType])			
			else:
				issue.warningErrorMsg('Missing Translated productType: ' + productType)				
		
		return beforeLastDash
	# Replace productType / Flip case, Cover, Leather flip case etc.
	def productNameType(self, beforeLastDash, country, product):				
		select = Select(country)
		productTypes = select.productTypes()
		issue = Issue()

		# Loop through productTypes, start with the longest (word count) productType key
		for productType in sorted(productTypes, key=len, reverse=True):			

			# Check if translated version exists
			if productTypes[productType] != '':				
				# if productType is in beforeLastDash, and type is not part of the device dev name (LG Style 3) (regular expression, r"\b" word boundaries)
				if re.search(r"\b" + re.escape(productType.lower()) + r"\b", beforeLastDash.lower()) and productType not in product['device']['devName'].lower():				
					# Replace translated productType in beforeLastDash
					beforeLastDash = beforeLastDash.lower().replace(productType, productTypes[productType])			
			else:
				issue.warningErrorMsg('Missing Translated productType: ' + productType)				
		
		return beforeLastDash

	# Replacing / Translate Prepositions (with, in, and, for)
	def productPrepositions(self, beforeLastDash, country):
		select = Select(country)
		prepositions = select.prepositions()
		helper = Helper()

		# Convert afterLastDash into a List
		beforeLastDashList = beforeLastDash.split()

		# Loops trough every word beforeLastDash
		i = 0
		for currentWord in beforeLastDashList:
			# If currentWord exists as a dict.key and has a translated version
			if currentWord in prepositions.keys() and prepositions[currentWord]:
				beforeLastDashList[i] = prepositions[currentWord]
			i += 1
		
		# Converting [afterLastDash] to a String				
		beforeLastDashString = ' '.join([str(elem) for elem in beforeLastDashList])
		return beforeLastDashString	



