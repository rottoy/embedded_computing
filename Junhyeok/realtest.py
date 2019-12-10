import time
import picamera
camera = picamera.PiCamera()
camera.resolution = (800, 600)
camera.capture('ex1.jpg')
time.sleep(2)
camera.close()