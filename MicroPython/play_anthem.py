from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t120 l4 v10 ms2c4c8c16a32g64f4mc ms4c4c4c4a4g4f4md ms4c4c4c4b4a4g4>c4>c4>c4>c4>d4>c4b4g4mf"
    buzzer.play(intro)