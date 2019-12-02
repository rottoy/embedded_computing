import RPi.GPIO as GPIO
import time
import threading
import FarmC



    



class controlThread(threading.Thread):
    
        flag=0
        def setInfo(self,dataList):
            self.dataList=dataList
        
        def run(self):
            
            while True:        
                print("this is control thread")
                if(self.dataList[0]<38):
                    
                    FarmC.pinSet(20,1)
                    print("36도 미만입니다.")
                else:
                    print("36도 이상입니다.")
                    FarmC.pinSet(20,0)
                    
                    
                    
                    
                time.sleep(3)
 

