import RPi.GPIO as GPIO
import time 
import threading
import FarmC
import json
import requests
 
class controlThread(threading.Thread):
    def __init__(self,dataList,pinList):
        threading.Thread.__init__(self) 
        self.dataList=dataList
        self.pinList=pinList
        
    def run(self):
        while True:        
            URL="http://172.30.1.55:4321/thermoReport"
            data={"temper":self.dataList[0],"humid":self.dataList[2]}
            data=json.dumps(data,ensure_ascii=False ) 
            print(data)
            r=requests.post(URL,data=data)
            response=r.json()
            print("this is control thread")
            if(response["light"]):
                FarmC.pinSet(pinList[1],1)
                print(response["setTemper"],end=" ")
                print("도 (기준온도) 미만입니다")
            else:
                print(response["setTemper"],end=" ")
                print("도 (기준온도) 이상입니다 ")
                FarmC.pinSet(pinList[1],0)   
            if(response["humid"]):
                FarmC.pinSet(pinList[2],1)
                print(response["setHumid"],end=" ")
                print("% (기준습도) 미만입니다")
            else:
                print(response["setHumid"],end=" ")
                print("% (기준습도) 이상입니다 ")
                FarmC.pinSet(pinList[2],0)   
            time.sleep(3)
 

