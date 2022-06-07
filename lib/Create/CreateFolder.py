import os

class CreateFolder:
	def __init__(self, week:str):		
		self.week = week

	def folder(self) -> None:
		path = os.getcwd() + '/import/' + self.week
		if not os.path.exists(path):		
			os.makedirs(path)