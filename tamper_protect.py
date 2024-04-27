#experimental generated snippet to auto wipe a pi if its picked up use at your own risk
#Assumes sensor plugged into gpio https://www.newark.com/mcm/83-17988/tilt-sensor-for-arduinoraspberry/dp/33AC0093

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(21)
    if input_state == False:
        print('Tilt detected! Wiping data...')
        
        # Securely wipe the SD card
        os.system('sudo shred -v -n1 /dev/mmcblk0')
        
        print('Data wipe complete. Shutting down...')
        
        # Shut down the Raspberry Pi
        os.system('sudo shutdown -h now')
        
        break
        
    time.sleep(0.2)
