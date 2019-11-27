from ctypes import *
import os
import sys


pin=0
order=""
intOrder=0
def setup():
    global pin
    global order
    global intOrder
    pin=(int)(sys.argv[1])
    order=sys.argv[2]
    if(order=="On"or order=="ON"or order =="on"):
        intOrder=1
    else:
        intOrder=0
def ledCtl():
    global pin
    global order
    global intOrder
    
    dirPath=os.path.dirname(os.path.realpath(__file__))
    dirPath = os.path.join(dirPath,'ledModule.so')
    
    Clib=cdll.LoadLibrary(dirPath)
    print (pin)
    print (intOrder)
    Clib.ledControl(pin,intOrder)
       
if __name__=='__main__':
    setup()
    ledCtl()
