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
<<<<<<< HEAD
                if(self.dataList[0]<37):
=======
                if(self.dataList[0]<36):
>>>>>>> 2903127df8e596a7c8b677fb16cd1b79a619e876
                    GPIO.setup(20,GPIO.OUT)
                    GPIO.output(20,True)
                    print("36도 미만입니다.")
                else:
                    print("36도 이상입니다.")
                    GPIO.setup(20,GPIO.OUT)
                    GPIO.output(20,False)
                    GPIO.setup(20,GPIO.IN)
                    
                    
                    
                    
<<<<<<< HEAD
                time.sleep(10)
=======
                time.sleep(3)
>>>>>>> 2903127df8e596a7c8b677fb16cd1b79a619e876
 

        

