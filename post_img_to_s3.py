# Invokes API securely by using AWS Signature version 4 to hash the secret_key and access_key
# The steps for signing AWS request can be found here: https://docs.aws.amazon.com/general/latest/gr/signing_aws_api_requests.html 

import requests
import base64
import json
import sys, os, base64, datetime, hashlib, hmac

#Add your image name here
with open("my-image.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

#Add your image name, s3 bucket name, s3 key\prefix here  
payload = {
    "image_name": "my-image.jpg",
    "s3_bucket_name" : "mybucket",
    "key": "upload_image",
    "image": encoded_string
}

# Provide your API gateway endpoint below

method = 'POST'
service = 'execute-api'
host = '8b52km67bi.execute-api.us-east-1.amazonaws.com'
region = 'us-east-1'
endpoint = 'https://8b52km67bi.execute-api.us-east-1.amazonaws.com/prod/upload-image-to-s3'
content_type = 'application/x-www-form-urlencoded'
amz_target = ''

request_parameters = json.dumps(payload)

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

# Please add the access_key and secret_key from the credentials file, DO NOT HARD CODE.
access_key = 'your_access_key'
secret_key = 'your_secret_key'

if access_key is None or secret_key is None:
    print('No access key is available.')
    sys.exit()

# Create a date for headers and the credential string
t = datetime.datetime.utcnow()
amz_date = t.strftime('%Y%m%dT%H%M%SZ')
date_stamp = t.strftime('%Y%m%d')

#Create a canonical request
canonical_uri = '/prod/upload-image-to-s3'
canonical_querystring = ''
canonical_headers = 'content-type:' + content_type + '\n' + 'host:' + host + '\n' + 'x-amz-date:' + amz_date + '\n' + 'x-amz-target:' + amz_target + '\n'

#Create the list of signed headers
signed_headers = 'content-type;host;x-amz-date;x-amz-target'
payload_hash = hashlib.sha256(request_parameters.encode('utf-8')).hexdigest()
canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

#Match the algorithm to the hashing algorithm you use SHA-256
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request'
string_to_sign = algorithm + '\n' +  amz_date + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

# Create the signing key using the function defined above
# Add signing information to the request
signing_key = getSignatureKey(secret_key, date_stamp, region, service)
signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

#Form the Headers
headers = {'Content-Type':content_type,
           'X-Amz-Date':amz_date,
           'X-Amz-Target':amz_target,
           'Authorization':authorization_header}
print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
print('Request URL = ' + endpoint)

r = requests.post(endpoint, data=request_parameters, headers=headers)
print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print(r.text)
