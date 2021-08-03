class Issue:
	def __init__(self, products = None):		
		self.products = products

	def checkForEmptyManAndDevName(self):
		products = self.products
		
		# Loop Through produts
		for product in products:
			if len(products[product]['manName']) == 0 or len(products[product]['devName']) == 0:
				# Error Message
				self.criticalErrorMsg(products[product]['sku'] + ' is missing manName or devName. You need to update the device list.')

	# User Messages
	def criticalErrorMsg(self, msg):
		print('\x1b[3;37;41m' + msg + '\x1b[0m')		