import logging
import logging.config
import yaml
import turtle
import time
import random
from configparser import ConfigParser

#recives colors from config.ini converts them in int array
def colorDecoder(color):
    rgb=color.split(",")
    rgb[0]=int(rgb[0])
    rgb[1]=int(rgb[1])
    rgb[2]=int(rgb[2])
    return rgb

# Loading logging configuration
with open('./log_c.yaml', 'r') as stream:
    config = yaml.safe_load(stream)

logging.config.dictConfig(config)

# Creating logger
logger = logging.getLogger('root')

# Initiating and reading config values
logger.info('Loading configuration from file')


try:
    #importing config
    config = ConfigParser()
    config.read('config.ini')

    backgroundColor = config.get('Color','bg')
    headColor = config.get('Color','head')
    foodColor = config.get('Color','food')
    scoreColor = config.get('Color','score')
    trailColor =  config.get('Color','trail')
except:
	logger.exception("")
logger.info('DONE')

delay = 0.1

# Score
score = 0
high_score = 0

# Set up the screen
logger.info('Stting up playing field')
wn = turtle.Screen()
wn.title("Snake Game")
wn.colormode(255)
rgb=colorDecoder(backgroundColor)
wn.bgcolor(rgb[0],rgb[1],rgb[2])
wn.setup(width=600, height=600)
wn.tracer(0) # Turns off the screen updates

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
rgb=colorDecoder(headColor)
head.color(rgb[0],rgb[1],rgb[2])
head.penup()
head.goto(0,0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
rgb=colorDecoder(foodColor)
food.color(rgb[0],rgb[1],rgb[2])
food.penup()
food.goto(0,100)

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
rgb=colorDecoder(scoreColor)
pen.color(rgb[0],rgb[1],rgb[2])
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

logger.info('DONE')

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# Main game loop
logger.info('Game has started')
while True:
    wn.update()

    # Check for a collision with the border
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        logger.info('Game finished with score = '+str(score))
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"

        # Hide the segments
        for segment in segments:
            segment.goto(1000, 1000)
        
        # Clear the segments list
        segments.clear()

        # Reset the score
        score = 0

        # Reset the delay
        delay = 0.1

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 


    # Check for a collision with the food
    if head.distance(food) < 20:
        # Move the food to a random spot
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x,y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("circle")
        rgb=colorDecoder(trailColor)
        new_segment.color(rgb[0],rgb[1],rgb[2])
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay
        delay -= 0.0001

        # Increase the score
        score += 10

        if score > high_score:
            high_score = score
        
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()    

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            logger.info('Game finished with score = '+str(score))
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
        
            # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)
        
            # Clear the segments list
            segments.clear()

            # Reset the score
            score = 0

            # Reset the delay
            delay = 0.1
        
            # Update the score display
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)

wn.mainloop()