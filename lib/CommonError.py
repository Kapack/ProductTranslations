from lib.Issue import Issue

class CommonError:
	def __init__(self, products):
		self.products = products

	# Check if name has two "last dashes"
	def dobuleDash(self):
		issue = Issue()
		i = 0
		for product in self.products:
			split = self.products[product]['name'].split()
			if split.count('-') >= 2:
				i += 1
		if i > 0:
			issue.warningErrorMsg('Warning: ' + str(i) + ' products contains more than two dashes. Correct them manually in import.csv')		
