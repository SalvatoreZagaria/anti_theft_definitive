from picamera import PiCamera
from time import sleep
import datetime

camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 15
camera.rotation = 180
camera.annotate_text_size = 10

# Take picture
camera.annotate_text = str(datetime.datetime.now())
camera.start_preview()
camera.capture("./image.jpg")
camera.stop_preview()

# Record video
camera.annotate_text = str(datetime.datetime.now())
camera.start_preview()
camera.start_recording("./video.h264")
sleep(5)
camera.stop_recording()
camera.stop_preview()
