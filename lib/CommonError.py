from common.Constants import BGCOLORS

class CommonError:
	def __init__(self, products:dict):
		self.products = products

	# Check if name has two "last dashes"
	def dobuleDash(self):		
		i = 0
		for product in self.products:
			split = self.products[product]['name'].split()
			if split.count('-') >= 2:
				print(self.products[product]['name'])
				i += 1
		if i > 0:
			print(BGCOLORS['FAIL'] + 'Warning: ' + str(i) + ' products contains more than two dashes. Correct them manually in import.csv' + BGCOLORS['ENDC'])