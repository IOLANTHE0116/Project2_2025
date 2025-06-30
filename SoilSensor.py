import RPi.GPIO as GPIO
import time
#GPIO SETUP
channel =4
GPI0.setmode(GPIO.BCM)
GPI0.setup(channel,GPIO.IN)
def callback(channel):
  if GPIo.input(channel):
    print("water Detected!")
else:
    print("water Detected!")
GPIO.add event detect(channel, GpIO.BoTH, bouncetime=300)# let us know when the pin goes HIGH Or LOW
GPIO.add event callback(channel, callback)# assign function to GPlo PIN, Run function on change
# infinite loopwhile True:
time.sleep(0)
