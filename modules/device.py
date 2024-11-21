import time

import RPi.GPIO as GPIO

def activate_buzzer(pin, state=0):
    """
    Activates a buzzer connected to the specified GPIO pin for a given duration.

    :param pin: GPIO pin number where the buzzer is connected.
    :param duration: Duration in seconds for which the buzzer should sound.
    """
    # Set up the GPIO pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, state)
