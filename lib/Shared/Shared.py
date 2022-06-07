from lib.Helper import Helper
from db.Select import Select
from lib.Issue import Issue

"""
Translated Product Types: Shared Methods
"""

class Shared:
	# Translated Single Colors (Incl. slashes ) in afterLastDash
	def productNameSingleColor(self, afterLastDash, country):				
		select = Select(country)
		colors = select.colors()
		colorSingle = colors[0]
		# helper = Helper()
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
				issue.criticalErrorMsg(''.join(afterLastDash) + ' ' + country + ' Missing Translated Version')							
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
						issue.criticalErrorMsg(''.join(afterLastDash) + ' ' + country + ' Missing Translated Version')	

		# If and in afterLastDash
		if ' and ' in afterLastDashString:
			# Split afterLastDashToString with /
			afterLastDashSplit = afterLastDashString.split(' and ')
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
						issue.criticalErrorMsg(''.join(afterLastDash) + ' ' + country + ' Missing Translated Version')	

		# Translate Single Words				
		# If afterLastDash contains a single word And exists as a color keys		
		if len(afterLastDash) == 1 and ''.join(afterLastDash) in colorSingle.keys():			
			# If there is a translated version.
			if colorSingle[''.join(afterLastDash)]['local']:						
				# Replace first index, with translated color					
				afterLastDash[0] = colorSingle[''.join(afterLastDash)]['local']
			
			# Else give a error message (If translated color missing)
			else:
				issue.criticalErrorMsg(''.join(afterLastDash) + ' ' + country + ' Missing Translated Version')

			# Converting [afterLastDash] to a proper String				
			afterLastDashString = ''.join([str(elem) for elem in afterLastDash])			
		
		# Return		
		return afterLastDashString

	# Getting Single Colors like "black stripe"
	def singleColorCatchAll(self, afterLastDash, country):
		select = Select(country)
		colors = select.colors()
		colorSingle = colors[0]
		issue = Issue()

		# Convert to string to list
		afterLastDashList = list(afterLastDash.split(" "))
		
		i = 0
		for word in afterLastDashList:			
			if word in colorSingle.keys():
				# If translated version exists
				if colorSingle[word]['local']:
					afterLastDashList[i] = str(colorSingle[word]['local'])
				else:
					issue.criticalErrorMsg('Color: ' + word + ' in ' + country + ' Missing Translated Version')
		
			i += 1
		# Converting [afterLastDash] to a proper String				
		afterLastDashString = ' '.join([str(elem) for elem in afterLastDashList])

		return afterLastDashString

	# Replace Colors (Where afterLastDash only exists of colors, and not motif)
	def productNameLongColor(self, afterLastDash, country):
		select = Select(country)
		colors = select.colorWords()
		colorLong = colors[1]
		# helper = Helper()
		# issue = Issue()
		
		# Convert AfterLastDash from List to String, with space between elements
		afterLastDashString = str('')
		for ele in afterLastDash:		
			afterLastDashString += str(ele) + ''

		# Loop through colorLong.keys()
		for key in colorLong:
			# afterLastDashString exists as key 
			if afterLastDashString.find(key) == 0:				
				afterLastDashString = afterLastDashString.replace(key, colorLong[key])

				# print(afterLastDashString)

		# return
		return afterLastDashString
	
	# SINGULAR LOOK WORDS: (Single Mofif word / Green Leaf, Yellow Owl)
	def productNameSingularMotif(self, afterLastDash, country):
		select = Select(country)
		helper = Helper()
		
		# Looks
		lookWords = select.lookWords()
		lookSingularWords = lookWords[0]
		
		# Colors
		colors = select.colors()
		colorSingularWords = colors[0]

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
		colors = select.colors()		
		colorPlurals = colors[1]
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
				if previousWord in colorPlurals.keys():
					# Replace with plural color
					afterLastDashList[i - 1] = helper.checkIfTranslatedExists(typeDict=colorPlurals, word=previousWord)

				# If previousWord exists as adjective
				if previousWord in adjectives.keys():
					afterLastDashList[i - 1] = helper.checkIfTranslatedExists(typeDict=adjectives, word=previousWord)

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
