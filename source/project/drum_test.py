#!/usr/bin/env python3

"""
Code to control motor for mechanical drum.
The drum is toggled on/off by pressing a "button" (US sensor).
"""

from utils.brick import Motor, TouchSensor, reset_brick
import time
from setup_brickpi import setup_ports

INSTRUCTION_BUFFER = 0.2    # seconds, nonzero so motor doesn't die

if __name__ == "__main__":
    try:
        # setup ports
        stop, motor = setup_ports(emergency_stop=True, drum_motor=True)
        
        # Designates to Encoder, that the current physical position is 0 degrees
        motor.reset_encoder()
        
        # Prevents position control from going over either:
        # 80% power or 360 deg/sec, whichever is slower
        motor.set_limits(power=80, dps=360)

        direction = +1
        # run until emergency stop is actuated
        while not stop.is_pressed():
            # added direction to have emergency stop verification twice as frequently
            motor.set_position_relative(direction * 90)
            time.sleep(INSTRUCTION_BUFFER)
            direction *= -1
    finally:
        print("Stopped")
        reset_brick()
        exit()
