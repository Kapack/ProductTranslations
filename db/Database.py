#!/usr/bin/python
# -*- coding: utf_8 -*-
import sqlite3
import os
import csv

class Database:
	def __init__(self, createDatabaseMsg = None):
		print createDatabaseMsg		
		global conn
		global c
		# Delete Database, so we are fully updated
		os.remove('products.db')
		# Create new Database
		conn = sqlite3.connect('products.db')
		conn.text_factory = str
		c = conn.cursor()

	def createAndInsertTables(self):
		self.createDeviceList()
		self.insertDeviceList()
		# self.createColorsTable()
		# self.insertColors()
		self.createProductTypesTable()
		self.insertProductTypes()	
		self.createLookWordsTable()
		self.insertLookWords()
		self.createColorWordsTable()
		self.insertColorWords()
		self.createPrepositionsTable()
		self.insertPrepositions()
		self.createAdjectivesTable()
		self.insertAdjectives()
		self.createVerbsTable()
		self.insertVerbs()
		self.createtMaterialsTable()
		self.insertMaterialsTable()
		self.createFeaturesTable()
		self.insertFeaturesTable()
		self.createProduct2020TemplatesTable()
		self.insertProduct2020Templates()
		self.createProduct2021TemplatesTable()
		self.insertProduct2021Templates()

	# Devices and model / https://docs.google.com/spreadsheets/d/1T1ESFt-b1Bs6Y3929xhpUPJsYo0LriLfydwoOm6fXpM/edit#gid=0
	def createDeviceList(self):
		sql = 'CREATE TABLE if not exists deviceList (id integer primary key not null, manName text, manSku text, devSku text, devName text)'
		c.execute(sql)

	def insertDeviceList(self):
		# Open Correct csv
		with open(os.getcwd() + '/db/csv/deviceList.csv', 'r') as file:
			reader = csv.DictReader(file, delimiter=';')
			# Loop trough .csv and insert every row to corresponding column
			i = 1
			for row in reader:
				c.execute('INSERT INTO deviceList VALUES(?, ?, ?, ?, ?)', (i, str(row['ManName']), str(row['ManSKU']), str(row['DevSKU']), str(row['DevName']) ))
				i += 1
				conn.commit()

	# # Create Colors Table
	# def createColorsTable(self):	
	# 	sql = 'CREATE TABLE if not exists colors (id integer primary key not null, color text, se text, dk text, no text, fi text, de text, nl text)'
	# 	c.execute(sql)

	# # Insert Colors into table
	# def insertColors(self):
	# 	# Open csv
	# 	with open(os.getcwd() + '/db/csv/colors.csv', 'r') as file:
	# 		reader = csv.DictReader(file, delimiter=';')		
	# 		# Loop trough CSV and insert
	# 		i = 1
	# 		for row in reader:			
	# 			c.execute('INSERT INTO colors VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (i, str(row['color']).lower(), str(row['se']), str(row['dk']), str(row['no']), str(row['fi']), str(row['de']), str(row['nl'])) )
	# 			i += 1
	# 			conn.commit()

	def createProductTypesTable(self):
		sql = 'CREATE TABLE if not exists productTypes (id integer primary key not null, type text, se text, dk text, no text, fi text, de text, nl text)'
		c.execute(sql)

	def insertProductTypes(self):
		with open(os.getcwd() + '/db/csv/productTypes.csv', 'r') as file: 
			reader = csv.DictReader(file, delimiter=';')
			i = 1
			for row in reader:			
				c.execute('INSERT INTO productTypes VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (i, str(row['type']).lower(), str(row['se']), str(row['dk']), str(row['no']), str(row['fi']), str(row['de']), str(row['nl'])) )
				i += 1
				conn.commit()

	# Look Words
	def createLookWordsTable(self):
		sql = 'CREATE TABLE if not exists lookWords (id integer primary key not null, singular text, plural text, se_indefinite_article text, se_singular text, se_plural text, dk_indefinite_article text, dk_singular text, dk_plural text, no_indefinite_article text, no_singular text, no_plural text, fi_indefinite_article text, fi_singular text, fi_plural text, de_indefinite_article text, de_singular text, de_plural text, nl_indefinite_article text, nl_singular text, nl_plural text)'
		c.execute(sql)

	def insertLookWords(self):
		with open(os.getcwd() + '/db/csv/lookWords.csv', 'r') as file: 
			reader = csv.DictReader(file, delimiter=';')
			i = 1		
			for row in reader:						
				c.execute('INSERT INTO lookWords VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (i, str(row['singular']).lower(), str(row['plural']).lower(), str(row['se_indefinite_article']), str(row['se_singular']), str(row['se_plural']), str(row['dk_indefinite_article']), str(row['dk_singular']), str(row['dk_plural']), str(row['no_indefinite_article']), str(row['no_singular']), str(row['no_plural']), str(row['fi_indefinite_article']), str(row['fi_singular']), str(row['fi_plural']), str(row['de_indefinite_article']), str(row['de_singular']), str(row['de_plural']), str(row['nl_indefinite_article']), str(row['nl_singular']), str(row['nl_plural']) ) )
				i += 1
				conn.commit()

	# Color Words
	def createColorWordsTable(self):	
		sql = 'CREATE TABLE if not exists colorWords (id integer primary key not null, color text, se_singular text, se_plural text, se_neutrum text, dk_singular text, dk_plural text, dk_neutrum text, no_singular text, no_plural text, no_neutrum text, fi_singular text, fi_plural text, fi_neutrum text, de_singular text, de_plural text, de_neutrum text)'
		c.execute(sql)

	def insertColorWords(self):
		with open(os.getcwd() + '/db/csv/colorWords.csv', 'r') as file: 
			reader = csv.DictReader(file, delimiter=';')
			i = 1		
			for row in reader:									
				c.execute('INSERT INTO colorWords VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ( i, str(row['color']).lower(), str(row['se_singular']).lower(), str(row['se_plural']).lower(), str(row['se_neutrum']).lower(), str(row['dk_singular']).lower(), str(row['dk_plural']).lower(), str(row['dk_neutrum']).lower(), str(row['no_singular']).lower(), str(row['no_plural']).lower(), str(row['no_neutrum']).lower(), str(row['fi_singular']).lower(), str(row['fi_plural']).lower(), str(row['fi_neutrum']).lower(), str(row['de_singular']).lower(), str(row['de_plural']).lower(), str(row['de_neutrum']).lower() ))
				i += 1
				conn.commit()

	# Prepositions
	def createPrepositionsTable(self):
		sql = 'CREATE TABLE if not exists prepositions (id integer primary key not null, preposition text, se text, dk text, no text, fi text, de text)'
		c.execute(sql)

	def insertPrepositions(self):
		with open(os.getcwd() + '/db/csv/prepositions.csv', 'r') as file:
			reader = csv.DictReader(file, delimiter=';')
			i = 1
			for row in reader:
				c.execute('INSERT INTO prepositions VALUES(?, ?, ?, ?, ?, ?, ?)', ( i, str(row['preposition']), str(row['se']), str(row['dk']), str(row['no']), str(row['fi']), str(row['de']) ))
				i += 1
				conn.commit()
	# Adjectives
	def createAdjectivesTable(self):
		sql = 'CREATE TABLE if not exists adjectives (id integer primary key not null, adjective text, se_singular text, se_plural text, dk_singular text, dk_plural text, no_singular text, no_plural text, fi_singular text, fi_plural text, de_singular text, de_plural text, nl_singular text, nl_plural text, fr_singular text, fr_plural text)'
		c.execute(sql)

	def insertAdjectives(self):
		with open(os.getcwd() + '/db/csv/adjectives.csv', 'r') as file:
			reader = csv.DictReader(file, delimiter=';')
			i = 1
			for row in reader:		
				c.execute('INSERT INTO adjectives VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ( i, str(row['adjective']), str(row['se_singular']), str(row['se_plural']), str(row['dk_singular']), str(row['dk_plural']), str(row['no_singular']), str(row['no_plural']), str(row['fi_singular']), str(row['fi_plural']), str(row['de_singular']), str(row['de_plural']), str(row['nl_singular']), str(row['nl_plural']), str(row['fr_singular']), str(row['fi_plural']) ))
				i += 1
				conn.commit()
	# Verbs
	def createVerbsTable(self):
		sql = 'CREATE TABLE verbs (id integer primary key not null, verb text, se text, dk text, no text, fi text, de text, nl text, fr text)'
		c.execute(sql)

	def insertVerbs(self):
		with open(os.getcwd() + '/db/csv/verbs.csv', 'r') as file:
			reader = csv.DictReader(file, delimiter=';')
			i = 1
			for row in reader:		
				c.execute('INSERT INTO verbs VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', ( i, str(row['verb']), str(row['se']), str(row['dk']), str(row['no']), str(row['fi']), str(row['de']), str(row['nl']), str(row['fr']) ))
				i += 1
				conn.commit()

	# Materials
	def createtMaterialsTable(self):
		sql = 'CREATE TABLE materials (id integer primary key not null, material text, se text, dk text, no text, fi text, de text, nl text, fr text)'
		c.execute(sql)

	def insertMaterialsTable(self):
		with open(os.getcwd() + '/db/csv/materials.csv', 'r') as file:
			reader = csv.DictReader(file, delimiter=';')
			i = 1
			for row in reader:		
				c.execute('INSERT INTO materials VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', ( i, str(row['material']), str(row['se']), str(row['dk']), str(row['no']), str(row['fi']), str(row['de']), str(row['nl']), str(row['fr']) ))
				i += 1
				conn.commit()

	# Product Features
	def createFeaturesTable(self):
		sql = 'CREATE TABLE features (id integer primary key not null, feature text, se text, dk text, no text, fi text, de text, nl text, fr text)'
		c.execute(sql)

	def insertFeaturesTable(self):
		with open(os.getcwd() + '/db/csv/features.csv', 'r') as file:
			reader = csv.DictReader(file, delimiter=';')
			i = 1
			for row in reader:
				c.execute('INSERT INTO features VALUES(?,?,?,?,?,?,?,?,?)', (i, str(row['feature']), str(row['se']), str(row['dk']), str(row['no']), str(row['fi']), str(row['de']), str(row['nl']), str(row['fr']) ))
				i += 1
				conn.commit()

	# Product 2020 Templates
	def createProduct2020TemplatesTable(self):
		sql = 'CREATE TABLE if not exists product2020Templates (id integer primary key not null, template text, eng text, dk text, se text, no text, fi text, nl text, de text, fr text)'
		c.execute(sql)

	def insertProduct2020Templates(self):
		with open(os.getcwd() + '/db/csv/productTemplates/product2020Templates.csv', 'r') as file: 
			reader = csv.DictReader(file, delimiter=';')		
			i = 1
			for row in reader:								
				c.execute('INSERT INTO product2020Templates VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (i, str(row['template']).lower(), str(row['eng']), str(row['dk']), str(row['se']), str(row['no']), str(row['fi']), str(row['nl']), str(row['de']), str(row['fr']) ))
				i += 1
				conn.commit()

	# Product 2021 Templates
	def createProduct2021TemplatesTable(self):
		sql = 'CREATE TABLE if not exists product2021Templates (id integer primary key not null, template text, eng text, dk text, se text, no text, fi text, nl text, de text, fr text)'
		c.execute(sql)

	def insertProduct2021Templates(self):
		with open(os.getcwd() + '/db/csv/productTemplates/product2021Templates.csv', 'r') as file: 
			reader = csv.DictReader(file, delimiter=';')		
			i = 1
			for row in reader:								
				c.execute('INSERT INTO product2021Templates VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (i, str(row['template']).lower(), str(row['eng']), str(row['dk']), str(row['se']), str(row['no']), str(row['fi']), str(row['nl']), str(row['de']), str(row['fr'])) )
				i += 1
				conn.commit()

	# Close Connection to DB / Kept for notes
	# def closeConnection(self):
		# c.close()
		# conn.close()