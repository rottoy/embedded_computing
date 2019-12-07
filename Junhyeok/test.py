# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 13:41:10 2019

@author: 임준혁
"""

import sys
import time
import threading
import requests
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QtWebEngineWidgets
from PyQt5.uic import loadUi

ui = 0
tempAutoMode = True
humidAutoMode = True
class MyWindow(QDialog):
   
    def __init__(self):
        super().__init__()
        self.ui=loadUi('./farmui.ui',self)
        #pushbutton_3,4,5,6
        #lcdNumber,lcdNumber_2,3,4
        #pushbutton,pushbutton_2
        #label_11 :streaming
        #labe_10 : camera
        
        self.pushButton_3.clicked.connect(self.tempUp)
        self.pushButton_4.clicked.connect(self.tempDown)
        self.pushButton_5.clicked.connect(self.humidUp)
        self.pushButton_6.clicked.connect(self.humidDown)
        self.pushButton.clicked.connect(self.tempAutoOrOff)
        self.pushButton_2.clicked.connect(self.humidAutoOrOff)
        self.t=controlThread()
        self.t.start()
        global ui
        ui = self.ui
    def tempUp(self):
        x=self.lcdNumber_3.intValue()
        self.lcdNumber_3.display(x+1)
    def humidUp(self):
        x=self.lcdNumber_4.intValue()
        self.lcdNumber_4.display(x+1)
    def tempDown(self):
        x=self.lcdNumber_3.intValue()
        if x > 0:
            self.lcdNumber_3.display(x-1)
    def humidDown(self):
        x=self.lcdNumber_4.intValue()
        if x> 0:            
            self.lcdNumber_4.display(x-1)
    def tempAutoOrOff(self): # Auto면 센서 on off 자동으로 판단, Off면 센서 무조건 차단. 이건 ui만 터치하므로 쓰레드에서 직접 끄는작업해야됨.
        global tempAutoMode
        tempAutoMode = not tempAutoMode
        if tempAutoMode==False:
            self.pushButton.setText("Off")
        else:
            self.pushButton.setText("Auto")
    def humidAutoOrOff(self): # Auto면 센서 on off 자동으로 판단, Off면 센서 무조건 차단. 이건 ui만 터치하므로 쓰레드에서 직접 끄는작업해야됨.
        global humidAutoMode
        humidAutoMode = not humidAutoMode
        if humidAutoMode==False:
            self.pushButton_2.setText("Off")
        else:
            self.pushButton_2.setText("Auto")
class controlThread(threading.Thread):
    global tempAutoMode
    global humidAutoMode
    def __init__(self):
        threading.Thread.__init__(self) 
        self.temparature =0
        self.humidity=0
        self.isTempSensorOn=False
        self.isHumidSensorOn=False
        
        
    def run(self):
        global ui
        
        data = {}
        data2= {}
        while True:
            URL = "http://211.184.247.88:2224/getTH"
            r=requests.get(URL,data=data)
            data=r.json()
            self.temparature=data['humidity']
            self.humidity=data['temparature']
            ui.lcdNumber.display(self.temparature)
            ui.lcdNumber_2.display(self.humidity)
            URL2 = "http://211.184.247.88:2224/getStatusTH"
            r2=requests.get(URL2,data=data2)
            data2=r2.json()
            self.isTempSensorOn=data2['isTemp']
            self.isHumidSensorOn=data2['isHumid']
            if tempAutoMode==True:
                ui.label_3.setText("status : "+str(self.isTempSensorOn))
            if humidAutoMode==True:
                ui.label_4.setText("status : "+str(self.isHumidSensorOn))
            
            
            #print(str(self.temparature)+" "+str(self.humidity))
            
            
            time.sleep(3)
            
if __name__=="__main__":
    app= QApplication(sys.argv)
    mywindow=MyWindow()
    mywindow.show()
    sys.exit(app.exec_())
