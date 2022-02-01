import os
import time

import boto3
from config import ACCESS_KEY, BUCKET, SECRET_KEY

client = boto3.client(
    "s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
)


def upload_picture(user_id, picture, pic_id):
    """Uploads image to the s3 bucket"""
    client.upload_file(picture, BUCKET, f"{user_id}/pictures/{pic_id}.jpg")


def upload_gif(user_id, gif):
    """Uploads gif to the s3 bucket in the common folder"""
    timestr = time.strftime("%Y%m%d-%H%M%S")
    client.upload_file(gif, BUCKET, "GIF/" f"{user_id}-{timestr}.gif")


def upload_private_gif(user_id, gif):
    """Uploads gif to the s3 bucket in private folder"""
    timestr = time.strftime("%Y%m%d-%H%M%S")
    client.upload_file(gif, BUCKET, f"{user_id}/gifs/{timestr}.gif")


def download_all_gifs():
    """Downloads all gifs from the s3 bucket"""
    gif_list = client.list_objects_v2(Bucket=BUCKET, Prefix="GIF")["Contents"]
    gifs = []
    for gif in gif_list:
        file_name = os.path.basename(gif["Key"])
        gifs.append(file_name)
        client.download_file(BUCKET, gif["Key"], file_name)
    return gifs


def download_users_gifs(user_id):
    """Downloads gifs for particular user from the s3 bucket"""
    try:
        gif_list = client.list_objects_v2(
            Bucket=BUCKET, Prefix="GIF/"f"{user_id}")[
            "Contents"
        ]
    except KeyError:
        gif_list = []

    try:
        private_gif_list = client.list_objects_v2(
            Bucket=BUCKET, Prefix=f"{user_id}/gifs/"
        )["Contents"]
    except KeyError:
        private_gif_list = []
    total = gif_list + private_gif_list

    gifs = []
    if total:
        for gif in total:
            file_name = os.path.basename(gif["Key"])
            gifs.append(file_name)
            client.download_file(BUCKET, gif["Key"], file_name)
    return gifs
