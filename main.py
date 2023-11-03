import turtle
from objects import Player,Object
import time
import random

CANVAS_HEIGHT = 500
CANVAS_WIDTH = 1000

BASE_LINE_Y = 0 # position of the ground
PLAYER_X = 0 

end = False



# Create a turtle screen
wn = turtle.Screen()
wn.setup(CANVAS_WIDTH,CANVAS_HEIGHT)
wn.setworldcoordinates(-20,-20,CANVAS_WIDTH,CANVAS_HEIGHT)
wn.title("Rectangle Drawing")
wn.bgcolor("white")

# Create a turtle object
ai = Player(PLAYER_X,BASE_LINE_Y)


# create obstacles 
obstacles= []

# this creates a list of turtles in a row, it would be more efficient to create 10 turtles, then use
# the same turtles again when they left the screen
for i in range(3):
    new_object = Object(800+i*1000+random.randint(0,500),BASE_LINE_Y)
    #new_object = Object(70,0)
    new_object.velocityX = -5 # -0.1
    obstacles.append(new_object)

# don't auto update the screen
wn.tracer(0)
# listen to key events
wn.listen()

def end_game(x,y):
    global end 
    end = True


def main():
    global end
    while not end:
        wn.onkeypress(ai.jump,"w")
        # draw all objects
        for object in obstacles:
            object.update()
            x = object.pos()[0]
        ai.update(obstacles)
        wn.update()
        if ai.dead:
            end = True
        time.sleep(0.01)
        wn.onclick(end_game)    # end the game

    wn.exitonclick()


if __name__ == "__main__":
    main()