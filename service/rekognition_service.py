import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

MIN_WORD_SIZE_THRESHOLD = 1
MAX_WORD_SIZE_THRESHOLD = 20

rek = boto3.client('rekognition')

def detected_texts(rek_response):
    detected_texts = []
    for text in rek_response['TextDetections']:
        if len(text['DetectedText']) >= MIN_WORD_SIZE_THRESHOLD and len(text['DetectedText']) <= MAX_WORD_SIZE_THRESHOLD:
            detected_texts.append(text['DetectedText'])
        
    print(' ..detected_words={}'.format(detected_texts))
    return detected_texts

def rek_searchByTextExtraction(s3_bucket, s3_key):
    logger.debug(' ..rek_searchByTextExtraction:  s3_bucket={}, s3_key={}'.format(s3_bucket, s3_key))
    
    rek_response = rek.detect_text(Image={
        'S3Object':{
            'Bucket': s3_bucket,
            'Name': s3_key
        }
    })

    return detected_texts(rek_response)