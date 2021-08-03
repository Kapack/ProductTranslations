# coding=utf-8
import sys

# Fixing can't encode unichar issue
reload(sys)
sys.setdefaultencoding('utf8')

from db.Select import Select
from lib.Helper import Helper
from lib.Issue import Issue

"""
Translates all words AFTER last dash (Motifs, colors etc.)
"""

class TranslateAfterLastDash:
	def make(self, productName, productType, country):
		helper = Helper()
		# Break up name
		beforeAndAfterLastDash = helper.beforeAndAfterLastDash(productName)
		beforeLastDash = beforeAndAfterLastDash[0]
		afterLastDash = beforeAndAfterLastDash[1]

		# Go Trough Translations methods
		if productType == 'cover' or productType == 'case' or products[i]['productType'] == 'watchstrap':
			afterLastDash = self.productNameColor(afterLastDash, country)

		if productType == 'cover' or productType == 'case':			
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
		select = Select(country)
		colors = select.colorWords()
		colorSingle = colors[0]
		helper = Helper()
		issue = Issue()				

		# Convert AfterLastDash from List to String, with space between elements
		afterLastDashString = str('')
		for ele in afterLastDash:			
			afterLastDashString += ele + ' '		

		# If words has a space, and exists as a key in colorSingle
		# Mistakes happens: Sometimes the product name has a "invisible" space at the end
		if len(afterLastDash) > 1 and ' '.join(afterLastDash) in colorSingle.keys():
			# If translated version exists
			if colorSingle[' '.join(afterLastDash)]['local']:
				afterLastDash = colorSingle[' '.join(afterLastDash)]['local']
			# Else give a error message (If transled color missing)
			else:
				issue.criticalErrorMsg(''.join(afterLastDash) + ' Missing Translated Version')				
			# Converting [afterLastDash] to a proper String				
			afterLastDashString = ''.join([str(elem) for elem in afterLastDash])

		# If afterLastDash is separated with spaces
		if '/' in afterLastDashString:					
			# Split afterLastDashToString with /
			afterLastDashSplit = afterLastDashString.split('/')
			for string in afterLastDashSplit:				
				# Strip away spaces around the word
				string = string.strip()
				# If string exists as a key
				if string in colorSingle.keys():
					# If translated version exist
					if colorSingle[string]['local']:								
						# Replace current index with translated word
						afterLastDashString = afterLastDashString.replace(string, colorSingle[string]['local'])
					# Else give a error message (If transled color missing)
					else:
						issue.criticalErrorMsg(''.join(afterLastDash) + ' Missing Translated Version')	

		# # Translate Single Words				
		# # If afterLastDash contains a single word And exists as a color keys
		if len(afterLastDash) == 1 and ''.join(afterLastDash) in colorSingle.keys():													
			# If there is a translated version.
			if colorSingle[''.join(afterLastDash)]['local']:						
				# Replace first index, with translated color					
				afterLastDash[0] = colorSingle[''.join(afterLastDash)]['local']
			# Else give a error message (If translated color missing)
			else:
				issue.criticalErrorMsg(''.join(afterLastDash) + ' Missing Translated Version')

			# Converting [afterLastDash] to a proper String				
			afterLastDashString = ''.join([str(elem) for elem in afterLastDash])

		# Return
		return afterLastDashString

	# SINGULAR LOOK WORDS: (Single Mofif words / Green Leaf, Yellow Owl)
	def productSingularMotifAndColor(self, afterLastDash, country):
		select = Select(country)
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
		
		# Convert afterLastDash into a List
		afterLastDashList = afterLastDash.split()
		# Loops trough every word afterLastDashList
		i = 0
		for currentWord in afterLastDashList:
			previousWord = afterLastDashList[i - 1]

			# If currentword exists in lookSingularWords					
			if currentWord in lookSingularWords.keys():
				# Replace word in afterLastDash at current index						
				afterLastDashList[i] = lookSingularWords[currentWord]['local']
				
				# Check if previousWord is a color and there is a translated version						
				if previousWord in colorSingularWords.keys() and colorSingularWords[previousWord]:					
					# Get the indefinite_article of current word, is it 2 use color_neutrum
				 	if lookSingularWords[currentWord]['indefinite_article'] == '2':				 		
						# replace with neutrum color																													
						afterLastDashList[i - 1] = colorSingularWords[previousWord]['neutrum']
					else:
						afterLastDashList[i - 1] = colorSingularWords[previousWord]['local']

				# If previousWord exists as adjective
				if previousWord in adjectives.keys():
					afterLastDashList[i - 1] = adjectives[previousWord]['singular']		
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
				afterLastDashList[i] = lookPluralWords[currentWord]
						
				# If previousWord exists in colorPluralWords. 						
				if previousWord in colorPluralWords.keys():
					# Replace with plural color
					afterLastDashList[i - 1] = colorPluralWords[previousWord]

				# If previousWord exists as adjective
				if previousWord in adjectives.keys():							
					afterLastDashList[i - 1] = adjectives[previousWord]

			i += 1
		
		# Converting [afterLastDash] to a String								
		afterLastDashString = ' '.join([str(elem) for elem in afterLastDashList])
		return afterLastDashString

	# Replacing / Translating Verbs (holding, wearing)
	def productVerbs(self, afterLastDash, country):
		select = Select(country)
		verbs = select.verbs()		

		# Convert afterLastDash into a List
		afterLastDashList = afterLastDash.split()

		# Loops trough every word afterLastDashList
		i = 0
		for currentWord in afterLastDashList:
			# if currentWord exists as verb and there is a translated version
			if currentWord in verbs.keys() and verbs[currentWord]:
				# replace currentWord with translated verb
				afterLastDashList[i] = verbs[currentWord]	

			i += 1
		
		# Converting [afterLastDash] to a String				
		afterLastDashString = ' '.join([str(elem) for elem in afterLastDashList])
		return afterLastDashString

	# Replacing / Translate Prepositions (with, in, and, for)
	def productPrepositions(self, afterLastDash, country):
		select = Select(country)
		prepositions = select.prepositions()
		helper = Helper()

		# Convert afterLastDash into a List
		afterLastDashList = afterLastDash.split()

		# Loops trough every word afterLastDashList
		i = 0
		for currentWord in afterLastDashList:
			# If currentWord exists as a dict.key and has a translated version
			if currentWord in prepositions.keys() and prepositions[currentWord]:
				afterLastDashList[i] = prepositions[currentWord]
			i += 1
		
		# Converting [afterLastDash] to a String				
		afterLastDashString = ' '.join([str(elem) for elem in afterLastDashList])
		return afterLastDashString













