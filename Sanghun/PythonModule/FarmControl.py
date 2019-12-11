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
            #서버의 주소가 들어갈 곳이다.
            data={"temper":self.dataList[0],"humid":self.dataList[2]}
            data=json.dumps(data,ensure_ascii=False ) 
            #서버에 전송할 json파일을 만든다. 
            #dataList의 0번째는 현재 온도, dataList의 2번째는 현재 습도이다.
            r=requests.post(URL,data=data)
            #서버로 request를 한다. 
            response=r.json()
            #그리고 리턴값인 r을 받는다.
            if(response["light"]):
                #만약 response의 light 가 1 이라면, 전구를 켠다. 
                FarmC.pinSet(self.pinList[1],1)#pinList[1]은 전구의 핀 번호이다.
                print(response["setTemper"],end=" ")
                print("도 (기준온도) 미만입니다")
            else:
                #만약 response의 light가 0 이라면, 전구를 끈다.
                print(response["setTemper"],end=" ")
                print("도 (기준온도) 이상입니다 ")
                FarmC.pinSet(self.pinList[1],0)   
            if(response["humid"]):
                #만약 response의 humid가 1 이라면, 가습기를 켠다. 
                FarmC.pinSet(self.pinList[2],1)#pinList[2]는 가습기의 핀 번호이다
                print(response["setHumid"],end=" ")
                print("% (기준습도) 미만입니다")
            else:
                #만약 response의 humid가 0 이라면 , 가습기를 끈다. 
                print(response["setHumid"],end=" ")
                print("% (기준습도) 이상입니다 ")
                FarmC.pinSet(self.pinList[2],0)   
            time.sleep(15) #15초에 한번 서버에 물어보고 라즈베리파이를 제어한다.

