# coding=utf-8
import sys
# Fixing can't encode unichar issue
reload(sys)
sys.setdefaultencoding('utf8')

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


	# Replace Colors (Where afterLastDash only exists of colors, and not motif)
	def productNameLongColor(self, afterLastDash, country):
		select = Select(country)
		colors = select.colorWords()
		colorLong = colors[1]
		helper = Helper()
		issue = Issue()
		
		# Convert AfterLastDash from List to String, with space between elements
		afterLastDashString = str('')
		for ele in afterLastDash:		
			afterLastDashString += str(ele) + ''

		# Loop through colorLong.keys()
		for key in colorLong:
			# afterLastDashString exists as key 
			if afterLastDashString.find(key) == 0:				
				afterLastDashString = afterLastDashString.replace(key, colorLong[key])

				print(afterLastDashString)

		# return
		return afterLastDashString