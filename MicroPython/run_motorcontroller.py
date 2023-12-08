from motor_controller import MotorController
import time

motorc = MotorController()

motorc.turn_right()
time.sleep(1)
motorc.turn_left()
time.sleep(1)
motorc.go_straight()
time.sleep(1)
motorc.turn_around()
