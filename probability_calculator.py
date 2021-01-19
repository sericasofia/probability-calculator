import copy
import random
import sys
import os

# clear terminal
def clear_screen():
    return f"{os.system('clear') if sys.platform == 'linux' or sys.platform == 'linux2' else os.system('cls')}"

class Hat:
    def __init__ (self, balls: dict): 
        self.balls = balls
        self.contents = [key for key, number in self.balls.items() for _ in range(number)] # display every ball in dictionary individually
        

    def draw(self, number_of_balls:int):
        random.shuffle(self.contents) # shuffle the contents list
        choices = []  
        
        # if number of balls are more than number of balls inside the hat, pull every ball at the same time.
        if number_of_balls >= len(self.contents):
            choices = self.contents
            self.contents = []
        else:
            for _ in range(number_of_balls):
                choices.append(self.contents.pop(random.randrange(0, len(self.contents)))) # choose randomly n number of balls which are pulled from he hat

        return choices # return pulled balls

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    expected_balls = [key for key, value in expected_balls.items() for _ in range(value)] # list of expected balls

    counts = 0
    
    for _ in range(num_experiments): # run experiement n times

        hatcopy = copy.deepcopy(hat) # make copy from hat

        draws = hatcopy.draw(num_balls_drawn) # draw balls rom the hat

        flag = True

        for ball in expected_balls: 
            if ball in draws:
                draws.remove(ball)
            else:
                flag = False

        if flag:
            counts += 1
            
    return (counts / num_experiments) * 100


if __name__ == '__main__':

    inside_hat = {}
    print("""
This section defines a balls you put inside a hat.

Give a color or type of the ball and how many of them.
Separate the ball and a number with a space.
Please do not enter the same color or type twice.
(example: 'yellow 3' OR 'striped 10').
""")

    while True:
        try:
            ball = input("(Empty input will exit): ")
            
            if ball == "":
                break

            inside_hat[ball.split()[0].lower()] = int(ball.split()[1])
        
        except ValueError:
            print("")

    clear_screen()

    print()

    expected_balls = {}
    print("""
This section defines the balls you are expecting to get when you are pulling balls from the hat.

Enter expected color or type of the ball and how many of them. 
Separate color or type and a number with a space.
Color or type of the expected balls must be the same as inside the hat.
Number of specific expected ball can't be more than the same specific ball inside the hat.
please do not give same color or type of the expected ball twice.
(example: 'blue 5' OR 'striped 6').
""")
    print(f"Inside of the hat: {', '.join([f'{key} = {value}' for key, value in inside_hat.items()])} ")
    print()
    while True:    
        expected = input("(Empty input will exit): ")

        if expected == "":
            break

        expected_balls.update({expected.split()[0].lower(): int(expected.split()[1])})

    clear_screen()

    number_balls_drawn = int(input(f"""
This section defines how many balls are pulled from the hat at the same time.

Enter how many balls will be pulled from the hat at the same time.
Please give a whole number (example: 10).
You have {sum(ball for ball in inside_hat.values())} balls inside hat.
    
: """))

    clear_screen()

    number_of_experiments = int(input("""
This section defines how many times the balls are pulled from the hat.

Enter how many times the balls are drawn from the hat.
Please give a whole number (example: 1000).

: """))

    clear_screen()

    hat = Hat(inside_hat)

    probability = experiment(
        hat=hat, 
        expected_balls=expected_balls,
        num_balls_drawn=number_balls_drawn, 
        num_experiments=number_of_experiments)

    print(f"Probability: {probability} %")
    print()
    input("Press 'Enter' to exit!")
    