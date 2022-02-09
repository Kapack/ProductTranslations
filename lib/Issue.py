class Issue:
	def __init__(self, products = None):		
		self.products = products

	def checkForEmptyManAndDevName(self):
		products = self.products
		
		# Loop Through produts
		for product in products:
			if len(products[product]['device']['manName']) == 0 or len(products[product]['device']['devName']) == 0:
				# Error Message
				self.warningErrorMsg(products[product]['sku'] + ' is missing manName or devName. Update the device list or the product fits multiple products.')

	def doubleSpace(self):
		products = self.products
		for product in products:
			if '  ' in products[product]['description']:
				self.criticalErrorMsg(products[product]['sku'] + ' Has a double spaces in description. Fix it manual with device name')	

	# User Messages
	def warningErrorMsg(self, msg):
		print('\x1b[1;30;43m' + msg + '\x1b[0m')	

	def criticalErrorMsg(self, msg):
		print('\x1b[3;37;41m' + msg + '\x1b[0m')