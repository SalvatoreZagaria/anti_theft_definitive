import os
import time
import asyncio
import datetime
import RPi.GPIO as GPIO

from camera import take_picture
from telegram_client import send_message, send_picture

GPIO.setmode(GPIO.BCM)

pirPin1 = 26
pirPin2 = 13

GPIO.setup(pirPin1, GPIO.IN)
GPIO.setup(pirPin2, GPIO.IN)

n_pictures = 10

loop = asyncio.get_event_loop()

WORKSPACE = os.environ.get("SYSTEM_WORKSPACE", None)
if WORKSPACE is None:
    raise Exception("Workspace not defined")
MEDIA_DIR = os.path.join(WORKSPACE, "media")


def intruder_detected(pirPin):
    current_timestamp = datetime.datetime.now().strftime("%m_%d_%Y__%H_%M_%S")
    msg = "{}: {} detected an intruder!".format(current_timestamp, pirPin)
    print(msg)
    loop.run_until_complete(send_message(msg))

    for i in range(n_pictures):
        pic_name = "{}_{}.jpg".format(current_timestamp, i)
        full_image_name = os.path.join(MEDIA_DIR, pic_name)
        take_picture(full_image_name)
        time.sleep(0.5)

        # send pic on Telegram
        loop.run_until_complete(send_picture(full_image_name))


def run_pir_sensors():
    time.sleep(0.2)
    print("Pir sensors running...")

    try:
        while True:
            if GPIO.input(pirPin1):
                intruder_detected(pirPin1)
            elif GPIO.input(pirPin2):
                intruder_detected(pirPin2)
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
