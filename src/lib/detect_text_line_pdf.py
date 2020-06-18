#Detects text in a document stored in an S3 bucket. Display polygon box around text and angled text 
import boto3
import io
from io import BytesIO
import sys

import psutil
import time
import json

import math
from PIL import Image, ImageDraw, ImageFont


# Displays information about a block returned by text detection and text analysis
def DisplayBlockInformation(block):
    print('Id: {}'.format(block['Id']))
    if 'Text' in block:
        print('    Detected: ' + block['Text'])
    print('    Type: ' + block['BlockType'])
   
    if 'Confidence' in block:
        print('    Confidence: ' + "{:.2f}".format(block['Confidence']) + "%")

    if block['BlockType'] == 'CELL':
        print("    Cell information")
        print("        Column:" + str(block['ColumnIndex']))
        print("        Row:" + str(block['RowIndex']))
        print("        Column Span:" + str(block['ColumnSpan']))
        print("        RowSpan:" + str(block['ColumnSpan']))    
    
    if 'Relationships' in block:
        print('    Relationships: {}'.format(block['Relationships']))
    print('    Geometry: ')
    print('        Bounding Box: {}'.format(block['Geometry']['BoundingBox']))
    print('        Polygon: {}'.format(block['Geometry']['Polygon']))
    
    if block['BlockType'] == "KEY_VALUE_SET":
        print ('    Entity Type: ' + block['EntityTypes'][0])
    if 'Page' in block:
        print('Page: ' + block['Page'])
    print()

def process_text_detection(bucket, document):

    
    #Get the document from S3
    s3_connection = boto3.resource('s3')
                          
    s3_object = s3_connection.Object(bucket,document)
    s3_response = s3_object.get()

    # stream = io.BytesIO(s3_response['Body'].read())
    # image=Image.open(stream)

   
    # Detect text in the document
    
    client = boto3.client('textract')
    #process using image bytes                      
    #image_binary = stream.getvalue()
    #response = client.detect_document_text(Document={'Bytes': image_binary})

    #process using S3 object
    response = client.start_document_text_detection(DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': document}})



    res
    return 0 


def get_document_detection():
    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId='0d86fd584b7507ad05a9ec2c819937ff3db6721765fbb3b61549d221c4c977f4')
    with open('data.json', 'w') as outfile:
        json.dump(response, outfile)

def get_document_analysis():
    client = boto3.client('textract')
    response = client.get_document_analysis(JobId='8562809f76a5d99017e2b49943dd01ffb35a4fe3dc0f428bac6c80acdce2f69c')
    with open('data_analysis.json', 'w') as outfile:
        json.dump(response, outfile)

def main():

    # bucket = 'textract-console-us-east-2-11a8b889-16d2-4002-90b7-d88fa1e88221'
    # document = '2016___gp_1_1_17_pages_3.pdf'
    # block_count=process_text_detection(bucket,document)
    # print("Blocks detected: " + str(block_count))
    get_document_analysis()
    print('Finished')
if __name__ == "__main__":
    main()
