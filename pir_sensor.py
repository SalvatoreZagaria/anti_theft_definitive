import os
import time
import zipfile
import asyncio
import datetime
import RPi.GPIO as GPIO

from camera import take_picture
from telegram_client import send_message
from drive_client import upload_file

GPIO.setmode(GPIO.BCM)

pirPin1 = 26
pirPin2 = 13

GPIO.setup(pirPin1, GPIO.IN)
GPIO.setup(pirPin2, GPIO.IN)

n_pictures = 100

loop = asyncio.get_event_loop()

WORKSPACE = os.environ.get("SYSTEM_WORKSPACE", None)
if WORKSPACE is None:
    raise Exception("Workspace not defined")
MEDIA_DIR = os.path.join(WORKSPACE, "media")


def create_zip_file(zip_file_name, files):
    zf = zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED)
    for f in files:
        zf.write(f)
    zf.close()


def intruder_detected():
    current_timestamp = datetime.datetime.now().strftime("%m_%d_%Y__%H_%M_%S")
    msg = "{}: intruder detected!".format(current_timestamp)
    print(msg)
    loop.run_until_complete(send_message(msg))

    tmp_pics_list = []
    for i in range(n_pictures):
        pic_name = "{}_{}.jpg".format(current_timestamp, i)
        full_image_name = os.path.join(MEDIA_DIR, pic_name)
        take_picture(full_image_name)
        tmp_pics_list.append(full_image_name)

        if len(tmp_pics_list) == 5:
            base_name, _ = os.path.splitext(tmp_pics_list[0])
            zip_file = "{}.zip".format(base_name)

            create_zip_file(zip_file, tmp_pics_list)
            upload_file(zip_file)
            tmp_pics_list = []

        # send pic on Telegram
        # loop.run_until_complete(send_picture(full_image_name))

        # send pic on Drive
        # upload_file(full_image_name)


def clear_GPIO():
    GPIO.cleanup()


def run_pir_sensors():
    time.sleep(0.2)
    print("Pir sensors running...")

    try:
        while True:
            if GPIO.input(pirPin1) or GPIO.input(pirPin2):
                intruder_detected()
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
