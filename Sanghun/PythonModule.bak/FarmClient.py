import flask
import requests
import json
import threading

class farmClient(threading.Thread):
    def setInfo(self,dataList):
        self.dataList=dataList # 혀재온도, 설정온도, 현재습도, 설정습도
    def run(self):
        URL = "http://127.0.0.1:4321/thermoReport"
        data={"temper":dataList[0], "humid" : dataList[2]}
        print(data)
        reponse=requests.post(URL,data=data)
        print(r.text)
        
if(__name__=="__main__


data = {"temper":"36", "humid":"70"}
data=json.dumps(data,ensure_ascii=False)
print(data)
print(type(data))
r=requests.post(URL,data=data)

print(r.status_code)
print(r.text)


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
