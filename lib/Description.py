# Adding Template Description
from db.Select import Select

class Description:
	def __init__(self, country, products):
		self.country = country
		self.products = products

	def productTemplate(self):
		# Check if first two words matches any in DB
		products = self.products
		select = Select(self.country)
		product2021Templates = select.product2021Templates()
		product2020Templates = select.product2020Templates()		

		# Loop trough products
		for product in products:
			# If product has a template attribute
			if products[product]['template'] != '':
				# Find correct template value, from productTemplates[key]. Searching for 
				template = product2020Templates.get(products[product]['template']) or product2021Templates.get(products[product]['template'])
				# Replace [DEVICE NAME] with Product Device name in template
				template = template.replace('[DEVICE NAME]', products[product]['manName'] + ' ' + products[product]['devName'])
				# Assign correct template description
				products[product]['description'] = template

	# Return final dict
	def done(self):
		products = self.products
		return products