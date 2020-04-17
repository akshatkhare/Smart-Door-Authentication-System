import json
import logging
import base64
import boto3
import os
import random 
import time, datetime
from decimal import Decimal 

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

smsClient = boto3.client('sns')

dynamo_resource = boto3.resource('dynamodb')
visitorsTable = dynamo_resource.Table("visitors")
passcodesTable = dynamo_resource.Table("passcodes")


def fill_dynamodb_visitors(faceId, name, phoneNumber,fileName):
    #visitor = visitorsTable.query(KeyConditionExpression=Key('faceId').eq(faceId))    
    #currTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    imageName = fileName + ".jpg"
    data = {
        "faceId" : faceId,
        "name" : name,
        "phoneNumber" : phoneNumber,
        "photos" : [
            {
                "objectKey" : imageName,
                "bucket" : "visitorphotovault",
                "createdTimestamp" : str(time.ctime(time.time()))
            }
        ]
    }
    visitorsTable.put_item(Item = data)
    msg = "Visitor " + name + " has been added!"
    return msg
    
def generate_passcode():
    return random.randint(100001, 999999)
    
def visitorSMS(contact, pin):
    LinkToEnterOTP = "http://visitorvault.s3-website-us-east-1.amazonaws.com"
    msg = 'Hello there, here is your pin to enter in the apartment. \n PIN : ' + str(pin)+ "\nGo to " + LinkToEnterOTP+" to enter pin. Your pin will expire in 5 minutes."
    sns = boto3.client('sns')
    response = sns.publish(
    PhoneNumber= '+1' + contact,
    Message=msg # this should include link to submit visitor info
    )
    
def fill_dynamodb_passcodes(faceId, passcode):
    expiry_time = int(time.time() + (60 * 5))
    data = {
        "faceId" : faceId,
        "passcode" : passcode,
        "ttl" : expiry_time
    }
    passcodesTable.put_item(Item = data)



def lambda_handler(event, context):
    # TODO implement
    visitor_name = event['message']['name-input']
    visitor_phone = event['message']['phone-input']
    visitor_face_id = event['message']['face-id']
    file_name = event['message']['file-name']
    print("inside owner lambda")
    msg = fill_dynamodb_visitors(visitor_face_id, visitor_name, visitor_phone,file_name)
    print("generate_passcode")
    pin = generate_passcode()
    print(pin)
    print("visitorSMS")
    visitorSMS(visitor_phone,pin)
    print("fill_dynamodb_passcodes")
    fill_dynamodb_passcodes(visitor_face_id,pin)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Pers Approved')
        }
