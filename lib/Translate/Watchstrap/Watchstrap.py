from lib.Helper import Helper
from db.Select import Select
from lib.Shared.Shared import Shared

"""
Translated Product Types: Watchstraps
"""

class Watchstrap:
	def translateName(self, productName:str, country:str, product:dict) -> str:
		helper = Helper()
		# Break up name
		beforeAndAfterLastDash = helper.beforeAndAfterLastDash(productName = productName)
		beforeLastDash = beforeAndAfterLastDash[0]
		afterLastDash = beforeAndAfterLastDash[1]

		# Go Trough Translations methods
		beforeLastDash = self.feature(beforeLastDash = beforeLastDash, country = country, product = product)
		beforeLastDash = self.prepositions(beforeLastDash = beforeLastDash, country = country, product = product)
		beforeLastDash = self.material(beforeLastDash = beforeLastDash, country = country, product = product)
		beforeLastDash = self.productNameType(beforeLastDash = beforeLastDash, country = country, product = product)
		afterLastDash = self.productNameColor(afterLastDash = afterLastDash, country = country)
		afterLastDash = self.singleColorCatchAll(afterLastDash = afterLastDash, country = country)
		afterLastDash = self.productNameSingularMotif(afterLastDash = afterLastDash, country = country)
		afterLastDash = self.productPluralMotifAndColor(afterLastDash = afterLastDash, country = country)
		afterLastDash = self.productPrepositions(afterLastDash = afterLastDash, country = country)
		afterLastDash = self.colorWithSize(afterLastDash = afterLastDash, country = country)
		afterLastDash = self.size(afterLastDash = afterLastDash, country = country, product = product)
		
		# Create new name		
		# Converting [afterLastDash] to a String				
		afterLastDashString = ''.join([str(elem) for elem in afterLastDash])
		productName = helper.createName(beforeLastDash, afterLastDashString)

		# Return productname
		return productName

	# Product Feature
	def feature(self, beforeLastDash:str, country:str, product:dict) -> str:
		helper = Helper()
		select = Select(country)
		productFeatures = select.productFeatures()

		# if feature exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(productFeatures, beforeLastDash, product)
		return beforeLastDash

	def prepositions(self, beforeLastDash:str, country:str, product:dict) -> str:
		helper = Helper()
		select = Select(country)
		prepositions = select.prepositions()

		# if prepositions exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(prepositions, beforeLastDash, product)
		return beforeLastDash

	# Product Material
	def material(self, beforeLastDash:str, country:str, product:dict) -> str:
		helper = Helper()
		select = Select(country)		
		productMaterials = select.productMaterials()
		# if material exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(productMaterials, beforeLastDash, product)
		return beforeLastDash
	
	# Replace productType / watchstrap etc.
	def productNameType(self, beforeLastDash:str, country:str, product:dict) -> str:		
		helper = Helper()
		select = Select(country)
		productTypes = select.productTypes()
		# if productType exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(productTypes, beforeLastDash, product)
		# Return
		return beforeLastDash

	# Replace Colors (Where afterLastDash only exists of colors, and not motif)
	# Translated Single Colors (Incl. slashes ) in afterLastDash
	def productNameColor(self, afterLastDash:str, country:str) -> str:
		shared = Shared()
		afterLastDashString = shared.productNameSingleColor(afterLastDash, country)
		return afterLastDashString

	def singleColorCatchAll(self, afterLastDash:str, country:str) -> str:
		shared = Shared()
		afterLastDashString = shared.singleColorCatchAll(afterLastDash, country)
		return afterLastDashString
	
	def productNameSingularMotif(self, afterLastDash:str, country:str) -> str:
		shared = Shared()
		afterLastDashString = shared.productNameSingularMotif(afterLastDash, country)
		return afterLastDashString

	def productPluralMotifAndColor(self, afterLastDash:str, country:str) -> str:		
		shared = Shared()
		afterLastDashString = shared.productPluralMotifAndColor(afterLastDash, country)
		return afterLastDashString
	
	# Replaces / Translate Prepositions (with, in, and, for)
	def productPrepositions(self, afterLastDash:str, country:str) -> str:
		shared = Shared()
		afterLastDashString = shared.productPrepositions(afterLastDash, country)
		return afterLastDashString

	# Where afterLastDash contains eg. black size: s
	def colorWithSize(self, afterLastDash:str, country:str) -> str:
		select = Select(country)
		colors = select.colors()
		colorSingle = colors[0]

		# if size exist in afterLastString
		if 'size' in afterLastDash.lower():
			# Split afterLastDash into list, so we can loop through each word and check if it exists as a key
			afterLastDashList = afterLastDash.lower().split()
			# Loop trough each word 
			for word in afterLastDashList:
				# if word exists as key in colorSingle
				if word.lower() in colorSingle.keys():
					# replace in afterLastDash
					afterLastDash = afterLastDash.replace(word, colorSingle[word]['local'])
					
		# Return afterLastDash
		return afterLastDash

	# Translate size in after last dash
	def size(self, afterLastDash:str, country:str) -> list:
		select = Select(country)
		productSizes = select.productSizes()

		stringList = afterLastDash.lower().split()
		newStringList = []

		for word in stringList:
			if word in productSizes.keys():
				word = productSizes[word]

			newStringList.append(word)

		newStringList = ' '.join([str(elem) for elem in newStringList])
		return newStringList