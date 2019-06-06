import json
import botocore.vendored.requests.packages.urllib3 as urllib3
from urllib.parse import unquote
import logging
from service.s3_image_service import uploadS3
from business.message_manager import MessageManager
from business.product_search import ProductSearch
from util.validation import validate
from util.reference_data import initTable

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def process(eventJson):

    # Initialization of DB instances.  Should be executed everytime the reference_data.py script is updated.
    if 'init_db_table' in eventJson.keys():
        return initTable(eventJson['init_db_table'])
        
    # Capture the fields of interest
    msgBody = eventJson['Body']
    imageUrl = ''
    if 'MediaUrl0' in eventJson.keys():
        imageUrl = eventJson['MediaUrl0']
    fromNumber = eventJson['From'].replace('+','')

    # Validate the message.
    responseCode = validate(msgBody, imageUrl)
    print('msgResponse = {}'.format(responseCode))

    msgManager = MessageManager()
    if responseCode == 'NO_IMAGE_DETECTED':
        return msgManager.retrieveMsgByResponseCode(responseCode, 'Hello')

    # Upload to S3
    image_object, s3_bucket, s3_key = uploadS3(imageUrl, fromNumber)

    # Trigger image search
    productSearch = ProductSearch(image_object, s3_bucket, s3_key)
    productSearch.execute()
    
    productMappingItem = productSearch.getProductMappingItem() 
    responseCode = productSearch.getResponseCode()
    
    print('productMappingItem={}'.format(productMappingItem))
    print('responseCode={}'.format(responseCode))

    return msgManager.retrieveMsgByResponseCode(responseCode, productMappingItem)
