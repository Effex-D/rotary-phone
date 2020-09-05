import RPi.GPIO as GPIO  
import math, sys, os
import subprocess
import socket

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

c=0
last = 1

def count(pin):
    global c 
    c = c + 1

GPIO.add_event_detect(15, GPIO.BOTH)

while True:
    try:
        if GPIO.event_detected(13):
            current = GPIO.input(13)
            if(last != current):
                if(current == 0):
                    GPIO.add_event_detect(15, GPIO.BOTH, callback=count, bouncetime=15)
                else:
                    GPIO.remove_event_detect(15)
                    number = int((c-1)/2)
		                       
                    print ("You dial", number)

                    c= 0                 
                    
                    
                last = GPIO.input(13)
    except KeyboardInterrupt:
        break
