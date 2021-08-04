from db.Select import Select
from lib.Helper import Helper
from lib.Issue import Issue

"""
Translates all words BEFORE last dash (Material, feature etc.)
Translated Product Types: Covers and Cases.
"""

class CoverCaseBeforeLastDash:
	def make(self, productName, country):
		helper = Helper()
		# Break up name
		beforeAndAfterLastDash = helper.beforeAndAfterLastDash(productName)
		beforeLastDash = beforeAndAfterLastDash[0]
		afterLastDash = beforeAndAfterLastDash[1]

		# Go Trough Translations methods		
		beforeLastDash = self.productFeature(beforeLastDash, country)
		beforeLastDash = self.productMaterial(beforeLastDash, country)
		beforeLastDash = self.productNameType(beforeLastDash, country)
		beforeLastDash = self.productPrepositions(beforeLastDash, country)
			
		# Converting [afterLastDash] to a String				
		afterLastDashString = ' '.join([str(elem) for elem in afterLastDash])
		# Create new name
		productName = helper.createName(beforeLastDash, afterLastDashString)
		# Return new name		
		return productName

	# Product Feature
	def productFeature(self, beforeLastDash, country):
		helper = Helper()
		select = Select(country)
		productFeatures = select.productFeatures()

		# if feature exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(productFeatures, beforeLastDash)

		return beforeLastDash

	# Product Material
	def productMaterial(self, beforeLastDash, country):
		helper = Helper()
		select = Select(country)		
		productMaterials = select.productMaterials()				

		# if material exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(productMaterials, beforeLastDash)		

		return beforeLastDash

	# Replace productType / Flip case, Cover, Leather flip case etc.
	def productNameType(self, beforeLastDash, country):		
		helper = Helper()
		select = Select(country)
		productTypes = select.productTypes()
		issue = Issue()

		beforeLastDash = helper.dictKeyInString(productTypes, beforeLastDash)
		

		# # Loop trough product types keys. Sorted by length of key, so flip case will get translated first
		# for productType in sorted(productTypes.keys(), key=len, reverse=True):
		# 	# If productTypes.keys() exists as a substring in name (Last three words, beforelastdash)										
		# 	if productType in ' '.join(beforeLastDash.split()[3:]).lower():
		# 		# If there is a translated version as productTypes.value():
		# 		if productTypes[productType] != '':					
		# 			# Replace substring, with spaces " MAN DEV Xcover Case - Red"
		# 			beforeLastDash = beforeLastDash.replace(productType, productTypes[productType])
		# 			print beforeLastDash

		# 		else:
		# 			issue.warningErrorMsg(productTypes[productType] + ' missing translated version')					
		
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



