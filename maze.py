from pololu_3pi_2040_robot import robot
from pololu_3pi_2040_robot.extras import editions
from machine import Pin
import time
import _thread
import play_anthem

buzzer = robot.Buzzer()
display = robot.Display()
motors = robot.Motors()
line_sensors = robot.LineSensors()

play_anthem.play()

# Note: It's not safe to use Button B in a
# multi-core program.
button_a = robot.ButtonA()

edition = editions.select()
if edition == "Standard":
    max_speed = 3000
    calibration_speed = 1000
    calibration_count = 100
elif edition == "Turtle":
    max_speed = 6000
    calibration_speed = 3000
    calibration_count = 100
elif edition == "Hyper":
    max_speed = 2000
    calibration_speed = 1000
    calibration_count = 100
    motors.flip_left(True)
    motors.flip_right(True)