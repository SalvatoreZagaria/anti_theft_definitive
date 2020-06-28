import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pirPin = 26

GPIO.setup(pirPin, GPIO.IN)


def intruder_detected(*args):
    print("Intruder detected!")


if __name__ == "__main__":
    time.sleep(0.2)
    print("Running...")
    try:
        GPIO.add_event_detect(pirPin, GPIO.RISING, callback=intruder_detected)
        while True:
            time.sleep(0.3)
    except KeyboardInterrupt:
        print("Quit")
        GPIO.cleanup()
