[Return to Overview](../README.md)

# AWS API Gateway

The API Gateway which exposes the Lambda function needs to be configured such that it receives
a request of type (application/x-www-form-urlencoded) and return a response type(application/xml)
whereas the integration request is JSON and the response is XML.

The API Gateway setup is denoted from Twilio's support link below:

https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply-python-amazon-lambda