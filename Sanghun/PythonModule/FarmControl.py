import RPi.GPIO as GPIO
import time 
import threading
import FarmC
import json
import requests
 

    



class controlThread(threading.Thread):
    def __init__(self,dataList):
        threading.Thread.__init__(self) 
        self.dataList=dataList
        
    def setInfo(self,dataList):#현재온도, 적정온도, 현재습도,적정습도
        self.dataList=dataList
        
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
                FarmC.pinSet(20,1)
                print(response["setTemper"],end=" ")
                print("도 (기준온도) 미만입니다")
            else:
                print(response["setTemper"],end=" ")
                print("도 (기준온도) 이상입니다 ")
                FarmC.pinSet(20,0)   
            time.sleep(3)
 

