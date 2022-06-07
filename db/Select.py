# coding=utf-8
#!/usr/bin/python
import sqlite3
from common.Logging import Log


class Select:
	def __init__(self, country):
		self.log = Log()
		self.country = country
		global conn
		global c
		conn = sqlite3.connect('products.db')
		c = conn.cursor()

	def deviceList(self):
		sql = 'SELECT manName, manSku, devSku, devName FROM deviceList'
		c.execute(sql)
		rows = c.fetchall()
	
		deviceList = {}		
		i = 0
		for key in rows:			
			deviceList[i] = {'manName' : rows[i][0], 'manSku' : rows[i][1], 'devSku' : rows[i][2], 'devName' : rows[i][3]}
			i += 1						

		return deviceList

	# Select Look Words
	def lookWords(self):
		sql = 'SELECT singular, plural,' + self.country + '_indefinite_article,' + self.country + '_singular,' + self.country + '_plural' + ' FROM looks'
		c.execute(sql)
		rows = c.fetchall()		
		lookSingularWords = { word[0].lower() : {'indefinite_article' : word[2].lower(), 'local' : word[3].lower() } for word in rows }
		lookPluralWords = { word[1].lower() : word[4].lower() for word in rows }

		return [lookSingularWords, lookPluralWords]

		# Closed connection in last funtions. 

	# Select Color Words
	def colors(self):
		sql = 'SELECT color,' + self.country + '_singular,' + self.country + '_plural,' + self.country + '_neutrum' + ' FROM colors'		
		c.execute(sql)
		rows = c.fetchall()
				
		colorSingularWords = { word[0].lower() : { 'local' : word[1].lower(), 'neutrum' : word[3].lower() } for word in rows }
		colorPluralWords = { word[0].lower() : word[2].lower() for word in rows }		
		
		return [colorSingularWords, colorPluralWords]

		# Closed connection in last funtions. 
	
	# Prepositions
	def prepositions(self):
		sql = 'SELECT preposition, ' + self.country + ' FROM prepositions'
		c.execute(sql)
		rows = c.fetchall()
		prepositions = { word[0].lower() : word[1].lower() for word in rows}
		
		return prepositions
		
	# Adjectives
	def adjectives(self):		
		sql = 'SELECT adjective,' + self.country + '_singular,' + self.country + '_plural' + ' FROM adjectives'
		c.execute(sql)
		rows = c.fetchall()

		adjectiveSingularWords = { word[0].lower() : { 'singular' : word[1].lower(), 'plural' : word[2].lower() } for word in rows }
		adjectivePluralWords = { word[0].lower() : word[2].lower() for word in rows }
						
		return [adjectiveSingularWords, adjectivePluralWords]

	# Verbs
	def verbs(self):
		sql = 'SELECT verb,' + self.country + ' FROM verbs'				
		c.execute(sql)
		rows = c.fetchall()
		verbs = { word[0].lower() : word[1].lower() for word in rows}
		
		return verbs

	# productTypes
	def productTypes(self):
		sql = 'SELECT type,' + self.country + ' FROM productTypes'
		c.execute(sql)
		rows = c.fetchall()				
		productTypes = { productType[0].lower() : productType[1].lower() for productType in rows }		
		# Return Dict
		return productTypes

	# ProductMaterials
	def productMaterials(self):
		sql = 'SELECT material,' + self.country + ' FROM materials'
		c.execute(sql)
		rows = c.fetchall()
		productMaterials = { material[0].lower() : material[1] for material in rows }
		# Append the name to dict
		productMaterials['name'] = 'material'
		return productMaterials

	# Product Features
	def productFeatures(self):
		sql = 'SELECT feature,' + self.country + ' FROM features'
		c.execute(sql)
		rows = c.fetchall()		
		productFeatures = { feature[0].lower() : feature[1].lower() for feature in rows }
		# Append the name to dict
		productFeatures['name'] = 'feature'

		return productFeatures

	# Product Sizes
	def productSizes(self):
		sql = 'SELECT size,' + self.country + ' FROM sizes'
		c.execute(sql)
		rows = c.fetchall()
		productSizes = { size[0].lower() : size[1].lower() for size in rows }
		return productSizes

	# 2020 Templates
	def product2020Templates(self):				
		sql = 'SELECT template, ' + self.country + ' FROM product2020Templates'
		c.execute(sql)						
		# Create Dict from data
		rows = c.fetchall()
		templates = { template[0].lower() : template[1] for template in rows}		
		# Return Dict
		return templates
		
	# 2021 templates
	def product2021Templates(self):				
		sql = 'SELECT template, eng, ' + self.country + ' FROM product2021Templates'
		c.execute(sql)						
		# Create Dict from data
		rows = c.fetchall()

		# templates = { self.country + '_' + template[0].lower() : template[1] for template in rows}
		eng_templates = { template[0].lower() : template[1] for template in rows }
		local_templates = { template[0].lower() : template[2] for template in rows }
		
		# If local is missing translation, give the english text, so we won't have empty values.
		for local in local_templates:
			if local_templates[local] == '':								
				local_templates[local] = eng_templates[local]	
				# If missing, then add in log	
				self.log.missingSmartphoneTemplate(country = self.country, key = local)		 				
		
		# Return Dict 
		return local_templates
	
	# Watchstraps templates 
	def watchstrapTemplates(self):
		sql = 'SELECT id,' + self.country + ' FROM watchstrapTemplates'
		c.execute(sql)
		rows = c.fetchall()								
		templates = { template[0] : str(template[1]) for template in rows}	
		return templates

	def watchstrapMaterialTemplates(self):
		sql = 'SELECT id, material,' + self.country + ' FROM watchstrapMaterialTemplates'
		c.execute(sql)
		rows = c.fetchall()
		templates = { template[0] : { 'material' : template[1], 'template' : template[2] }  for template in rows}
		return templates
	
	def watchstrapFeatureTemplates(self):
		sql = 'SELECT id, feature,' + self.country + ' FROM watchstrapFeatureTemplates'
		c.execute(sql)
		rows = c.fetchall()
		templates = { template[0] : { 'feature' : template[1], 'template' : template[2] }  for template in rows}
		return templates
	
	def watchstrapSizeTemplates(self):
		sql = 'SELECT id, ' + self.country + ' FROM watchstrapSizeTemplates'
		c.execute(sql)
		rows = c.fetchall()		
		templates = { 'template' : template[1] for template in rows}
		return templates
	
	def watchstrapEndings(self):
		sql = 'SELECT id, ' + self.country + ' FROM watchstrapEndings'
		c.execute(sql)
		rows = c.fetchall()		
		templates = { 'end' : template[1] for template in rows}
		
		return templates		