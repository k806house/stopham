import os


class DevConfig:
    DEBUG = True
    S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
    S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
    S3_URL = 'https://obs.ru-moscow-1.hc.sbercloud.ru'
    S3_BUCKET = 'hackathon-ecs-4'
