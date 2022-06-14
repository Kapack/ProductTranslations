from db.Select import Select
from lib.Helper import Helper
from lib.Shared.Shared import Shared

"""
Translates all words AFTER last dash (Motifs, colors etc.)
Translated Product Types: Covers and Cases.

"""

class CoverCaseAfterLastDash:
	def make(self, productName:str, country:str) -> str:		
		helper = Helper()
		# Break up name
		beforeAndAfterLastDash = helper.beforeAndAfterLastDash(productName = productName)
		beforeLastDash = beforeAndAfterLastDash[0]
		afterLastDash = beforeAndAfterLastDash[1]

		# Go Trough Translations methods		
		afterLastDash = self.productNameSingleColor(afterLastDash = afterLastDash, country = country)		
		# afterLastDash = self.productNameLongColor(afterLastDash, country)		
		afterLastDash = self.productSingularMotifAndColor(afterLastDash = str(afterLastDash), country = country)
		afterLastDash = self.productPluralMotifAndColor(afterLastDash = str(afterLastDash), country = country)
		afterLastDash = self.productVerbs(afterLastDash = str(afterLastDash), country = country)
		afterLastDash = self.productPrepositions(afterLastDash = str(afterLastDash), country = country)

		# Create new name
		# Converting [afterLastDash] to a String
		afterLastDashString = ''.join([str(elem) for elem in afterLastDash])		
		productName = helper.createName(beforeLastDash = beforeLastDash, afterLastDashString = afterLastDashString)		
		# Return new name
		return productName

	# Translated Single Colors (Incl. slashes) in afterLastDash
	def productNameSingleColor(self, afterLastDash:str, country:str) -> str:
		shared = Shared()		
		afterLastDashString = shared.productNameSingleColor(afterLastDash = afterLastDash, country = country)
		return afterLastDashString

	# Replace Colors (Where afterLastDash only exists of colors, and not motif)
	# Translate "Long" Colors (Dark Blue, Wine Red)
	def productNameLongColor(self, afterLastDash:str, country:str) -> str:		
		shared = Shared()		
		afterLastDashString = shared.productNameLongColor(afterLastDash = afterLastDash, country = country)		
		return afterLastDashString

	# SINGULAR LOOK WORDS: (Single Mofif word / Green Leaf, Yellow Owl)
	def productSingularMotifAndColor(self, afterLastDash:str, country:str) -> str:
		shared = Shared()
		afterLastDashString = shared.productNameSingularMotif(afterLastDash = afterLastDash, country = country)
		return afterLastDashString
	
	# PLURAL LOOK WORDS: (Plural Mofif words / Green Leafs, Yellow Owls)
	def productPluralMotifAndColor(self, afterLastDash:str, country:str) -> str:		
		shared = Shared()
		afterLastDashString = shared.productPluralMotifAndColor(afterLastDash = afterLastDash, country = country)
		return afterLastDashString

	# Replacing / Translating Verbs (holding, wearing)
	def productVerbs(self, afterLastDash:str, country:str) -> str:
		helper = Helper()
		select = Select(country)
		verbs = select.verbs()		

		# Convert afterLastDash into a List
		afterLastDashList = afterLastDash.split()

		# Loops trough every word afterLastDashList
		i = 0
		for currentWord in afterLastDashList:
			# if currentWord exists as verb
			if currentWord in verbs.keys():
				# replace currentWord with translated verb
				afterLastDashList[i] = helper.checkIfTranslatedExists(typeDict=verbs, word=currentWord)								
			i += 1
		
		# Converting [afterLastDash] to a String				
		afterLastDashString = ' '.join([str(elem) for elem in afterLastDashList])
		return afterLastDashString

	# Replaces / Translate Prepositions (with, in, and, for)
	def productPrepositions(self, afterLastDash:str, country:str) -> str:
		shared = Shared()
		afterLastDashString = shared.productPrepositions(afterLastDash = afterLastDash, country = country)
		return afterLastDashString