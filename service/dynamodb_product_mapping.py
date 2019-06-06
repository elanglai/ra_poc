import boto3
import logging
from model.product_mapping_item import ProductMappingItem

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client('dynamodb')
PRODUCT_TABLE = "product_mapping"

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
            
            productMappingItem = ProductMappingItem(
                item['competitor_catalog_id']['S'], 
                item['ab_catalog_id']['S'], 
                item['reason']['S'], 
                item['webpage_link']['S']
            )
        else:
            productMappingItem = ProductMappingItem(
                productId.lower(), 
                '', 
                '', 
                ''
            )
        
        return 'PRODUCT_FOUND', productMappingItem

def findProductByWordList(word_list):

    for word in word_list:
        searchResult = dynamodb.get_item(
            TableName = PRODUCT_TABLE, 
            Key = {
                'competitor_catalog_id':{
                    'S':word.upper()
                }
            }
        )

        if 'Item' in searchResult:
            item = searchResult['Item']
            
            competitorCatalogId = item['competitor_catalog_id']['S']
            abCatalogId = item['ab_catalog_id']['S']
            reason = item['reason']['S']
            webPageLink = item['webpage_link']['S']
        
            productMappingItem = ProductMappingItem(
                competitorCatalogId, 
                abCatalogId, 
                reason, 
                webPageLink
            )

            return 'PRODUCT_FOUND', productMappingItem
            
    return 'PRODUCT_NOT_FOUND', ''