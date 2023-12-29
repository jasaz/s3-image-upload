# s3-image-upload

I wrote a quick code to help a friend copy images from Raspberry Pi to S3 bucket. 

Uploads image to S3 using Serverless stack - API gateway, Lambda and S3
Secures the API using AWS Signature version 4 and API gateway resouce policies

## Functions 

- *post_img_to_s3.py* - Invokes call to public API (unsecured)
- *post_image_to_s3_unsecured.py* - Invokes call to public API securely using AWS Signature version 4
- *lambda_handler.py* - Lambda function invoked by the API gateway for uploading the file to S3
- *api-gateway-resource-policy.json* - API gateway resource policy

### Credentials

Please replace the access keys below in the code.  

- ACCESS_KEY = '12345'
- SECREST_ACCESS_KEY = 'ABCDE'

 
 
