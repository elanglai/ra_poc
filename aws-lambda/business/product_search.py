import logging
from service.rekognition_service import rek_searchByTextExtraction 
from service.dynamodb_product_mapping import findProductByWordList
from service.dynamodb_product_mapping import findProductByKey
from service.sagemaker_service import sagemaker_searchByClassification
from service.s3_image_service import downloadS3
from model.product_mapping_item import ProductMappingItem

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ProductSearch:

    # class variable shared by all instances
    PRODUCT_NOT_FOUND = 'PRODUCT_NOT_FOUND'
    PRODUCT_FOUND = 'PRODUCT_FOUND'

    def __init__(self, image_object, s3_bucket, p3_key):
        self.imageObject = image_object,
        self.s3_bucket = s3_bucket
        self.s3_key = p3_key
        self.productMappingItem = ''
        self.responseCode = ''

    # Search the product based on the extracted text
    def searchByTextExtraction(self):
        logger.debug(' ..ProductSearch#searchByTextExtraction')

        # invoke rekognition serice
        word_list = rek_searchByTextExtraction(self.s3_bucket, self.s3_key)
        
        # find product that matches one of the extracted keywords
        self.responseCode, self.productMappingItem = findProductByWordList(word_list)

    # Search the product's classification by comparing the image against the previously trained data model
    def searchByImageClassification(self):
        logger.debug(' ..ProductSearch#searchByImageClassification')

        image = downloadS3(self.s3_bucket, self.s3_key)
        
        # invoke sagemaker service
        self.responseCode, self.productId = sagemaker_searchByClassification(image)

        if self.responseCode == 'PRODUCT_FOUND':
            self.responseCode, self.productMappingItem = findProductByKey(self.productId)

    def execute(self):
        # First, try matching the user's product image based on extracted text hoping we can use the text as a model number
        self.searchByTextExtraction()

        # Second, try matching the user's product image by running it against an image classification data model
        if self.responseCode != 'PRODUCT_FOUND':
            self.searchByImageClassification()
        
    def getResponseCode(self):
        return self.responseCode
        
    def getProductMappingItem(self):
        return self.productMappingItem
