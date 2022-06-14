from db.Select import Select

class Smartphone:

    def assignTemplate(self, product:dict, country:str) -> dict:
        select = Select(country)
        product2021Templates = select.product2021Templates()
        product2020Templates = select.product2020Templates()

        # Find correct template value, from productTemplates[key]. Searching for 
        template = product2020Templates.get(product['template']) or product2021Templates.get(product['template'])
        product['description'] = template
        return product