from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t240 l8 v10 mscccagfmc2 mscccagfmd2 mscccbag>c>c>c>c>d>cbgmf2"
    buzzer.play(intro)