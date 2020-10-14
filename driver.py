import RPi.GPIO as GPIO
import datetime
class rotaryDriver():
    def __init__(self, mode="driver"):
        self.count = 0
        self.mode = mode
        self.hook_status = "down"
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(15, GPIO.RISING, callback=self.add_one, bouncetime=75)
        GPIO.add_event_detect(13, GPIO.BOTH, callback=self.end_count, bouncetime=200)
        GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(11, GPIO.BOTH, callback=self.button_callback)
        message = input("Press enter to quit\n\n")
        GPIO.cleanup()  # Clean up

    def add_one(self, channel):
        self.count = self.count + 1

    def end_count(self, channel):
        if self.count == 0:
            self.inform("dial", "open")
        elif self.count == 10:
            self.inform("rotary", "0")
        else:
            self.inform("rotary", self.count)
        self.count = 0

    def button_callback(self, channel):
        if GPIO.input(11):
            self.hook_status = "down"
            self.inform("hook", "down")
        else:
            self.hook_status = "up"
            self.inform("hook", "up")

    def inform(self, switch, event):
        if self.mode == "testing":
            print("Action detected: {} - {}".format(switch, event))
        elif self.mode == "driver":
            print("EVENT: SWITCH: {} - ACTION: {} - HOOK_STATUS: {}".format(switch, event, self.hook_status))


if __name__ == "__main__":
    tester = rotaryDriver()
