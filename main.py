#!/usr/bin/env python2.7

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

class Main:
	def __init__(self):
		userAnswer = self.userInput()
		week = userAnswer[0]
		createDatabaseMsg = userAnswer[1]		
		# If any .csv has been updated, so database will be updated
		if (createDatabaseMsg == 'y'):
			self.createDatabase(createDatabaseMsg)
		
		countries = userAnswer[2]
		
		for country in countries:					
			self.createFolders(week, country)
			products = self.getCsv(week, country)
			self.commonErrors(products)
			products = self.getAttributes(country, products)
			products = self.translateItems(country, products)
			products = self.makeDescriptions(country, products)
			products = self.corrections(country, products)
			
			self.issues(products)
			self.saveCsv(country, week, products)

		# User Success Message
		print('\x1b[0;30;42m' + 'Translations Complete' + '\x1b[0m')	

	# User Input
	def userInput(self):	
		week = raw_input("Week number?: ")
		createDatabaseMsg = raw_input("Do you want to update the database? / Has any .csv files been updated? [y/n] ").lower()
		country = raw_input("Write country abbreviation (eg. dk, se, fi, de, nl etc.) Write all for every country: ").lower()
		# week = '00'
		# createDatabaseMsg = 'n'
		# country = 'se'
		country = [country]		
		if country == ['all']:
			country = ['se', 'dk', 'no', 'fi', 'de', 'nl', 'fr']
		
		return [week, createDatabaseMsg, country]

	# Create Database
	def createDatabase(self, createDatabaseMsg):
		print('Creating database...')
		database = Database(createDatabaseMsg)
		database.createAndInsertTables()		

	# Create Folders
	def createFolders(self, week, country):
		createFolder = CreateFolder(week, country)
		createFolder.folder()

	# Get CSV Items
	def getCsv(self, week, country):
		openCsv = OpenCsv(week, country)
		# File Needs SKU, Name and Description
		products = openCsv.initFile()
		return products

	# Check for common errors, before any changes have been made
	def commonErrors(self, products):
		commonError = CommonError(products)
		commonError.dobuleDash()

	# Analyse Skus and Names. Append correct values to products = {...}
	def getAttributes(self, country, products):
		append = Append(country, products)
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
	def translateItems(self, country, products):	
		print('Translating ' + country + '...')
		translate = Translate(country, products)
		products = translate.makeCoverCaseBeforeLastDash(products)
		products = translate.makeCoverCaseAfterLastDash(products)
		products = translate.makeScreenProtector(products)
		products = translate.makeWatchstrap(products)
		return products

	# Make Description from productTemplates
	def makeDescriptions(self, country, products):
		print('Adding template descriptions...')
		products = Description(country, products)
		products = products.loopProducts()
		return products

	# Corrections
	def corrections(self, country, products):
		print('Making corrections...')
		correct = Correction(country)
		products = correct.formatName(products)
		products = correct.formatDeviceName(products)
		return products

	# Check for common issues
	def issues(self, products):
		issue = Issue(products)	
		issue.checkForEmptyManAndDevName()
		issue.doubleSpace()

	# Create CSV and Folder
	def saveCsv(self, country, week, products):
		print('Saving ' + country + ' files...')
		createCsv = CreateCsv(country, week, products)
		createCsv.saveFile()

# Calling Main
if __name__ == '__main__':
	Main()
	