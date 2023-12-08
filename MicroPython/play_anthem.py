from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t240 l8 v10 !c!c!c?agfc2 cccagfd2 cccbag>c>c>c>c>d>cbgf2"
    buzzer.play(intro)