# Translation
from lib.Translate.CoverCase.CoverCaseBeforeLastDash import CoverCaseBeforeLastDash
from lib.Translate.CoverCase.CoverCaseAfterLastDash import CoverCaseAfterLastDash
from lib.Translate.Screenprotector.Screenprotector import Screenprotector
from lib.Translate.Watchstrap.Watchstrap import Watchstrap

class Translate:
	def __init__(self, country:str, products:dict):		
		self.country = country		
		self.products = products

	# ProductType: Covers And Cases - Translate Words BEFORE Last Dash
	def getCoverCaseBeforeLastDash(self, products:dict) -> dict:
		translateBeforeLastDash = CoverCaseBeforeLastDash()		
		for product in products:			
			if products[product]['productType'] == 'cover' or products[product]['productType'] == 'case':							
				products[product]['name'] = translateBeforeLastDash.make(productName=products[product]['name'], country=self.country, product=products[product])
		
		# Return
		return products
	
	# ProductType: Covers And Cases - Translate Words AFTER Last Dash
	def getCoverCaseAfterLastDash(self, products:dict) -> dict:
		translateAfterLastDash = CoverCaseAfterLastDash()		

		for product in products:			
			if products[product]['productType'] == 'cover' or products[product]['productType'] == 'case':
				products[product]['name'] = translateAfterLastDash.make(productName=products[product]['name'], country=self.country)
		# Return
		return products

	# ProductType: Screen Protectors - Translate Screen Protectos
	def screenProtectorName(self, products:dict) -> dict:
		translateScreenProtector = Screenprotector()

		for product in products:
			if products[product]['productType'] == 'screenprotector':
				products[product]['name'] = translateScreenProtector.make(productName=products[product]['name'], country=self.country, product=products[product])

		return products

	# ProductType: Watchstraps
	def watchstrapName(self, products:dict) -> dict:
		watchstrap = Watchstrap()

		for product in products:									
			if products[product]['productType'] == 'watchstrap':
				products[product]['name'] = watchstrap.translateName(productName=products[product]['name'], country=self.country, product=products[product])

		return products