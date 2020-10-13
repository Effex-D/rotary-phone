import RPi.GPIO as GPIO
import datetime

count = 0

def add_one(channel):
    global count
    count = count + 1

def end_count(channel):
    global count
    if count == 0:
        print("Switch opened (IE: You are dialing something)")
    elif count == 10:
        print("You dialed: 0")
    else:
        print("You dialed: {}".format(count))
    count = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(15,GPIO.RISING,callback=add_one, bouncetime=75)
GPIO.add_event_detect(13,GPIO.BOTH,callback=end_count, bouncetime=200)

message = input("Press something to quit\n")

GPIO.cleanup()
