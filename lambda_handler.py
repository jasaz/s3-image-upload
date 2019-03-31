#This lambda function is invoked by API gateway
#It gets the payload from the event of lambda_handler which contains Base64 encoded image, image name, s3 bucket_name and s3 key
#It decodes the image before uploading into S3 

import json
import base64
import boto3

def lambda_handler(event, context):
    print ("Executing Lambda function")
    data = json.loads(json.dumps(event))
    payload = json.loads(data['body'])
    encoded_image = payload['image']
    image_name = payload['image_name']
    s3_bucket_name = payload['s3_bucket_name']
    folder = payload['key']
    file_path = folder + "/" + image_name
    
    decoded_image = base64.b64decode(encoded_image)
    
    s3_client = boto3.client('s3')
    s3_client.put_object(Body = decoded_image, Bucket = s3_bucket_name, Key = file_path, ContentType = 'image/jpeg', ACL = 'bucket-owner-full-control')
    return {
    "statusCode": 200,
    "body": "Lambda executed successfully"
    }