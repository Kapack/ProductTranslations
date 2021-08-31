# coding=utf-8
import sys
# Fixing can't encode unichar issue
reload(sys)
sys.setdefaultencoding('utf8')

from lib.Helper import Helper
from db.Select import Select
from lib.Translate.Shared.Shared import Shared

"""
Translated Product Types: Watchstraps
"""

class Watchstrap:
	def make(self, productName, country, product):		
		helper = Helper()
		# Break up name
		beforeAndAfterLastDash = helper.beforeAndAfterLastDash(productName)
		beforeLastDash = beforeAndAfterLastDash[0]
		afterLastDash = beforeAndAfterLastDash[1]		

		# Go Trough Translations methods
		beforeLastDash = self.feature(beforeLastDash, country, product)
		beforeLastDash = self.prepositions(beforeLastDash, country, product)
		beforeLastDash = self.material(beforeLastDash, country, product)
		beforeLastDash = self.productNameType(beforeLastDash, country, product)
		afterLastDash = self.productNameColor(afterLastDash, country)

		afterLastDash = self.size(afterLastDash, country, product)
		
		# Create new name
		# Converting [afterLastDash] to a String				
		afterLastDashString = ''.join([str(elem) for elem in afterLastDash])		
		productName = helper.createName(beforeLastDash, afterLastDashString)
				
		# Return productname
		return productName


	# Product Feature
	def feature(self, beforeLastDash, country, product):
		helper = Helper()
		select = Select(country)
		productFeatures = select.productFeatures()

		# if feature exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(productFeatures, beforeLastDash, product)

		return beforeLastDash

	def prepositions(self, beforeLastDash, country, product):
		helper = Helper()
		select = Select(country)
		prepositions = select.prepositions()

		# if prepositions exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(prepositions, beforeLastDash, product)

		return beforeLastDash


	# Product Material
	def material(self, beforeLastDash, country, product):
		helper = Helper()
		select = Select(country)		
		productMaterials = select.productMaterials()				

		# if material exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(productMaterials, beforeLastDash, product)

		return beforeLastDash
	

	# Replace productType / watchstrap etc.
	def productNameType(self, beforeLastDash, country, product):		
		helper = Helper()
		select = Select(country)
		productTypes = select.productTypes()
		# if productType exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(productTypes, beforeLastDash, product)
		# Return
		return beforeLastDash

	# Replace Colors (Where afterLastDash only exists of colors, and not motif)
	# Translated Single Colors (Incl. slashes ) in afterLastDash
	def productNameColor(self, afterLastDash, country):
		shared = Shared()		
		afterLastDashString = shared.productNameSingleColor(afterLastDash, country)
		return afterLastDashString

	# Translate size in after last dash
	def size(self, afterLastDash, country, product):
		helper = Helper()
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












		
