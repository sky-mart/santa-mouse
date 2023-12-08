from pololu_3pi_2040_robot import robot
import time
from machine import I2C, Pin
from vl6180x import Sensor
display = robot.Display()


i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=400_000)
tof = Sensor(i2c)

while True:
  distance = tof.range()
  display.fill(0)
  display.text("Range : " + str(distance), 0, 0)
  display.show()