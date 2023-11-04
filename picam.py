# Desc: This file is used to upload snapshots with the Raspberry Pi camera to Prusa Connect.

import requests
import os
import time
import logging
import ffmpeg

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# add the handlers to logger
logger.addHandler(ch)

# ENV variables
DELAY_SECONDS = 10
HTTP_URL = os.environ['HTTP_URL']
STREAM_URL = os.environ['STREAM_URL']
FINGERPRINT = os.environ['FINGERPRINT']
TOKEN = os.environ['TOKEN']
OUTPUT_FILE = 'image.jpg'

def take_snapshot():
    ### Take snapshot with Raspberry Pi camera
    logger.info('Taking snapshot...')
    stream = ffmpeg.input(STREAM_URL, format='v4l2')
    stream = ffmpeg.output(stream, OUTPUT_FILE,
                           vframes=1,
                           format='image2',
                           pix_fmt='yuvj420p')
    ffmpeg.run(stream, overwrite_output=True)


def upload_snapshot():
    ### Upload snapshot to Prusa Connect

    # Create request to HTTP_URL with content-type image/jpg 
    # and fingerprint and token with a data binary
    logger.info('Reading snapshot...')
    with open('image.jpg', 'rb') as f:
        data = f.read()

    headers = {
        'content-type': 'image/jpg',
        'token': TOKEN,
        'fingerprint': FINGERPRINT
        }
    logger.info('Uploading snapshot...')
    r = requests.put(HTTP_URL, data=data, headers=headers)
        
    # Check if request was successful
    if r.status_code == 204:
        logger.info('Snapshot uploaded successfully.')
    else:
        logger.error('Snapshot upload failed.')
        logger.error(r.status_code)
        logger.error(r.text)


def main():
    while True:
        take_snapshot()
        upload_snapshot()
        time.sleep(DELAY_SECONDS)


if __name__ == '__main__':
    main()