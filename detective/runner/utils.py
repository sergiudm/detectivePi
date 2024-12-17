# Description: This file contains the RunnerEngine class which is responsible for running the runner.

# import RPi.GPIO as GPIO
# import time

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)


class PinManeger:
    """PinManeger class to manage pins

    Attributes:
    pinContainer: a pinContainer is a set of pins with their states
    """

    def __init__(self):
        self.pinContainer = dict()
        for i in range(10):
            self.pinContainer[i] = dict()

    def set_pin_container(self, pin_id, pin_with_state):
        self.pinContainer[pin_id] = pin_with_state

    def show_pins(self):
        for pin_id, pins in self.pinContainer.items():
            print(f"Pin ID: {pin_id}, Pin Container: {pins}")


def msg2pin_state(msg, state_mapping):
    """msg2pin_state function to convert message to pin state

    Args:
    msg: message to convert

    Returns:
    pin_state: pin state
    """
    pin_manager = PinManeger()


def run_gpio():
    pins = PinManeger()
    pins.set_pin_container(1, {17: 0, 23: 0, 3: 0})
    pins.set_pin_container(2, {4: 1, 5: 1, 6: 1})
    pins.show_pins()


if __name__ == "__main__":
    run_gpio()
