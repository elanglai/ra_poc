import boto3
import json
from botocore.exceptions import ClientError

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
dynamodbClient = boto3.client('dynamodb')

TABLE_PRODUCT_MAPPING = 'product_mapping'
TABLE_PRODUCT_MAPPING_DATA_JSON_FILE = './util/data/product_mapping_table_data.json'

def createProductMappingTable():
    try:
        dynamodbClient.describe_table(
            TableName=TABLE_PRODUCT_MAPPING
        )
        print('DynamoDB {} already exists.'.format(TABLE_PRODUCT_MAPPING))
    except ClientError:
        # Create the DynamoDB table.
        print('DynamoDB {} does not exist.'.format(TABLE_PRODUCT_MAPPING))
        table = dynamodb.create_table(
            TableName=TABLE_PRODUCT_MAPPING,
            KeySchema=[
                {
                    'AttributeName': 'competitor_catalog_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'competitor_catalog_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_PRODUCT_MAPPING)
        
        # Print out some data about the table.
        print(table.item_count)
        pass


def createProductMappingData():
    table = dynamodb.Table(TABLE_PRODUCT_MAPPING)

    with open(TABLE_PRODUCT_MAPPING_DATA_JSON_FILE, 'r') as productMappingDataFile:
        productMappingDataList = json.load(productMappingDataFile)

    for productMappingData in productMappingDataList:
        table.put_item(
            Item={
                'competitor_catalog_id': productMappingData['competitor_catalog_id'],
                'ab_catalog_id': productMappingData['ab_catalog_id'],
                'reason':  productMappingData['reason'],
                'webpage_link': productMappingData['webpage_link'],
            }    
        )
    
def initTable(tableName):
    if tableName == TABLE_PRODUCT_MAPPING:
        createProductMappingTable()
        createProductMappingData()
        return 'Table initialization complete: {}'.format(tableName)
    return 'Table {} is not a valid table name. Possible values are [{}]'.format(tableName, TABLE_PRODUCT_MAPPING)    
