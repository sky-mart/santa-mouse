from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t240 v10 cccagfc4 cccagfd4 cccbag>c>c>c>c>d>cbgf4"
    buzzer.play(intro)