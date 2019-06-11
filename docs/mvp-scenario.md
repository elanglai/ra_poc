[Return to Overview](../README.md)

## MVP Flow

1. the user uses his mobile to interact with RA's Uncle Rocky service.  The user sends an image snapshot of the product he wants looked up.  
2. The SMS message is translated by Twilio to an HTTP post request to AWS's API gateway which exposes the Lambda function "processMessage".
3. The user's session is tracked via on the DynamoDB table "message-session". The Lambda is responsible for answering to the user's interaction. 
4. If an image is provided, the processing of the delegated to another Lambda function, namely "findMatchingPorduct".
5. The image first analyzed using Rekognization's text extraction service.  
6. The retrieved words are then used to lookup the DynamoDB table "product-mapping".
7. If no match found based on the extracted words, the image analyzed using Amazon's SageMaker which tries to deduce the product's classification (model) based on a previously trained data model. 
8. The deduced classification is then used to lookup the DynamoDB table "product-mapping".
9. If a match is round, the associated DB record item is returned which contains RA's equivalent product model and reason why RA's product is comparable or superior to the third party product.
10. RA's product characteristics is then looked up for additional links etc that can be used to return additional detailed information about the RA product and where the product can be ordered from.

**Note:**
Based on the outcome of the "findMatchingProduct" function, the "processMessage" function is responsible for creating the response back to the end-user. Likewise, if the end user interacts with the system and there's an ongoing session, this later function can be extended to entertain additional message request/responses.   
