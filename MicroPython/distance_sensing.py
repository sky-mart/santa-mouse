from pololu_3pi_2040_robot import robot
from machine import I2C, Pin
from vl6180x import Sensor
import time

display = robot.Display()

MAX_DIST_RAW = 190
MIN_DIST_RAW = 10
MAX_DIST_PHY = 20.5
MIN_DIST_PHY = 1.5
RAW_RANGE = 180
PHY_RANGE = 19
FACTOR = 180.0 / 19.0


def dbg(text):
  display.fill(0)
  display.text(text, 0, 0)
  display.show()

class DistanceSensor:
  def __init__(self, i2c):
    self.tof = Sensor(i2c)

  def get_distance(self):
    time.sleep(0.01)
    actual_value = self.tof.range()
    if actual_value > 190:
      actual_value = 190
    actual_value -= MIN_DIST_RAW
    return (actual_value / FACTOR) + 1.5


i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=400_000)
ds = DistanceSensor(i2c)

while True:
  dbg(str(ds.get_distance()))
