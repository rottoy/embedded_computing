import Measuring
import FarmServer
import FarmControl
import time
import FarmC
import RPi.GPIO as GPIO


dataList=[0,38.0,0,75] #  현재 온도, 적정온도이다. 일단은. 네트워크에서 받아와서 적정온도는 채울 것이다.
#뒤에두개는 현재습도 적정습도이다.
def measure():
    #measure쓰레드를 실행시킨다. 
    global dataList
    t=Measuring.measureThread()
    t.setInfo(dataList)
    t.start()
    print("measure start")
    time.sleep(5)

def control():
    global dataList
    t=FarmControl.controlThread(dataList)
    #t.setInfo(dataList)
    t.start()
    print("control start")
    time.sleep(3)
    ##컨트롤 쓰레드를 실행시킨다. 
    #하는일은 원래는 서버로부터 값을 받아 실행시키는거지만,
    #일단은 내가 직접 준다음에 그걸로 해보자.

def setup(thermoPin,lightPin,humidPin):
    GPIO.setmode(GPIO.BCM)
    setupThermoPin(thermoPin)
    setupLightPin(lightPin)
    setupHumid(humidPin)
    
def setupThermoPin(pin):
    print("this is setupTHermoPin method")
    GPIO.setup(pin,GPIO.OUT)

def setupLightPin(pin):
    GPIO.setup(pin,GPIO.OUT)

def setupHumid(pin):
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,True)

def main():
    setup(21,20,16)
    measure()
    control()

   
    
if(__name__=="__main__"):
    main()
    
