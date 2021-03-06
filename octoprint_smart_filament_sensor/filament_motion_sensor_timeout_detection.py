import RPi.GPIO as GPIO
import threading
import time

class FilamentMotionSensorTimeoutDetection(threading.Thread):
    used_pin = -1
    max_not_moving_time = -1
    lastMotion = 0
    keepRunning = True

    # Initialize FilamentMotionSensor
    def __init__(self, threadID, threadName, pUsedPin, pMaxNotMovingTime, pLogger, pCallback=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = threadName
        self.callback = pCallback
        self._logger = pLogger

        self.used_pin = pUsedPin
        self.max_not_moving_time = pMaxNotMovingTime
        self.lastMotion = time.time()
        self.keepRunning = True

        # Remove event, if already an event was set
        GPIO.remove_event_detect(self.used_pin)
        GPIO.add_event_detect(self.used_pin, GPIO.BOTH, callback=self.motion)

    # Override run method of threading
    def run(self):
        while self.keepRunning:
            timespan = (time.time() - self.lastMotion)

            if (timespan > self.max_not_moving_time):
                if(self.callback != None):
                    self.callback()

            time.sleep(0.250)

        GPIO.remove_event_detect(self.used_pin)

    # Eventhandler for GPIO filament sensor signal
    # The new state of the GPIO pin is read and determinated.
    # It is checked if motion is detected and printed to the console.
    def motion(self, pPin):
        self.lastMotion = time.time()
        self._logger.debug("Motion detected at " + str(self.lastMotion))