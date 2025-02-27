import datetime

from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 15
camera.rotation = 180
camera.annotate_text_size = 10
camera.start_preview()


def take_picture(full_image_name):
    current_time = datetime.datetime.now()
    camera.annotate_text = current_time.strftime("%m/%d/%Y, %H:%M:%S")

    camera.capture(full_image_name)


def stop_preview():
    camera.stop_preview()


# Record video
# camera.annotate_text = str(datetime.datetime.now())
# camera.start_preview()
# camera.start_recording("./video.h264")
# time.sleep(5)
# camera.stop_recording()
# camera.stop_preview()
