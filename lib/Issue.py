class Issue:
	def __init__(self, products:dict = None, country:str = None):		
		self.products = products
		self.country = country

	def checkForEmptyManAndDevName(self) -> None:
		products = self.products
		skus = []
		# Loop Through produts
		for product in products:
			if len(products[product]['device']['manName']) == 0 or len(products[product]['device']['devName']) == 0:
				skus.append(products[product]['sku'])
				# Error Message
				# self.warningErrorMsg(products[product]['sku'] + ' is missing manName or devName. Update the device list or the product fits multiple products.')
		
		textfile = open("log/errors/missingManDevName.txt", "w")
		for sku in skus:
			textfile.write(sku + "\n")
		textfile.close()


	def doubleSpace(self) -> None:
		products = self.products
		skus = []

		for product in products:
			if '  ' in products[product]['description']:
				skus.append(products[product]['sku'])
				# self.criticalErrorMsg(products[product]['sku'] + ' Has a double spaces in description. Fix it manual with device name')	

		textfile = open("log/errors/doubleDash.txt", "w")
		for sku in skus:
			textfile.write(sku + "\n")
		textfile.close()


	# User Messages
	def warningErrorMsg(self, msg):
		print('\x1b[1;30;43m' + msg + '\x1b[0m')	

	def criticalErrorMsg(self, msg):
		print('\x1b[3;37;41m' + msg + '\x1b[0m')