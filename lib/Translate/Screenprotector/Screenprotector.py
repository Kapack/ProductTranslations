from lib.Helper import Helper
from db.Select import Select
from itertools import permutations
from lib.Issue import Issue

"""
Translated Product Types: Screenprotectors
"""

class Screenprotector:
	def make(self, productName, country):		
		# Go Trough Translations methods		
		productName = self.prepositions(productName, country)
		productName = self.productNameType(productName, country)
		
		# Return new name		
		return productName

	# Replaces / Translate Prepositions (with, in, and, for)
	def prepositions(self, productName, country):
		select = Select(country)		
		helper = Helper()
		prepositions = select.prepositions()

		# Check if prepositionsKey is in name, and replace
		productName = helper.dictKeyInString(prepositions, productName)

		return productName

	# Replace productType / tempered glass, etc.
	def productNameType(self, productName, country):		
		select = Select(country)
		productTypes = select.productTypes()
		issue = Issue()
				
		# Each permutation of name
		for permutation in permutations(productName.lower().split(' '), 2):			
			# # Let permutation be string
			permutation = str(' '.join(permutation))					
			# If Permutation exist as a productType key, and translated version exists
			if permutation in productTypes.keys() and productTypes[permutation] != '':
				# Replace permuation in name with productTypes[value] 																								
				productName = productName.lower().replace(permutation, productTypes[permutation])

			## ERROR MSG
			# If permutation exists but translated version is empty
			if permutation in productTypes.keys() and productTypes[permutation] == '':
				issue.criticalErrorMsg(permutation + ' missing translated version')

		return productName