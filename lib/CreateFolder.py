import os

class CreateFolder:
	def __init__(self, weekInput, countryInput):
		self.countryInput = countryInput
		self.weekInput = weekInput

	def folder(self):		
		# Create /import/Week/Country/ Folder				
		path = os.getcwd() + '/import/' + self.weekInput + '/' + self.countryInput + '/'
		if not os.path.exists(path):		
			os.makedirs(path)	