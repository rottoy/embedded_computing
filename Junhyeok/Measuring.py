import threading
import RPi.GPIO as GPIO
import dht11
import time
import datetime

class measureThread(threading.Thread):
        def __init__(self, args):

            threading.Thread.__init__(self)
            self.args = args
        def run(self):
            #print(self.args[0])
            #print(self.args[1])
            
            print('hello')
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.cleanup() #여기까지 GPIO를 셋 하고
            instance = dht11.DHT11(pin=21) #dht11의 DHT11가 뭔진모르겠지만 21번핀으로 온습도 체크할게
            """
            while True:
                result = instance.read()
                if result.is_valid():
                    print("Last valid input: " + str(datetime.datetime.now()))
                    print("Temperature: %d C" % result.temperature)
                    print("Humidity: %d %%" % result.humidity)
                time.sleep(1)
            """
            self.args[0]= 75 #온도 여기다 result.temperature 주시면 됩니다. 지금은 오류나서
            self.args[1]= 85 #습도 여기다 result.humidity 주시면 됩니다. 지금은 오류나서

# initialize GPIO


# read data using pin 21


