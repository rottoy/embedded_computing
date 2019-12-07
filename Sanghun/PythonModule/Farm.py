import Measuring
import FarmServer
import FarmControl
import time
import FarmC
import sys
import RPi.GPIO as GPIO


dataList=[0,0.0,0,0] #  현재온도, 적정온도, 현.습, 적.습 이다. 일단은. 네트워크에서 받아와서 적정온도는 채울 것이다.
pinList=[0,0,0] #순서대로 온습도계 온도계 습도계이다. 
#뒤에두개는 현재습도 적정습도이다.
def measure():
    #measure쓰레드를 실행시킨다. 
    global dataList
    global pinList
    t=Measuring.measureThread(dataList,pinList)
    t.start()
    print("measure start")
    time.sleep(5)

def control():
    global dataList
    global pinList
    t=FarmControl.controlThread(dataList,pinList)
    t.start()
    print("control start")
    time.sleep(5)
    ##컨트롤 쓰레드를 실행시킨다. 
    #하는일은 원래는 서버로부터 값을 받아 실행시키는거지만,
    #일단은 내가 직접 준다음에 그걸로 해보자.

def setup(thermoPin,lightPin,humidPin): #순서대로 온습도계, 전구, 가습기이다. 
    global pinList
    pinList=thermoPin,lightPin,humidPin
    GPIO.setmode(GPIO.BCM)
    setupThermoPin(pinList[0])
    setupLightPin(pinList[1])
    setupHumid(pinList[2])
    
def setupThermoPin(pin):
    print("this is setupTHermoPin method")
    GPIO.setup(pin,GPIO.OUT)

def setupLightPin(pin):
    GPIO.setup(pin,GPIO.OUT)

def setupHumid(pin):
    GPIO.setup(pin,GPIO.OUT)
    

def main(): #순서대로 온습도계, 전구, 가습기의 핀 번호를 받습니다 .
    setup((int)sys.argv[1],(int)sys.argv[2],(int)sys.argv[3])
    measure()
    control()

   
    
if(__name__=="__main__"):
    main()
    
