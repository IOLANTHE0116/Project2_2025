import RPi.GPIO as GPIO
import time

# Set the GPIO pins
channel = 21 # Corresponds to physical pin 40
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

try:
while True:
if GPIO.input(channel) == GPIO.LOW:
print("Soil test results: Wet")
else:
print("Soil test results: dry")
time.sleep(1)
except KeyboardInterrupt:
print("Terminate")
finally:
GPIO.cleanup()
