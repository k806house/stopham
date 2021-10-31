import os
import sys

import boto3
import botocore

from flask import current_app
from urllib.parse import urlparse

BOTO_CONFIG = botocore.config.Config(retries={"max_attempts": 5, "mode": "standard"})


def _ensure_s3_bucket_for_file(s3, bucket, dirname):
    bucket = s3.Bucket(bucket)
    bucket.objects.filter(Prefix=f"{dirname}/").delete()


def _delete_obj_if_exists(s3, bucket, key):
    s3.Object(bucket, key).delete()


def _download_obj_if_exists(s3, bucket, key):
    return s3.Object(bucket, key).get()


def _upload_file_by_exts_impl(client, bucket, s3_folder, dir, exts):
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            file = os.path.join(root, name)
            short_filename = file[len(dir) + 1 :]
            _, file_extension = os.path.splitext(file)
            if file_extension in exts:
                client.upload_file(file, bucket, os.path.join(s3_folder, short_filename))


def _get_s3():
    boto3_params = {
        "service_name": "s3",
        "aws_access_key_id": current_app.config["S3_ACCESS_KEY"],
        "aws_secret_access_key": current_app.config["S3_SECRET_KEY"],
        "endpoint_url": current_app.config["S3_URL"],
        "use_ssl": False,
        "verify": False,
        "config": BOTO_CONFIG,
    }

    s3_client = boto3.client(**boto3_params)
    s3 = boto3.resource(**boto3_params)
    return s3_client, s3


def upload_files_by_exts(dir, bucket, s3_folder, exts):
    s3_client, s3 = _get_s3()
    _ensure_s3_bucket_for_file(s3, bucket, s3_folder)
    _upload_file_by_exts_impl(s3_client, bucket, s3_folder, dir, exts)


def upload_file_by_name(filename, bucket, s3_folder, s3_filename):
    s3_client, s3 = _get_s3()
    s3_client.upload_file(filename, bucket, os.path.join(s3_folder, s3_filename))


def download_file_by_name(s3_link):
    parsed = urlparse(s3_link)
    s3_url = f"{parsed.scheme}://{parsed.hostname}"
    splited_path = parsed.path.lstrip("/").split("/", 1)
    bucket, key = splited_path
    s3_client, s3 = _get_s3()
    obj = _download_obj_if_exists(s3, bucket, key)
    return obj['Body'].read().decode('utf-8')


def delete_file_by_name(s3_link):
    parsed = urlparse(s3_link)
    s3_url = f"{parsed.scheme}://{parsed.hostname}"
    splited_path = parsed.path.lstrip("/").split("/", 1)
    bucket, key = splited_path
    s3_client, s3 = _get_s3()
    _delete_obj_if_exists(s3, bucket, key)
