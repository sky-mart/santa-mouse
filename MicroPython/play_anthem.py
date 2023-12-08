from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t160 l4 v10 msc8c8a8g8f8mlc msc8c8a8g8f8mld msc8c8b8+a8g8>c8>c8>c8>c8>d8>c8b8+g8mlf"
    buzzer.play(intro)