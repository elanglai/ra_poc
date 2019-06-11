import json
import logging
from urllib.parse import unquote
from controller.product_assistant_controller import process

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.debug('Start lambda function: {}'.format(context.function_name))
    logger.info('Received event: {}'.format(str(event)))
    
    # Convert event to json structure
    eventJson = json.loads(unquote(str(event)).replace("'","\""))

    replyMessage = process(eventJson)

    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>{}</Message></Response>'.format(replyMessage)
