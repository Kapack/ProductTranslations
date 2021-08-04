# coding=utf-8
import sys

# Fixing can't encode unichar issue
reload(sys)
sys.setdefaultencoding('utf8')

from db.Select import Select
from lib.Helper import Helper
from lib.Translate.Shared.Shared import Shared
from lib.Issue import Issue

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
		afterLastDash = self.productNameColor(afterLastDash, country)		
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

	# Replace Colors (Where afterLastDash only exists of colors, and not motif)
	# Translated Single Colors (Incl. slashes ) in afterLastDash
	def productNameColor(self, afterLastDash, country):
		shared = Shared()		
		afterLastDashString = shared.productNameColor(afterLastDash, country)
		return afterLastDashString


	# SINGULAR LOOK WORDS: (Single Mofif words / Green Leaf, Yellow Owl)
	def productSingularMotifAndColor(self, afterLastDash, country):
		select = Select(country)
		helper = Helper()
		issue = Issue()
		
		# Looks
		lookWords = select.lookWords()
		lookSingularWords = lookWords[0]
		
		# Colors
		colorWords = select.colorWords()
		colorSingularWords = colorWords[0]

		# Adjectives
		adjectiveWords = select.adjectives()		
		adjectives = adjectiveWords[0]
		
		# Convert afterLastDash into a List
		afterLastDashList = afterLastDash.split()
		# Loops trough every word afterLastDashList
		i = 0
		for currentWord in afterLastDashList:
			previousWord = afterLastDashList[i - 1]

			# If currentword exists in lookSingularWords					
			if currentWord in lookSingularWords.keys():

				afterLastDashList[i] = helper.checkIfTranslatedExists(typeDict=lookSingularWords, word=currentWord, key='local')
																
				# Check if previousWord is a color and there is a translated version						
				if previousWord in colorSingularWords.keys() and colorSingularWords[previousWord]:					
					# Get the indefinite_article of current word, is it 2 use color_neutrum
				 	if lookSingularWords[currentWord]['indefinite_article'] == '2':				 		
						# replace with neutrum color
						afterLastDashList[i - 1] = helper.checkIfTranslatedExists(typeDict=colorSingularWords, word=previousWord, key='neutrum')																												
						
					else:
						afterLastDashList[i - 1] = helper.checkIfTranslatedExists(typeDict=colorSingularWords, word=previousWord, key='local')						

				# If previousWord exists as adjective
				if previousWord in adjectives.keys():
					afterLastDashList[i - 1] = helper.checkIfTranslatedExists(typeDict=adjectives, word=previousWord, key='singular')					
			i += 1

		# Converting [afterLastDash] to a String								
		afterLastDashString = ' '.join([str(elem) for elem in afterLastDashList])				

		return afterLastDashString
	
	# PLURAL LOOK WORDS: (Plural Mofif words / Green Leafs, Yellow Owls)
	def productPluralMotifAndColor(self, afterLastDash, country):		
		select = Select(country)
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
		
		# Convert afterLastDash into a List
		afterLastDashList = afterLastDash.split()

		# Loops trough every word afterLastDashList
		i = 0
		for currentWord in afterLastDashList:
			previousWord = afterLastDashList[i - 1]

			# If currentword exists in lookPluralWords					
			if currentWord in lookPluralWords:
				# Replace word in afterLastDash at current index
				afterLastDashList[i] = helper.checkIfTranslatedExists(typeDict=lookPluralWords, word=currentWord)
						
				# If previousWord exists in colorPluralWords. 						
				if previousWord in colorPluralWords.keys():
					# Replace with plural color
					afterLastDashList[i - 1] = helper.checkIfTranslatedExists(typeDict=colorPluralWords, word=previousWord)

				# If previousWord exists as adjective
				if previousWord in adjectives.keys():
					afterLastDashList[i - 1] = helper.checkIfTranslatedExists(typeDict=adjectives, word=previousWord)

			i += 1
		
		# Converting [afterLastDash] to a String								
		afterLastDashString = ' '.join([str(elem) for elem in afterLastDashList])
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
		helper = Helper()
		select = Select(country)
		prepositions = select.prepositions()		

		# Convert afterLastDash into a List
		afterLastDashList = afterLastDash.split()

		# Loops trough every word afterLastDashList
		i = 0
		for currentWord in afterLastDashList:
			# If currentWord exists as a dict.key
			if currentWord in prepositions.keys():
				afterLastDashList[i] = helper.checkIfTranslatedExists(typeDict=prepositions, word=currentWord)
			i += 1
		
		# Converting [afterLastDash] to a String				
		afterLastDashString = ' '.join([str(elem) for elem in afterLastDashList])
		return afterLastDashString



