import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pirPin1 = 26
pirPin2 = 13

GPIO.setup(pirPin1, GPIO.IN)
GPIO.setup(pirPin2, GPIO.IN)


def intruder_detected(pirPin):
    print("{} detected an intruder!".format(pirPin))


if __name__ == "__main__":
    time.sleep(0.2)
    print("Running...")
    try:
        GPIO.add_event_detect(pirPin1, GPIO.RISING, callback=intruder_detected)
        GPIO.add_event_detect(pirPin2, GPIO.RISING, callback=intruder_detected)
        while True:
            time.sleep(0.3)
    except KeyboardInterrupt:
        print("Quit")
        GPIO.cleanup()
