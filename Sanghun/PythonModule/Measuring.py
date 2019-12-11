import threading
import RPi.GPIO as GPIO
import dht11
import time
import datetime

class measureThread(threading.Thread):
    
    def __init__(self,dataList,pinList):
        threading.Thread.__init__(self) 
        self.dataList=dataList
        self.pinList=pinList
        
    def run(self):

        GPIO.setwarnings(False)    
        instance = dht11.DHT11(self.pinList[0]) #dht11
        while True:
            instance = dht11.DHT11(self.pinList[0]) #dht11
            result = instance.read()
            if result.is_valid():
                print("Last valid input: " + str(datetime.datetime.now()))
                print("Temperature: %d C" % result.temperature)
                print("Humidity: %d %%" % result.humidity)
                self.dataList[0]=result.temperature 
                self.dataList[2]=result.humidity
                #실습때 배운 DHT11의 이용하여 
                #온,습도를 측정한 후 전역변수인 리스트에 현재 온도,습도를 대입했다.
            time.sleep(3)

        


# initialize GPIO


# read data using pin 21


