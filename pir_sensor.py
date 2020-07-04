import os
import time
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

WORKSPACE = os.environ.get("SYSTEM_WORKSPACE", None)
if WORKSPACE is None:
    raise Exception("Workspace not defined")
MEDIA_DIR = os.path.join(WORKSPACE, "media")


def intruder_detected(pirPin):
    current_timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    msg = "{}: {} detected an intruder!".format(current_timestamp, pirPin)
    print(msg)
    send_message(msg)

    for i in range(n_pictures):
        pic_name = "{}_{}.jpg".format(current_timestamp, i)
        full_image_name = os.path.join(MEDIA_DIR, pic_name)
        take_picture(full_image_name)
        time.sleep(0.5)

        # send pic on Telegram
        send_picture(full_image_name)


def run_pir_sensors():
    time.sleep(0.2)
    print("Pir sensors running...")
    try:
        GPIO.add_event_detect(pirPin1, GPIO.RISING, callback=intruder_detected)
        GPIO.add_event_detect(pirPin2, GPIO.RISING, callback=intruder_detected)
        while True:
            time.sleep(0.3)
    except KeyboardInterrupt:
        GPIO.cleanup()
