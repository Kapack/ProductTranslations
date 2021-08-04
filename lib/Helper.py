# coding=utf-8
from lib.Issue import Issue

class Helper:

	def beforeAndAfterLastDash(self, productName):
		beforeLastDash = productName.split(' - ')[0]
		afterLastDash = productName.split(' - ')[-1].lower().split(' ')

		return [beforeLastDash, afterLastDash]

	def createName(self, beforeLastDash, afterLastDashString):
		productName = beforeLastDash + ' - ' + afterLastDashString

		return productName

	def dictKeyInString(self, typeDict, string):
		issue = Issue()

		# String into a list / We a splitting the list into. a string, so we replace standalone words.
		stringList = string.lower().split()		
		# New stringList / We will convert this to a string lastly
		newStringList = []

		# Loop trough the list of strings, save index and word to variable
		for (index, word) in enumerate(stringList):			
			# Saving currentWord to a variable
			currentWord = stringList[index]

			# If currentWord (Single word / Watchband) is in typeDict key
			if currentWord in typeDict.keys():

				# If translated version exists
				if typeDict[currentWord]:
					# Replace currentWord									
					currentWord = typeDict[currentWord]
				# Give error message, if translated version does not exists
				else:
					issue.warningErrorMsg(currentWord + ' Missing Translated Version')

			# Double words / CurrentWord + NextWord (Watch Band)
			# If the index number +1 is lower than the length of stringList, we can check if currentWord or currentWord + nextWord has a match
			if index + 1 < len(stringList):
				# Saving nextWord to variable
				nextWord = stringList[index + 1]				
				# If currentWord (Double words / Watch band) is in typeDict key
				if currentWord + ' ' + nextWord in typeDict.keys():
					# If translated version exists
					if typeDict[currentWord + ' ' + nextWord]:						
						# Replace
						currentWord = typeDict[currentWord + ' ' + nextWord]
						# Remove next word, so we wont append double (Urrem Band)
						stringList.remove(nextWord)

					# Give error message, if translated version does not exists
					else:
						issue.warningErrorMsg(currentWord + ' ' + nextWord + ' Missing Translated Version')								

			# Append Word (translated or english)			
			newStringList.append(currentWord)			

		# Convert list back to a string again
		newStringList = ' '.join([str(elem) for elem in newStringList])
				
		# Return list
		return newStringList

	def checkIfTranslatedExists(self, typeDict, word, key=None):
		# Check if translated version exists. 
		# If True return translated. If False return original (English)
		issue = Issue()		

		if key:
			# If translated version exists
			if typeDict[word][key]:
				# Replace Word
				word = typeDict[word][key]

			# Else Give Error Message
			else:
				issue.warningErrorMsg(key + ' : ' + word + ' Missing Translated Version')		
		else:			
			# If translated version exists
			if typeDict[word]:
				# Replace Word
				word = typeDict[word]

			# Else Give Error Message
			else:
				issue.warningErrorMsg(word + ' Missing Translated Version')

		# Return Word
		return word

