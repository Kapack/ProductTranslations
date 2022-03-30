import random
from db.Select import Select

class Watchstrap:

    def initTemplate(self, product, country):
        select = Select(country)	
        watchstrapTemplates = select.watchstrapTemplates()
        watchTemplate = []
        materialTemplates = select.watchstrapMaterialTemplates()

        # Give where only DeviceName, so we alwaus have at least one translated
        for template in watchstrapTemplates:
            # if ('[DEVICE NAME]' in watchstrapTemplates[template]) and ('[MATERIAL]' not in watchstrapTemplates[template]) and ('[COLOR]' not in watchstrapTemplates[template]):
            if ('[DEVICE NAME]' in watchstrapTemplates[template]):
                # Append Matching Templates to a list
                watchTemplate.append(watchstrapTemplates[template])
                # Pick a random, and make it first element of our description
                product['description'] = random.choice(watchTemplate) + ' '	

		# If product has Both color And material
        if (product['attributes']['color'] and product['attributes']['material']):
            # Find each template that has both
            for template in watchstrapTemplates:	
                if ('[COLOR]' in watchstrapTemplates[template]) and ('[MATERIAL]' in watchstrapTemplates[template]):	
                    # Append Matching Templates to a list
                    watchTemplate.append(watchstrapTemplates[template])
                    # Pick a random, and make it first element of our description
                    product['description'] = random.choice(watchTemplate) + ' '	
		
        # # If product only has Color
        if (product['attributes']['color'] and str(product['attributes']['material']) == ''):           
            # Find each template that has Color and Not Material
            for template in watchstrapTemplates:	
                if ('[COLOR]' in watchstrapTemplates[template]) and ('[MATERIAL]' not in watchstrapTemplates[template]):	
                    # Append Matching Templates to a list
                    watchTemplate.append(watchstrapTemplates[template])
                    # Pick a random, and make it first element of our description
                    product['description'] = random.choice(watchTemplate) + ' '

        # If product only has Material
        if (not product['attributes']['color'] and str(product['attributes']['material']) != ''):                   
            for matTem in materialTemplates:
                # If product has a material attribute, matches materialTemplate and translated version exists
                if materialTemplates[matTem]['material'] == product['attributes']['material'] and materialTemplates[matTem]['template'] != '' :
                    # Find each baseTemplate that has Material and Not Color
                    for template in watchstrapTemplates:	
                        if ('[MATERIAL]' in watchstrapTemplates[template]) and ('[COLOR]' not in watchstrapTemplates[template]):	
                            # Append Matching Templates to a list
                            watchTemplate.append(watchstrapTemplates[template])
                            # Pick a random, and make it first element of our description
                            product['description'] = random.choice(watchTemplate) + ' '	        
        return product
    
    def attrText(self, product, country):
        select = Select(country)	
        materialTemplates = select.watchstrapMaterialTemplates()
        matTemplate = []
        featureTemplates = select.watchstrapFeatureTemplates()
        fetTemplate = []

        # Insert material texts
        i = 1
        for materialTemplate in materialTemplates:
            # If product has a material attribute, matches materialTemplate and translated version exists
            if materialTemplates[i]['material'] == product['attributes']['material'] and materialTemplates[i]['template'] != '' :
                # Append matching templates to a list
                matTemplate.append(materialTemplates[i]['template'])
            i += 1

        # Pick a random, from above created list
        if matTemplate:							
            product['description'] += random.choice(matTemplate)
		
        # Inserting Feature Text		
        i = 1
        for featureTemplate in featureTemplates:
            # print featureTemplates[i]['template']
            if featureTemplates[i]['feature'] == product['attributes']['feature'] and featureTemplates[i]['feature'] != '' :								
                # Append matching templates to a list
                fetTemplate.append(featureTemplates[i]['template'])
            i += 1			

            # Pick a random, from above created list
            if fetTemplate:	
                product['description'] += random.choice(fetTemplate)	
        
        return product
    
    def sizeText(self, product, country):
        select = Select(country)	
        sizeTemplates = select.watchstrapSizeTemplates()

        # Sizes
        # if translated sizeTemplates exists
        if sizeTemplates:
            # Split template into list, so we can find current/previous word and replace
            sizeTemplateList = sizeTemplates['template'].split()
            # Loop through all keys
            for dictKey in product['sizes']:
                # Check if product Key does not has value (If attribute is empty)
                if bool(product['sizes'][dictKey]) == False:
                    # If product does not have any value, remove variable string - eg. Width: [WIDTH] - from description					
                    if sizeTemplates['template'].find('[' + dictKey.upper() + ']') != -1:
                        # Find the index in the sizeTemplateList, where we have dictkey
                        currentWordIndex = int(sizeTemplateList.index('[' + dictKey.upper() + '].')) # Notice the dot
                        previousWordIndex = int(currentWordIndex - 1)
                        # Remove current and previewous word
                        sizeTemplateList.remove(sizeTemplateList[currentWordIndex])
                        sizeTemplateList.remove(sizeTemplateList[previousWordIndex])
                
                # If currentProudct has attribute, replace variable in list with attribute
                else:
                    sizeTemplateList = [word.replace('[' + dictKey.upper() + '].', product['sizes'][dictKey] + '.') for word in sizeTemplateList]
            
            # If sizeTemplateList only consists of one word, we don't want to use it
            if len(sizeTemplateList) != 1:
                # Make sizeTemplateList	back to a string and append to description.
                sizeTemplate = ' '.join([str(elem) for elem in sizeTemplateList])
                product['description'] += sizeTemplate
        
        return product
    
    def endingText(self, product, country):
        select = Select(country)	
        endTemplates = select.watchstrapEndings()

        for ending in endTemplates:			
            # Append ending to description
            product['description'] += endTemplates[ending]
        
        return product