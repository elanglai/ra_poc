Welcome to the AWS Machine Learning POC setup for Uncle Rocky using Sagenaker & MXNET
==============================================
This sample code helps get you started with a Python scripts and configurations for
Sagemaker and MXNET.

What's Here
-----------

This sample includes:

* README.md - this file
* rockwell4.sh - this file is used to convert directory structure of the Images into RecordIO files
* Product-Assistant-Image-Machine-Learning-ra-dataset - this file is used by sagemaker in Notebook Instance to do -
* 1. Create create, train and validate Model for Image classification
* 2. Fine-tune the Image classification model
* 3. Deploy classifier into EC2 instance and perform image classification
* 4. Create Endpoint to host the model and perform realtime inference 
* 5. Deploy Endpoint to EC2 Instance and expose REST service

Window Setup Steps for converting Images to RecordIO file using MXNT

1. Download and install https://www.anaconda.com/distribution/
2. Make Sure Numpy is also installed or intall it mannually, pip install numpy
3. Install MXNet with Python. pip install mxnet
4. Install opencv, pip install opencv-python 
5. Download https://github.com/apache/incubator-mxnet
6. Open Command prompt and run this Bat script,incubator-mxnet-master\setup-utils\install-mxnet-windows-python.bat
7. Copy \sagemaker\script\rockwell4.sh in incubator-mxnet-master\example\image-classification\data
8. Create folder "ra_dataset" in incubator-mxnet-master\example\image-classification\data
9. Dump all Images into ra_dataset in separate folders based on the type of Images
10.In rockwell4.sh change the IMG_TRAIN to total number of Images you have added into ra_dataset
11.In rockwell4.sh change the MX_DIR to point to downloaded directory of incubator-mxnet-master
12.Run the script rockwell4.sh
13.It will generate two rec files - One for train and another for validation
