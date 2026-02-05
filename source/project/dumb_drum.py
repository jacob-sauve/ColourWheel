from utils.brick import Motor, TouchSensor, wait_ready_sensors, reset_brick
import time

motor = Motor("A")
STOP = TouchSensor(3)

wait_ready_sensors(True)

# Designates to Encoder, that the current physical position is 0 degrees
motor.reset_encoder()

# Prevents position control from going over either:
# 50% power or 90 deg/sec, whichever is slower
motor.set_limits(power=50, dps=90)

#motor.set_limits() # UNLIMITED POWER (AND SPEED)

# Will rotate 10 degrees backwards from current position.
# Does not care about the absolute position.
while not STOP.is_pressed():
    motor.set_position_relative(motor.get_position()-10)
    time.sleep(2)
print("Stopped")
reset_brick()
exit()
