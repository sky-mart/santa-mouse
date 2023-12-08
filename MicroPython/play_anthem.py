from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t140 l2 v10 msc8c8c8a8g8f8mlc msc8c8c8a8g8f8mld2 msc8c8c8b8a8g8>c8>c8>c8>c8>d8>c8b8g8mlf4"
    buzzer.play(intro)