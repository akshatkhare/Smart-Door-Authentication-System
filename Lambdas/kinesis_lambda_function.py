import logging
import base64
import json
import boto3
import os
import random as r
import time
import cv2
from decimal import Decimal 


s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

smsClient = boto3.client('sns')

dynamo_resource = boto3.resource('dynamodb')

dynamo_visitors_table = dynamo_resource.Table("visitors")
dynamo_passcodes_table = dynamo_resource.Table("passcodes")


def lambda_handler(event, context):
    #event = {'Records': [{'kinesis': {'kinesisSchemaVersion': '1.0', 'partitionKey': 'adafcaa5-89d4-422f-bf27-4daa9b075595', 'sequenceNumber': '49605769860245632248889974945911519689281908967292797346', 'data': 'eyJJbnB1dEluZm9ybWF0aW9uIjp7IktpbmVzaXNWaWRlbyI6eyJTdHJlYW1Bcm4iOiJhcm46YXdzOmtpbmVzaXN2aWRlbzp1cy1lYXN0LTE6OTE5MTE1ODE2NzM2OnN0cmVhbS9rdnMyLzE1ODUxNzk0MTEzNzUiLCJGcmFnbWVudE51bWJlciI6IjkxMzQzODUyMzMzMTgxNDY3MTI5Mjc5NTY0OTc1NDI5MTg1MjUwNTc4NTg0NjI3IiwiU2VydmVyVGltZXN0YW1wIjoxLjU4NjA0MDMzOTQ0NEU5LCJQcm9kdWNlclRpbWVzdGFtcCI6MS41ODYwNDAzMzgwMDZFOSwiRnJhbWVPZmZzZXRJblNlY29uZHMiOjEuMzc2OTk5OTc0MjUwNzkzNX19LCJTdHJlYW1Qcm9jZXNzb3JJbmZvcm1hdGlvbiI6eyJTdGF0dXMiOiJSVU5OSU5HIn0sIkZhY2VTZWFyY2hSZXNwb25zZSI6W3siRGV0ZWN0ZWRGYWNlIjp7IkJvdW5kaW5nQm94Ijp7IkhlaWdodCI6MC40MTE1MjgyLCJXaWR0aCI6MC4yNDI5MTA2MiwiTGVmdCI6MC40NzA3MjQ1MiwiVG9wIjowLjU0MDMyNzd9LCJDb25maWRlbmNlIjoxMDAuMCwiTGFuZG1hcmtzIjpbeyJYIjowLjUxODExNTUsIlkiOjAuNjg3MjQ1MTMsIlR5cGUiOiJleWVMZWZ0In0seyJYIjowLjYyOTYwNjEsIlkiOjAuNjg4NDY2MjUsIlR5cGUiOiJleWVSaWdodCJ9LHsiWCI6MC41Mjg0MzI2LCJZIjowLjg0NTIzMTA2LCJUeXBlIjoibW91dGhMZWZ0In0seyJYIjowLjYyMDc4NzcsIlkiOjAuODQ2NDAwNiwiVHlwZSI6Im1vdXRoUmlnaHQifSx7IlgiOjAuNTY3MTMwMTUsIlkiOjAuNzY4MzA0OTQsIlR5cGUiOiJub3NlIn1dLCJQb3NlIjp7IlBpdGNoIjoxLjM2MzgyMTQsIlJvbGwiOi0xLjczMjQzNjQsIllhdyI6LTguNDQ4MDUyfSwiUXVhbGl0eSI6eyJCcmlnaHRuZXNzIjo0NC4wNjAyNjUsIlNoYXJwbmVzcyI6NzguNjQzNX19LCJNYXRjaGVkRmFjZXMiOlt7IlNpbWlsYXJpdHkiOjk5Ljc1OTAzLCJGYWNlIjp7IkJvdW5kaW5nQm94Ijp7IkhlaWdodCI6MC40NDQyNiwiV2lkdGgiOjAuNDE1NjgyLCJMZWZ0IjowLjI1Mjg3NSwiVG9wIjowLjI1ODM5MX0sIkZhY2VJZCI6IjkwMjk0ZDAwLTQ5NzQtNGYyNy04NWI4LTA1NmJjN2IyN2EwNyIsIkNvbmZpZGVuY2UiOjEwMC4wLCJJbWFnZUlkIjoiZDM5Y2YyN2QtYzk5YS0zOWI1LTgyMjgtMzNmMDdkMTQ1Y2EzIiwiRXh0ZXJuYWxJbWFnZUlkIjoic2FtYXN0aCJ9fV19XX0=', 'approximateArrivalTimestamp': 1586040342.595}, 'eventSource': 'aws:kinesis', 'eventVersion': '1.0', 'eventID': 'shardId-000000000026:49605769860245632248889974945911519689281908967292797346', 'eventName': 'aws:kinesis:record', 'invokeIdentityArn': 'arn:aws:iam::919115816736:role/service-role/kinesisStreamLambda-role-rt87cqzi', 'awsRegion': 'us-east-1', 'eventSourceARN': 'arn:aws:kinesis:us-east-1:919115816736:stream/kds-image-data'}]}
    logging.info("API CALLED. EVENT IS:{}".format(event))
    print(event)
    print("Data streaming")
    records_length = len(event['Records'])
    for i in range(records_length):
        data = event['Records'][i]['kinesis']['data']
        json_data = json.loads(base64.b64decode(data).decode('utf-8'))
        if len(json_data['FaceSearchResponse']) < 1:
            return {
                'statusCode': 200,
                'body': json.dumps('No Face Response')
            }
        else:
            break
    #data = event['Records'][0]['kinesis']['data']
    print(base64.b64decode(data))
    #json_data = json.loads(base64.b64decode(data).decode('utf-8'))
    stream_name="kvs2"
    #json_data = {"InputInformation":{"KinesisVideo":{"StreamArn":"arn:aws:kinesisvideo:us-east-1:919115816736:stream/kvs2/1585179411375","FragmentNumber":"91343852333181467129279564975429185250578584627","ServerTimestamp":1.586040339444E9,"ProducerTimestamp":1.586040338006E9,"FrameOffsetInSeconds":1.3769999742507935}},"StreamProcessorInformation":{"Status":"RUNNING"},"FaceSearchResponse":[{"DetectedFace":{"BoundingBox":{"Height":0.4115282,"Width":0.24291062,"Left":0.47072452,"Top":0.5403277},"Confidence":100.0,"Landmarks":[{"X":0.5181155,"Y":0.68724513,"Type":"eyeLeft"},{"X":0.6296061,"Y":0.68846625,"Type":"eyeRight"},{"X":0.5284326,"Y":0.84523106,"Type":"mouthLeft"},{"X":0.6207877,"Y":0.8464006,"Type":"mouthRight"},{"X":0.56713015,"Y":0.76830494,"Type":"nose"}],"Pose":{"Pitch":1.3638214,"Roll":-1.7324364,"Yaw":-8.448052},"Quality":{"Brightness":44.060265,"Sharpness":78.6435}},"MatchedFaces":[]}]}
    print('JSON DATA',json_data)
    
    
    smsClient = boto3.client('sns')
    mobile = "9175309620"
    
    faceId='123'
    fileName = 'name1.jpeg'
    face_search_response = json_data['FaceSearchResponse']
    if face_search_response is None or len(face_search_response) == 0:
        return ("No one at the door")
    else:
        matched_face = json_data['FaceSearchResponse'][0]['MatchedFaces']
        print("matched face ")
    
    if face_search_response is not None and ( matched_face is None or len(matched_face)==0):
        fragmentNumber= json_data['InputInformation']['KinesisVideo']['FragmentNumber']
        fileName,faceId=store_image(stream_name,fragmentNumber, None, json_data)
        print("after image added to s3 and collection")
    else:
        image_id = json_data['FaceSearchResponse'][0]['MatchedFaces'][0]['Face']['ImageId']
        print('IMAGEID',image_id)
        faceId = json_data['FaceSearchResponse'][0]['MatchedFaces'][0]['Face']['FaceId']
        print('FACEID',faceId)

    print("faceid after")
    print(faceId)
    key = {'faceId' : faceId}   
    visitors_response = dynamo_visitors_table.get_item(Key=key)
    
    keys_list = list(visitors_response.keys())
    print(keys_list)
    print(visitors_response)
    print("data")
    
    
    if('Item' in keys_list):
    
        otp=""    
        for i in range(4):
            otp+=str(r.randint(1,9))
        print("otp "+str(otp))
        
        fragmentNumber= json_data['InputInformation']['KinesisVideo']['FragmentNumber']
        fileName,faceId=store_image(stream_name,fragmentNumber, faceId, json_data)
        
        phone_number_visitor = visitors_response['Item']['phoneNumber']
        face_id_visitor = visitors_response['Item']['faceId']
        
        
        
        visitors_name = visitors_response['Item']['name']
        visitors_photo = visitors_response['Item']['photos']
        photo={'objectKey':fileName , 'bucket' : 'visitorphotovault', 'createdTimestamp' : str(time.ctime(time.time()))}
        visitors_photo.append(photo)
        
        print("inside current addition")
        my_visitor_entry = {'faceId' : face_id_visitor , 'name' : visitors_name , 'phoneNumber' : phone_number_visitor , 'photos' : visitors_photo}
        dynamo_visitors_table.put_item(Item=my_visitor_entry)
        
        passcode_response = dynamo_passcodes_table.get_item(Key=key)
        keys_list_passcode = list(passcode_response.keys())
        print(key)
        print("key list passcode")
        print(keys_list_passcode)
        print(passcode_response)
        cur_time = int(time.time())
        print("curr time "+str(cur_time))
        if('Item' in keys_list_passcode):
            print("if item in keys_list_passcode")
            exp_time = passcode_response['Item']['expiration']
            print("exp time "+exp_time)
        if('Item' in keys_list_passcode) and (cur_time <= int(exp_time)):
            print("OTP already present")
            #otp = passcode_response['Item']['otp']
            #sendOtpToVisitor(phone_number_visitor, otp)
        else:
            my_string = {'faceId' : face_id_visitor, 'otp': otp, 'expiration' : str(int(time.time() + 300))}
            dynamo_passcodes_table.put_item(Item=my_string)
            sendOtpToVisitor(phone_number_visitor, otp)
            print("sent message to visitor")
        
    elif matched_face is None or len(matched_face) == 0:
        phone_number_owner = '9175309620'
        link_visitor_image = ' http://visitorphotovault.s3-website-us-east-1.amazonaws.com/' + fileName
        
        
        
        ####saqib changes start
        link_visitor_details_form = 'https://smart-door-trr.s3.amazonaws.com/WebPage_Vistor_Info.html?filename='+fileName+"&faceid="+faceId
        ###saqib changes end
        link_visitor_details_form = 'https://smart-door-trr.s3.amazonaws.com/WebPage_Vistor_Info.html?faceid='+faceId
        link = 'http://ownervault.s3-website-us-east-1.amazonaws.com?fileName='+fileName+"&faceId="+faceId
        print("URLs sent to Owner: ")
        sendMessageToOwner(phone_number_owner, link, link_visitor_image)
        print("sent message to owner")
    
    print("final returning")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def sendOtpToVisitor(phone_number, otp):
    
    message_visitor = "Hello, here is your one time password, "
    message_visitor += str(otp)
    message_visitor += " follow this link \n"
    message_visitor += "http://visitorvault.s3-website-us-east-1.amazonaws.com/"
    smsClient.publish(PhoneNumber="+1"+phone_number,Message=message_visitor)
    
