import logging

class Log:
    def __init__(self) -> None:
        logging.basicConfig(filename="log/translationErrors.log", encoding='utf-8', format='%(asctime)s %(message)s', filemode='w', level=logging.INFO)
        self.logger = logging.getLogger()        

    def missingSmartphoneTemplate(self, country:str, key:str) -> None:    
        logging.warning('Missing Template: ' + key +  ' . Country' + country)
    
    def missingWord(self, country:str, word:str) -> None:     
        logging.warning('Missing Word: ' + word +  ' . Country' + country)        
    
    def missingProductType(self, country:str, productType:str) -> None:
        logging.warning('Missing ProductType: ' + productType +  ' . Country' + country)

    
    
    
