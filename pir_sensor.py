import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pirPin = 3

GPIO.setup(pirPin, GPIO.IN)

while True:
    i=GPIO.input(pirPin)
    if i==0:
        print("No intruders")
    elif i==1:
        print("Intruders")
    time.sleep(0.2)

