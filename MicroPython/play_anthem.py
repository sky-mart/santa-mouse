from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t120 l2 v10 ms8c8c8c8a8g8f2mc ms8c8c8c8a8g8f2md ms8c8c8c8b8a8g8>c8>c8>c8>c8>d8>c8b8g2mf"
    buzzer.play(intro)