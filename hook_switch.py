import RPi.GPIO as GPIO

def button_callback(channel):
    print("Button was pushed")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

hang_up = False

while hang_up == False:
    GPIO.wait_for_edge(11,GPIO.RISING)
    hang_up = True
    message = input("Hook down. Hangup Signal.")

GPIO.cleanup()
