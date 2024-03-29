import Measuring
import FarmServer
import FarmControl
import time
import RPi.GPIO as GPIO


dataList=[0,17.0] #  현재 온도, 적정온도이다. 일단은.
def measure():
    #measure쓰레드를 실행시킨다. 
    t=Measuring.measureThread()
    t.setInfo(dataList)
    t.start()
    print("measure start")
    time.sleep(5)

def control():
    t=FarmControl.controlThread()
    t.setInfo(dataList)
    t.start()
    print("control start")
    time.sleep(3)
    ##컨트롤 쓰레드를 실행시킨다. 
    #하는일은 원래는 서버로부터 값을 받아 실행시키는거지만,
    #일단은 내가 직접 준다음에 그걸로 해보자.

def setup(thermoPin,lightPin):
    GPIO.setmode(GPIO.BCM)
    setupThermoPin(thermoPin)
    setupLightPin(lightPin)
    
def setupThermoPin(pin):
    print("this is setupTHermoPin method")
    GPIO.setup(pin,GPIO.OUT)

def setupLightPin(pin):
    GPIO.setup(pin,GPIO.OUT)

def main():
    setup(21,20)
    measure()
    control()

   
    
if(__name__=="__main__"):
    main()
    