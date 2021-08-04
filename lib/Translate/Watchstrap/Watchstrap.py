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
	def make(self, productName, country):		
		helper = Helper()
		# Break up name
		beforeAndAfterLastDash = helper.beforeAndAfterLastDash(productName)
		beforeLastDash = beforeAndAfterLastDash[0]
		afterLastDash = beforeAndAfterLastDash[1]

		# Go Trough Translations methods
		beforeLastDash = self.productFeature(beforeLastDash, country)		
		beforeLastDash = self.productMaterial(beforeLastDash, country)
		beforeLastDash = self.productNameType(beforeLastDash, country)
		afterLastDash = self.productNameColor(afterLastDash, country)
		
		# Create new name
		# Converting [afterLastDash] to a String				
		afterLastDashString = ''.join([str(elem) for elem in afterLastDash])		
		productName = helper.createName(beforeLastDash, afterLastDashString)	
				
		# Return productname
		return productName


	# Product Feature
	def productFeature(self, beforeLastDash, country):
		helper = Helper()
		select = Select(country)
		productFeatures = select.productFeatures()

		# if feature exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(productFeatures, beforeLastDash)

		return beforeLastDash

	# Product Material
	def productMaterial(self, beforeLastDash, country):
		helper = Helper()
		select = Select(country)		
		productMaterials = select.productMaterials()				

		# if material exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(productMaterials, beforeLastDash)

		return beforeLastDash
	

	# Replace productType / watchstrap etc.
	def productNameType(self, beforeLastDash, country):		
		helper = Helper()
		select = Select(country)
		productTypes = select.productTypes()
		# if productType exist in beforeLastDash
		beforeLastDash = helper.dictKeyInString(productTypes, beforeLastDash)		
		# Return
		return beforeLastDash


	# Replace Colors (Where afterLastDash only exists of colors, and not motif)
	# Translated Single Colors (Incl. slashes ) in afterLastDash
	def productNameColor(self, afterLastDash, country):
		shared = Shared()		
		afterLastDashString = shared.productNameColor(afterLastDash, country)
		return afterLastDashString
