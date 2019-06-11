import boto3
import logging
from model.product_mapping_item import ProductMappingItem

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client('dynamodb')
PRODUCT_TABLE = "product_mapping"

def getItemValue(key, item):
    value = ''
    if key in item:
        if item[key]['S'].upper() != 'NONE':
            value = item[key]['S']
    return value


def findProductByKey(productId):
        searchResult = dynamodb.get_item(
            TableName = PRODUCT_TABLE, 
            Key = {
                'competitor_catalog_id':{
                    'S':productId.upper()
                }
            }
        )
        
        if 'Item' in searchResult:
            item = searchResult['Item']
            
            ab_catalog_id = getItemValue('ab_catalog_id', item)
            reason = getItemValue('reason', item)
            link =  getItemValue('webpage_link', item)

            productMappingItem = ProductMappingItem(
                item['competitor_catalog_id']['S'], 
                ab_catalog_id, 
                reason, 
                link
            )
            return 'PRODUCT_FOUND', productMappingItem
        else:
            productMappingItem = ProductMappingItem(
                productId.lower(), 
                '', 
                '', 
                ''
            )
            return 'PRODUCT_FOUND_WIHOUT_PRODUCT_MAP', productMappingItem
        
        

def findProductByWordList(word_list):

    for word in word_list:
        
        responseCode, productMappingItem = findProductByKey(word)
        
        if responseCode == 'PRODUCT_FOUND':
            return responseCode, productMappingItem

    return 'PRODUCT_NOT_FOUND', ''