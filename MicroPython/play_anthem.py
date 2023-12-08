from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t240 gedcg4 gedca4 afedggggagfdc4"
    buzzer.play(intro)