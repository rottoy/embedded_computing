import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)
print("setup")
time.sleep(2)

GPIO.output(21,True)
time.sleep(1000)
GPIO.output(21,False)

GPIO.cleanup()
print("end")
