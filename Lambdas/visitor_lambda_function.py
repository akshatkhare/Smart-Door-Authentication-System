import json
import boto3
import time

dynamo_resource = boto3.resource('dynamodb')
dynamo_visitors_table = dynamo_resource.Table("visitors")
dynamo_passcodes_table = dynamo_resource.Table("passcodes")
dynamo_passcodes_match = dynamo_resource.Table("passcodes")

def lambda_handler(event, context):
    
    print("inside visito fun 1") 
    visitors_provided_otp = event['message']['passcode-input']     
    passcodes_response = dynamo_passcodes_table.scan()
    otps = []
    otp_faceid_dict = {}
   
    print("passcodes response")
    print(passcodes_response)
    for i in range(len(passcodes_response['Items'])):
        otp_faceid_dict[passcodes_response['Items'][i]['otp']] = passcodes_response['Items'][i]['faceId']
    
    #faceId = otp_faceid_dict[visitors_provided_otp]
    
    if visitors_provided_otp in otp_faceid_dict.keys():
        print("Give access to visitor")       
        key = {'faceId' : otp_faceid_dict[visitors_provided_otp]}   
        visitors_response = dynamo_visitors_table.get_item(Key=key)
        
        passcode_response_match = dynamo_passcodes_match.get_item(Key=key)
        keys_list_passcode = list(passcode_response_match.keys())
        print(keys_list_passcode)
        print(passcode_response_match)
        cur_time = int(time.time())
        exp_time = "0"
        if('Item' in keys_list_passcode):
            exp_time = passcode_response_match['Item']['expiration']
        #if('Item' in keys_list_passcode) and cur_time <= int(exp_time):
        #    print("OTP already present")
            
        visitors_name = visitors_response['Item']['name']
        msg = ""
        if cur_time > int(exp_time):
            msg = "The OTP you entered has expired"
        elif visitors_name:
            print("if")  
            msg = "Welcome to the house: " + visitors_name
        else:
            print("else") 
            msg = "Entry not allowed"
        return{
        'statusCode': 200,
        'body': json.dumps(msg)
        }
    return{
    'statusCode': 200,
    'body': json.dumps('Entry not allowed')
    }
