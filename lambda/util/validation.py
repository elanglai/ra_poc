import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# class variable shared by all instances
NO_IMAGE_DETECTED = 'NO_IMAGE_DETECTED'

def validate(msgIn, imageUrlIn):
    logger.debug(' ..validate: msg={} imageUrl={}'.format(msgIn, imageUrlIn))
    responseCode = ''

    if imageUrlIn == '':
        responseCode = NO_IMAGE_DETECTED

    return responseCode
