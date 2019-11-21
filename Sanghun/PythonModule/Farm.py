import Measuring
import FarmServer
import FarmControl



def measure():
    t=Measuring.measureThread()
    t.start()
    print("measure start")
    
def main():
    measure()
    
if(__name__=="__main__"):
    main()
    