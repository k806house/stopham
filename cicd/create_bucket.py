import os

import boto3


s3 = boto3.resource(service_name='s3',
    aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
    endpoint_url='https://obs.ru-moscow-1.hc.sbercloud.ru',
    use_ssl=False,
    verify=False,    
)
#for bucket in s3.buckets.all():
#    print(bucket.name)

my_bucket = s3.Bucket('hackathon-ecs-4')
for my_bucket_object in my_bucket.objects.all():
    print(my_bucket_object)
