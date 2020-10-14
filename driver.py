import RPi.GPIO as GPIO
import datetime
import json

class rotaryDriver():
    """
    rotaryDriver is designed to connect a physical rotary phone systems to raspberry pi.

    The hook switch should be connected to GPIO11.
    The rotary dial itself should have 4 wires coming off it. Two identify when the rotary is open (IE, when you
    are dialling a number.) This should be connected to GPIO13.
    The other two wires pulse once for each number it passes when dialling. These need to be connected to GPIO15.


    """

    def __init__(self, mode="driver"):
        """
        The init method sets up required values and also runs the main program loop. This is not a good way to handle
        the main loop.

        :param mode: accepts either "driver" or "testing" strings. Testing gives a more human readable output that
        prints to the screen.
        """
        self.count = 0
        self.mode = mode
        self.hook_status = "down"
        self.dial_status = "closed"
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(15, GPIO.RISING, callback=self.add_one, bouncetime=75)
        GPIO.add_event_detect(13, GPIO.BOTH, callback=self.end_count, bouncetime=200)
        GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(11, GPIO.BOTH, callback=self.hook_callback)
        message = input("Press enter to quit\n\n")
        GPIO.cleanup()  # Clean up

    def add_one(self, channel):
        """
        add_one is used by the main loop to count the pulses on the rotary dial. Added as a function because GPIO event
        detection needs a function to call. I think?

        :param channel: I think this is required by the GPIO event, but doesn't actually do anything.
        """
        self.count = self.count + 1

    def end_count(self, channel):
        """
        This waits for a switch event on pin 13 (dial opening/closing) and ends the count based on that.

        :param channel: Required by event definition, but unused.
        """
        if GPIO.input(13):
            self.dial_status = "open"
            self.inform("dial", "open")
        else:
            self.dial_status = "closed"
            self.inform("dial", "closed")
            if self.count == 0:
                catch_0 = True # Little work around to nullify the 0 count from a closed dial. Not sure if required.
            elif self.count == 10:
                self.inform("rotary", "0")
            else:
                self.inform("rotary", self.count)
            self.count = 0

    def hook_callback(self, channel):
        """
        Function to wait for the callback from the hook switch. Checks which switch action (rise/fall) is happening and
        sets the hook_status for each. Then calls the inform system.

        :param channel: Required, but not used.
        """
        if GPIO.input(11):
            self.hook_status = "down"
            self.inform("hook", "down")
        else:
            self.hook_status = "up"
            self.inform("hook", "up")

    def inform(self, switch, action):
        """
        Inform is the main writing section of the driver. While in testing mode (self.mode == "testing") it simply
        prints the information that it receives. If the mode is the default of driver, it creates a JSON from the event
        and
        PERFORMS INCORRECT ACTIONS. I don't really know how to output this to have it run as an actual driver, yet.
        I'll think about it.

        :param switch: Receives the switch that has been the target of the interaction. Either hook, dial, or rotary.
        :param action: Receives an action. For hook, either "up" or "down". For dial, "open" or "closed. For rotary,
        a number between 0 and 9.
        """
        if self.mode == "testing":
            print("Action detected: {} - {}".format(switch, action))
        elif self.mode == "driver":
            event = {"switch": switch,
                     "action": action,
                     "hook_status": self.hook_status,
                     "dial_status": self.dial_status}
            print("EVENT: SWITCH: {} - ACTION: {} - HOOK_STATUS: {} - DIAL_STATUS - {}".format(event["switch"],
                                                                            event["action"],
                                                                            event["hook_status"],
                                                                            event["dial_status"]))

if __name__ == "__main__":
    tester = rotaryDriver()
