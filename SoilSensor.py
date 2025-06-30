import RPi.GPIO as GPIO
import time

# 设置 GPIO 引脚
channel = 21 # 对应物理引脚40
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

try:
while True:
if GPIO.input(channel) == GPIO.LOW:
print("Wet")
else:
print("Dry")
time.sleep(1)
except KeyboardInterrupt:
print("Terminate")
finally:
GPIO.cleanup()
