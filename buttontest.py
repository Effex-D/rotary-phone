import RPi.GPIO as GPIO
import datetime
def button_callback(channel):
    print("Connected" + datetime.datetime.now().strftime("%H%M%S"))

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(13,GPIO.RISING,callback=button_callback)

message = input("Press something to quit")

GPIO.cleanup()
