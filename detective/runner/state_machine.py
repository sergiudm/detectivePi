# Description: This file contains the RunnerEngine class which is responsible for running the runner.

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class StateMachine:
    def __init__(self, initial_state, pin_data):
        self.current_state = initial_state
        self.pin_data = pin_data
        for pin in self.pin_data["pin_list"]:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        self.set_pin_state(self.current_state)


    def set_pin_state(self, state):
        high_pins = self.pin_data["pin_map"].get(state, [])
        for pin in self.pin_data["pin_list"]:
            if pin in high_pins:
                GPIO.output(pin, GPIO.HIGH)
                print(f"Pin {pin} set to HIGH")
            else:
                GPIO.output(pin, GPIO.LOW)
                print(f"Pin {pin} set to LOW")
        print(f"Transitioning to state: {state}")

    def transition(self, new_state):
        if new_state in self.pin_data["pin_map"]:
            self.current_state = new_state
            self.set_pin_state(self.current_state)
        else:
            print(f"Error: Invalid state '{new_state}'")


if __name__ == "__main__":
    pin_data = {
        "pin_list": [17, 23, 24, 25, 27],
        "pin_map": {
            "Right": [17, 23, 24],
            "Return": [23, 24],
            "Left": [17, 24],
            "Pause": [],
            "Like": [25],
            "OK": [27],
            "default": [],
        },
    }
    # Example usage:
    state_machine = StateMachine("stop", pin_data)  # Start in "stop" state

    state_machine.transition("OK")
    time.sleep(1)

    state_machine.transition("pause")
    time.sleep(1)

    state_machine.transition("good")
    time.sleep(1)

    state_machine.transition("invalid_state")  # Example of invalid state
