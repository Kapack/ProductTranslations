from db.Select import Select

class Smartphone:

    def assignTemplate(self, product, country):
        select = Select(country)
        product2021Templates = select.product2021Templates()
        product2020Templates = select.product2020Templates()		
        # Find correct template value, from productTemplates[key]. Searching for 
        template = product2020Templates.get(product['template']) or product2021Templates.get(product['template'])

        # Assign correct template description
        if template is not None:
            # Replace [DEVICE NAME] with Product Device name in template
            template = template.replace('[DEVICE NAME]', product['device']['manName'] + ' ' + product['device']['devName'])
            product['description'] = template

        return product