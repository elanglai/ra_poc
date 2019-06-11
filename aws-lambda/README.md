[Return to Overview](../README.md)

# AWS Lambda

## Code structure overview
- README.md - this file
- buildspec.yml - this file is used by AWS CodeBuild to package your
  application for deployment to AWS Lambda
- index.py - this file contains the sample Python code for the web service
- template.yml - this file contains the AWS Serverless Application Model (AWS SAM) used
  by AWS CloudFormation to deploy your application to AWS Lambda and Amazon API
  Gateway.
- tests/ - this directory contains unit tests for your application
- template-configuration.json - this file contains the project ARN with placeholders used for tagging resources with the project ID

## Steps to reference a revised image model endpoint
To run the lambda against a new image model, the Python script `.\services\sagemaker_service.py` needs to be updated. See the inline comments.

1. You can do so directly on via the Lambda editor https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/ProductAssistant?tab=graph

2. Navigate to the appropriate file to make the change as per the sample below.
``` python
SAGEMAKER_ENDPOINT_NAME = 'DEMO-imageclassification-ep--2019-06-10-02-00-45'
object_categories = ['3RT2023-1NF30', 'CWB9-11-30D15', 'MC9A-30-01-K7-S-E', 'XTCE009B01', 'LC1D09KUE']
```

3. Click Save and allow one minute for the changes to take effect

