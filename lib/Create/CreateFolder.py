import os

class CreateFolder:
	def __init__(self, weekInput:str, countryInput:str):
		self.countryInput = countryInput
		self.weekInput = weekInput

	def folder(self) -> None:		
		# Create /import/Week/Country/ Folder				
		path = os.getcwd() + '/import/' + self.weekInput + '/' + self.countryInput + '/'
		if not os.path.exists(path):		
			os.makedirs(path)	