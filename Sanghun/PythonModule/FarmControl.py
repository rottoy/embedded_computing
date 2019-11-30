import RPi.GPIO as GPIO
import time
import threading



    



class controlThread(threading.Thread):
    
        flag=0
        def setInfo(self,dataList):
            self.dataList=dataList
        
        def run(self):
            
            while True:        
                print("this is control thread")
                if(self.dataList[0]<38.8):
                    GPIO.setup(20,GPIO.OUT)
                    GPIO.output(20,True)
                    print("36도 미만입니다.")
                else:
                    print("36도 이상입니다.")
                    GPIO.setup(20,GPIO.OUT)
                    GPIO.output(20,False)
                    GPIO.setup(20,GPIO.IN)
                    
                    
                    
                    
                time.sleep(3)
 

