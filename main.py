#!/usr/bin/env python3

# DO NOT CHANGE ANY FILE NAMES!

# This program translate the columns in import.csv - The columns HAS to be names sku, name and description
# The program can only translate from English to given language.
# All files in ~/csv folder is inserted into a sqlite databaase
# The descriptions are made from templates (~/csv/productXXXXTemplates.csv)
# The Names are translated with single word and sentences. In the name before and after Last dash has a important significance
# The program will loop through color, object (motif), material etc. if it finds a match, it will replace otherwise the original word will be used.
# If an english has been found, but no translated version, you will get an error message in shell.

# The translated files are found in the ~/import folder

from db.Database import Database
from lib.Create.CreateFolder import CreateFolder
from lib.Opencsv import OpenCsv
from lib.CommonError import CommonError
from lib.Create.CreateCsv import CreateCsv
from lib.Append import Append
from lib.Translate.Translate import Translate
from lib.Translate.Description.Description import Description
from lib.Issue import Issue
from lib.Correction import Correction
from common.Constants import BGCOLORS

class Main:
	def __init__(self):
		userAnswer = self.userInput()
		week = userAnswer[0]
		createDatabaseMsg = userAnswer[1]	
		countries = userAnswer[2]
		# If any .csv has been updated, so database will be updated
		if (createDatabaseMsg == 'y'):
			self.createDatabase(createDatabaseMsg)
		
		self.initFolders(week=week)
		for country in countries:											
			products = self.getCsv(week = week, country = country)
			self.commonErrors(products = products)
			products = self.getAttributes(country = country, products = products)
			products = self.translateNames(country = country, products = products)
			products = self.makeDescriptions(country = country, products = products)
			products = self.corrections(country = country, products = products)
			self.issues(country = country, products = products)
			self.saveFiles(country = country, week = week, products = products)

		# User Success Message
		print(BGCOLORS['SUCCESS'] + 'Translations Complete' + BGCOLORS['ENDC'])	

	# User Input
	def userInput(self) -> list:	
		week = '00'
		createDatabaseMsg = 'n'
		country = ['dk']

		# week = input("Week number?: ")
		# createDatabaseMsg = input("Do you want to update the database? / Has any .csv files been updated? [y/n] ").lower()
		# country = input("Write country abbreviation (eg. dk, se, fi, de, nl etc.) Write all for every country: ").lower()		
		# country = [country]		

		# if country == ['all']:
		# 	country = ['se', 'dk', 'no', 'fi', 'de', 'nl']
		
		return [week, createDatabaseMsg, country]

	def createDatabase(self, createDatabaseMsg:str) -> None:
	# Create Database
		print('Creating database...')
		database = Database(createDatabaseMsg)
		database.createAndInsertTables()		
		
	# Create and delete folders/files
	def initFolders(self, week:str) -> None:
		createFolder = CreateFolder(week = week)
		issue = Issue()

		createFolder.folder()		
		issue.clearLogFile()

	# Get CSV Items
	def getCsv(self, week:str, country:str) -> dict:
		# openCsv = OpenCsv(week = week, country = country)
		openCsv = OpenCsv(week = week, country = country)
		# File Needs SKU, Name and Description
		products = openCsv.initFile()
		return products

	# Check for common errors, before any changes have been made
	def commonErrors(self, products:dict) -> None:
		commonError = CommonError(products = products)
		commonError.dobuleDash()

	# Analyse Skus and Names. Append correct values to products = {...}
	def getAttributes(self, country:str, products:dict) -> dict:
		append = Append(country = country, products = products)
		append.productType()
		append.deviceAndModel()		
		append.attributeColor()
		append.attributeMaterial()
		append.attributeFeature()
		append.attributeSize()
		append.product2021Template()
		products = append.product2020Template()		
		return products

	# Translate
	def translateNames(self, country:str, products:dict) -> dict:
		print('Translating ' + country + '...')
		translate = Translate(country = country, products = products)
		products = translate.getCoverCaseBeforeLastDash(products = products)
		products = translate.getCoverCaseAfterLastDash(products = products)
		products = translate.screenProtectorName(products = products)
		products = translate.watchstrapName(products = products)
		return products

	# Make Description from productTemplates
	def makeDescriptions(self, country:str, products:dict) -> dict:		
		print('Adding template descriptions...')
		products = Description(country = country, products = products)
		products = products.loopProducts()
		return products

	# Correct Common Errors
	def corrections(self, country:str, products:dict) -> dict:
		print('Making corrections...')
		correct = Correction(country = country)
		products = correct.formatName(products = products)
		products = correct.formatDeviceName(products = products)
		products = correct.descStartsWithSpace(products = products)				
		products = correct.currentAndNextInDescription(products = products)
		return products

	# Check for common issues
	def issues(self, products:dict, country:str) -> None:		
		issue = Issue(products = products, country = country)	
		issue.checkForEmptyManAndDevName()
		issue.doubleSpace()		
		issue.checkForLogFiles()

	# Create CSV and Folder
	def saveFiles(self, country:str, week:str, products:dict) -> None:		
		createCsv = CreateCsv(country = country, week = week, products = products)
		createCsv.saveCsv()
	
# Calling Main
if __name__ == '__main__':
	Main()
	