def sendMessageToOwner(phone_number, link, image_link):
    
    message_owner = "Hello, here is the link for your visitor image, "
    message_owner += str(image_link)
    message_owner += " Give them access by adding their Phone Number & Name\ "
    message_owner += str(link)
    
    smsClient.publish(PhoneNumber="+1"+phone_number,Message=message_owner)

def store_image(stream_name, fragmentNumber,faceId, result):
    
    print("fragment ")
    print(fragmentNumber)
    
    kvs = boto3.client("kinesisvideo")
    collectionId="faces"
        # Grab the endpoint from GetDataEndpoint
    endpoint = kvs.get_data_endpoint(
        APIName="GET_HLS_STREAMING_SESSION_URL",
        StreamName=stream_name
    )['DataEndpoint']

    # # Grab the HLS Stream URL from the endpoint
    kvam = boto3.client("kinesis-video-archived-media",
                        endpoint_url=endpoint)
    url = kvam.get_hls_streaming_session_url(
        StreamName=stream_name,
        PlaybackMode="LIVE_REPLAY",
        HLSFragmentSelector={
            'FragmentSelectorType': 'SERVER_TIMESTAMP',
            'TimestampRange': {
                'StartTimestamp': result['InputInformation']['KinesisVideo']['ServerTimestamp']
            }
        }
    )['HLSStreamingSessionURL']
        
    print("capturing video")
    vcap = cv2.VideoCapture(url)
    final_key = 'frame.jpg'
    print("video captured")
    s3_client = boto3.client('s3')
    bucket = "visitorphotovault"
    while(True):
        # Capture frame-by-frame
        print("capturing frame by frame")
        ret, frame = vcap.read()

        if frame is not None:
            print("frame is not none")
            # Display the resulting frame
            vcap.set(1, int(vcap.get(cv2.CAP_PROP_FRAME_COUNT) / 2) - 1)
            print("beofre writing image")
            cv2.imwrite('/tmp/' + final_key, frame)
            #s3_client.upload_file('/tmp/' + final_key, bucket, final_key)
            print("faceid")
            #if(faceId is None):
            #    faceId=index_image(frame, collectionId,fragmentNumber)
            print("faceID")
            #print(faceId)
            #fileName= faceId+'-'+fragmentNumber+'.jpg'
            #flag = r.randint(100,999)
            fileName = fragmentNumber+ '.jpg'
            print(fileName)
            print("writing to s3")
            s3_client.upload_file(
                '/tmp/frame.jpg',
                'visitorphotovault', 
                fileName
            )
            print("written to s3")
            if(faceId is None):
                print("faceid was none")
                response =index_image(collectionId, bucket, fileName)
                faceId = response[0]['Face']['FaceId']
                fileName = response[0]['Face']['ExternalImageId']
            
            vcap.release()
            print('Image uploaded')
            break
        else:
            print("Frame is None")
            break

    # When everything done, release the capture
    vcap.release()
    print("releasinf vcap")
    cv2.destroyAllWindows()
        
    location = boto3.client('s3').get_bucket_location(
        Bucket=bucket)['LocationConstraint']
    s3ImageLink = "https://%s.s3.amazonaws.com/%s" % (
        bucket, fileName)
    print("s3ImageLink ====" + s3ImageLink)
    
    return fileName, faceId


def index_image(collection_id, bucket_name, bucket_file_name):
    print("Indexing[" + bucket_name + ":" + bucket_file_name +
          "] into collection[" + collection_id + "]")
    client = boto3.client('rekognition')
    response = client.index_faces(CollectionId=collection_id,
                                  Image={'S3Object': {
                                      'Bucket': bucket_name, 'Name': bucket_file_name}},
                                  ExternalImageId=bucket_file_name,
                                  DetectionAttributes=())

    print("Index Face Response - ")
    print(response)
    for faceRecord in response['FaceRecords']:
        print ("  FaceId : {} and ExternalImageId : {}".format(
            faceRecord['Face']['FaceId'], faceRecord['Face']['ExternalImageId']))

    if len(response['FaceRecords']) > 0:
        return response['FaceRecords']
    else:
        print("No Faces Found in image")
        return None
