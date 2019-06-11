import boto3
import botocore.vendored.requests.packages.urllib3 as urllib3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
bucket = 'product-assistant-image-classification'
folder = 'client-provided-input-images'

""" Uploads image to s3 bucket """
def uploadS3(imageUrl, fromNumber):
    logger.debug(' ..s3_image_service#uploadS3:  imageUrl={}, fromNumber={}'.format(str(imageUrl), fromNumber))
    imageName = imageUrl.split('/')[-1]
    
    http = urllib3.PoolManager()
    key = '{0}/{1}-{2}.jpg'.format(folder, fromNumber, imageName)
    logger.info(' ..bucket={}, key={}'.format(bucket, key))
    
    imageObject = http.request('GET', imageUrl, preload_content=False)
    s3.upload_fileobj(imageObject, bucket, key)
    
    return imageObject, bucket, key

def downloadS3(bucket, key):
    obj = s3.get_object(
        Bucket=bucket, 
        Key=key)
    return obj['Body'].read()
    