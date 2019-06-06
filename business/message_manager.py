import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class MessageManager:
    
    # Static message reponse
    NO_IMAGE_DETECTED = 'Please upload an image of the product\'s facade.'
    PRODUCT_NOT_FOUND = 'We\'re sorry, we could not find a match for the product you\'re searching.'
    NOT_FOUND_DUE_TO_LOW_PROBABLITY = 'We\'re sorry, the image you provided did not resolve to a product match. Please retry with a new image.'

    # Dynamic messages response when the searched product was found
    def PRODUCT_FOUND(self, item):
        replyMsg = 'This is a {}.'.format(item.competitorCatalogId)
        
        if item.abCatalogId != '':
            replyMsg += ' The AB equivalent is {}.'.format(item.abCatalogId)
            if  item.reason != '':
                replyMsg += ' {} is better because it has {}.'.format(item.abCatalogId, item.reason)
        
            if item.webPageLink != '':
                # Pad the first paragraph to force the link to show on a seperate SMS block
                replyMsg = replyMsg.ljust(153)
                replyMsg += 'AB product link: {}'.format(item.webPageLink)
        else:
            replyMsg += ' No AB equivalent was found.'.format(item.abCatalogId)

        return replyMsg
        
    def __init__(self):
        self.prevMsg = ''
        self.msgOut = ''
    
    def retrieveMsgByResponseCode(self, responseCode, productMappingItem):
        logger.info(' ..MessageManager#retrieveMsgByResponseCode: responseCode={} productMappingItem={}'.format(responseCode, productMappingItem))
    
        if responseCode == 'PRODUCT_NOT_FOUND':
            self.msgOut = self.PRODUCT_NOT_FOUND
        elif responseCode == 'NO_IMAGE_DETECTED':
            self.msgOut = self.NO_IMAGE_DETECTED
        elif responseCode == 'PRODUCT_NOT_FOUND_DUE_TO_LOW_PROBABLITY':
            self.msgOut = self.NOT_FOUND_DUE_TO_LOW_PROBABLITY
        elif responseCode == 'PRODUCT_FOUND':
            self.msgOut = self.PRODUCT_FOUND(productMappingItem)
            
        logger.info(' ..return msg={}'.format(self.msgOut))
    
        return self.msgOut