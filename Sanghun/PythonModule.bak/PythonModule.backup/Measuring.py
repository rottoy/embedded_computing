import threading
import RPi.GPIO as GPIO
import dht11
import time
import datetime

class measureThread(threading.Thread):
    
        def setInfo(self,dataList):
            self.dataList=dataList
            
        def run(self):
            print('설정온도는', end=" " )           
            
            print(self.dataList[1], end=" " )
            print("입니다")
            GPIO.setwarnings(False)
            
  
            
            instance = dht11.DHT11(pin=21) #dht11의 DHT11가 뭔진모르겠지만 21번핀으로 온습도 체크할게
            while True:
                instance = dht11.DHT11(pin=21) #dht11의 DHT11가 뭔진모르겠지만 21번핀으로 온습도 체크할게
                result = instance.read()
                if result.is_valid():
                    print("Last valid input: " + str(datetime.datetime.now()))
                    print("Temperature: %d C" % result.temperature)
                    print("Humidity: %d %%" % result.humidity)
                    #여기서 현재 온도를 넘겨준다.
                    self.dataList[0]=result.temperature 
                time.sleep(3)

        


# initialize GPIO


# read data using pin 21


