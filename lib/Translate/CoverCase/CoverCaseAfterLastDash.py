from db.Select import Select
from lib.Helper import Helper
from lib.Shared.Shared import Shared

"""
Translates all words AFTER last dash (Motifs, colors etc.)
Translated Product Types: Covers and Cases.

"""

class CoverCaseAfterLastDash:
	def make(self, productName, country):		
		helper = Helper()
		# Break up name
		beforeAndAfterLastDash = helper.beforeAndAfterLastDash(productName)
		beforeLastDash = beforeAndAfterLastDash[0]
		afterLastDash = beforeAndAfterLastDash[1]

		# Go Trough Translations methods		
		afterLastDash = self.productNameSingleColor(afterLastDash, country)		
		# afterLastDash = self.productNameLongColor(afterLastDash, country)		
		afterLastDash = self.productSingularMotifAndColor(str(afterLastDash), country)
		afterLastDash = self.productPluralMotifAndColor(str(afterLastDash), country)
		afterLastDash = self.productVerbs(str(afterLastDash), country)
		afterLastDash = self.productPrepositions(str(afterLastDash), country)

		# Create new name
		# Converting [afterLastDash] to a String				
		afterLastDashString = ''.join([str(elem) for elem in afterLastDash])		
		productName = helper.createName(beforeLastDash, afterLastDashString)		
		# Return new name
		return productName

	# Translated Single Colors (Incl. slashes) in afterLastDash
	def productNameSingleColor(self, afterLastDash, country):
		shared = Shared()		
		afterLastDashString = shared.productNameSingleColor(afterLastDash, country)			
		return afterLastDashString

	# Replace Colors (Where afterLastDash only exists of colors, and not motif)
	# Translate "Long" Colors (Dark Blue, Wine Red)
	def productNameLongColor(self, afterLastDash, country):		
		shared = Shared()		
		afterLastDashString = shared.productNameLongColor(afterLastDash, country)		
		return afterLastDashString

	# SINGULAR LOOK WORDS: (Single Mofif word / Green Leaf, Yellow Owl)
	def productSingularMotifAndColor(self, afterLastDash, country):
		shared = Shared()
		afterLastDashString = shared.productNameSingularMotif(afterLastDash, country)
		return afterLastDashString
	
	# PLURAL LOOK WORDS: (Plural Mofif words / Green Leafs, Yellow Owls)
	def productPluralMotifAndColor(self, afterLastDash, country):		
		shared = Shared()
		afterLastDashString = shared.productPluralMotifAndColor(afterLastDash, country)
		return afterLastDashString

	# Replacing / Translating Verbs (holding, wearing)
	def productVerbs(self, afterLastDash, country):
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
	def productPrepositions(self, afterLastDash, country):
		shared = Shared()
		afterLastDashString = shared.productPrepositions(afterLastDash, country)
		return afterLastDashString

		# helper = Helper()
		# select = Select(country)
		# prepositions = select.prepositions()		

		# # Convert afterLastDash into a List
		# afterLastDashList = afterLastDash.split()

		# # Loops trough every word afterLastDashList
		# i = 0
		# for currentWord in afterLastDashList:
		# 	# If currentWord exists as a dict.key
		# 	if currentWord in prepositions.keys():
		# 		afterLastDashList[i] = helper.checkIfTranslatedExists(typeDict=prepositions, word=currentWord)
		# 	i += 1
		
		# # Converting [afterLastDash] to a String				
		# afterLastDashString = ' '.join([str(elem) for elem in afterLastDashList])
		# return afterLastDashString