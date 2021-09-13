'''
Has the turtle animation to visualize the policy and to show its updates as
a neat and clean animation
'''

import turtle
from time import sleep


wn = turtle.Screen()
wn.bgcolor("White")
wn.title("A Maze Game")
wn.setup(700,700)
#wn.exitonclick()

#Create Pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("#008080")
        self.penup()
        self.speed(0)
        self.ht()
        #Animation speed

pen=Pen()

def setup_maze(level):

    pen.ht()

    wn.tracer(0, 0)
    for y in range(len(level)):
        for x in range(len(level[y])):
            #Get the character at each x, y coordinate
            #Note the order of y and x in the next line
            character = level[y][x]
            #Calculate the screen x, y coordinates
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            #Check if it is an X (representing a wall)
            if character == "#":
                pen.goto(screen_x, screen_y)
                pen.stamp()

    pen.color('red')
    pen.goto(-264, 264)
    pen.stamp()

    wn.update()

    #turtle.done()

#turtle animations
def animate_policy(policy, iterations):

    pen.shape('arrow')
    pen.ht()
    wn.tracer(0,0)

    for y in range(len(policy)):
        for x in range(len(policy[y])):

            character = policy[y][x]

            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)


            if character != '#':
                pen.goto(screen_x, screen_y)
                pen.color('white')
                pen.shape('square')
                pen.stamp()
                pen.color('black')
                pen.shape('arrow')


            if character == 'up':
                pen.setheading(90)
                pen.stamp()

            if character == 'down':
                pen.setheading(270)
                pen.stamp()

            if character == 'left':
                pen.setheading(180)
                pen.stamp()

            if character == 'right':
                pen.setheading(0)
                pen.stamp()

    pen.color('red')
    pen.shape('square')
    pen.goto(-264, 264)
    pen.stamp()
    pen.color('white')
    pen.shape('square')
    pen.goto(-288, 264)
    pen.stamp()
    pen.color('white')
    pen.shape('square')
    pen.goto(-288+24*(len(policy)-1), 288-24*(len(policy)-2))
    pen.stamp()

    pen.color('white')
    pen.goto(-288, -194)
    pen.stamp()
    pen.goto(-268, -194)
    pen.stamp()
    pen.goto(-248, -194)
    pen.stamp()
    pen.goto(-228, -194)
    pen.stamp()
    pen.goto(-208, -194)
    pen.stamp()
    pen.goto(-188, -194)
    pen.stamp()
    pen.goto(-168, -194)
    pen.stamp()
    pen.goto(-148, -194)
    pen.stamp()

    pen.color('black')
    pen.goto(-297, -208)
    pen.write('Iterations: {}'.format(iterations), font=('Arial', 20, 'normal'))

    # sleep(1)#Ketan Speed Control
    wn.update()
