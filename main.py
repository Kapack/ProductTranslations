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
from lib.CreateFolder import CreateFolder
from lib.Opencsv import OpenCsv
from lib.CreateCsv import CreateCsv
from lib.Append import Append
from lib.Translate.Translate import Translate
from lib.Description import Description
from lib.Issue import Issue


def main():			
	userAnswer = userInput()
	week = userAnswer[0]
	country = userAnswer[1]
	createDatabaseMsg = userAnswer[2]	
	# If any .csv has been updated, so database will be updated
	if (createDatabaseMsg == 'y'):
		createDatabase(createDatabaseMsg)
	
	createFolders(week, country)	
	products = getCsv(week, country)	
	products = getAttributes(country, products)
	products = translateItems(country, products)
	products = makeDescriptions(country, products)
	issues(products)
	saveCsv(country, week, products)

	# User Success Message
	print('\x1b[0;30;42m' + 'Translations Complete' + '\x1b[0m')	

# User Input
def userInput():	
	week = raw_input("Week number?: ")
	country = raw_input("Write country abbreviation (eg. dk, se, fi, de, nl etc.): ").lower()
	createDatabaseMsg = raw_input("Do you want to update the database? / Has any .csv files been updated? [y/n] ").lower()

	# week = '002'
	# country = 'dk'	

	return [week, country, createDatabaseMsg]

# Create Database
def createDatabase(createDatabaseMsg):
	database = Database(createDatabaseMsg)
	database.createAndInsertTables()

# Create Folders
def createFolders(week, country):
	createFolder = CreateFolder(week, country)
	createFolder.folder()

# Get CSV Items
def getCsv(week, country):
	openCsv = OpenCsv(week, country)
	# File Needs SKU, Name and Description
	products = openCsv.initFile()
	return products

# Analyse Skus and Names. Append correct Attributes
def getAttributes(country, products):
	append = Append(country, products)
	append.productType()
	append.deviceAndModel()
	append.product2021Template()
	append.product2020Template()
	products = append.done()

	return products

# Translate
def translateItems(country, products):	
	translate = Translate(country, products)
	products = translate.makeBeforeLastDash(products)	
	products = translate.makeAfterLastDash(products)

	#print products

	# if country == 'dk' or country == 'se':
	# 	translate.productPrepositions()
	# 	translate.productVerbs()
	# 	translate.productSingularMotifAndColor()
	# 	translate.productPluralMotifAndColor()
	
	# translate.productNameColor()	
	# translate.productMaterial()
	# translate.productFeature()
	# translate.productNameType()
	# products = translate.done()
	
	return products

# Make Description from productTemplates
def makeDescriptions(country, products):
	template = Description(country, products)
	template.productTemplate()
	products = template.done()
	return products

# Check for common errors
def issues(products):
	issue = Issue(products)
	issue.checkForEmptyManAndDevName()

# Create CSV and Folder
def saveCsv(week, country, products):
	createCsv = CreateCsv(country, week, products)
	createCsv.saveFile()

# Calling Main
if __name__ == '__main__':
	main()