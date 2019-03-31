#Posts image to S3 without any authentication enabled.
#The image is Base64 encoded before POST request is called


import requests
import base64
import json

#Add image name, s3 bucket name and  key
with open("MyImage.jpg ", "rb") as image_file:
    		encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
payload = {
    			"image_name": "my-image.jpg",
    			"s3_bucket_name" : "mybucket",
    			"key": "upload_image",
    			"image": encoded_string
}
# Provide your endpoint name below
r = requests.post('https://8b52km67bi.execute-api.us-east-1.amazonaws.com/prod/upload-image-to-s3', json.dumps(payload))
print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print(r.text)
