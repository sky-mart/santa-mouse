# import machine
from pololu_3pi_2040_robot import robot
import time

motors = robot.Motors()
display = robot.Display()
yellow_led = robot.YellowLED()
imu = robot.IMU()
imu.reset()
imu.enable_default()

class MotorController():

    def turn_right(self):
        self.turn(90)

    def turn_left(self):
        self.turn(-90)

    def turn_around(self):
        self.turn(180)

    def go_straight(self):
        max_speed = 250
        motors.set_speeds(max_speed, max_speed)

    def turn(self, target_angle):
        drive_motors = False
        last_time_gyro_reading = None
        last_time_far_from_target = None
        turn_rate = 0.0  # degrees per second
        robot_angle = 0.0  # degrees
        max_speed = 250
        turn_time = 50
        kp = 14
        kd = 4

        while True:
            # Update the angle and the turn rate.
            if imu.gyro.data_ready():
                imu.gyro.read()
                turn_rate = imu.gyro.last_reading_dps[2]  # degrees per second
                now = time.ticks_us()
                if last_time_gyro_reading:
                    dt = time.ticks_diff(now, last_time_gyro_reading)
                    robot_angle += turn_rate * dt / 1000000
                last_time_gyro_reading = now

            # Decide whether to stop the motors.
            if drive_motors:
                far_from_target = abs(robot_angle - target_angle) > 3
                if far_from_target:
                    last_time_far_from_target = time.ticks_ms()
                elif time.ticks_diff(time.ticks_ms(), last_time_far_from_target) > 250:
                    drive_motors = False

            # Drive motors.
            if drive_motors:
                turn_speed = (target_angle - robot_angle) * kp - turn_rate * kd
                if turn_speed > max_speed: turn_speed = max_speed
                if turn_speed < -max_speed: turn_speed = -max_speed
                motors.set_speeds(-turn_speed, turn_speed)
            else:
                motors.off()

            # Break out of the turn loop if turned enough
            if target_angle == robot_angle:
                return