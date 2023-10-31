import turtle
from objects import Player,Object
import time
import random
import copy

# colors for the different AIs
COLORS  =  [
    "green", 
    "blue", 
    "yellow", 
    "purple", 
    "orange", 
    "black", 
    "skyblue", 
    "gold", 
    "maroon",
    "cyan", 
    "magenta", 
    "lime", 
    "pink", 
    "navy", 
    "coral", 
    "olive", 
    "brown", 
    "teal", 
    "violet",
    "salmon"
]

# Create a turtle screen
wn = turtle.Screen()
#wn.screensize(1000,1000)
CANVAS_HEIGHT = 500
CANVAS_WIDTH = 1000

# Window setup
wn.setup(CANVAS_WIDTH,CANVAS_HEIGHT)
# change the coordinates such that at the bottom left is 0,0
wn.setworldcoordinates(0,0,CANVAS_WIDTH,CANVAS_HEIGHT)
wn.title("Turtle AI")
wn.bgcolor("white")






# How many AIs at the same time per generation
number_of_AIs = 20
# how many obstacles (but they will come back after the passed the player/AI)
number_of_obstacles = 3
# how many neurons in the middle layer 
number_of_neurons = 2
# mutation strength
mutation_strength = 0.2

def create_AIs(number) -> Player:
    ais = []
    for i in range(number-1):
        new_AI = Player(0,0,"AI",number_of_neurons)
        new_AI.color(COLORS[i])
        ais.append(new_AI)
    return ais

# create obstacles 
obstacles= []

first_AI = Player(0,0,"AI",number_of_neurons)

def clear_drawings(ais, obstacles):
    for ai in ais:
        ai.clear_all()
    for obj in obstacles:
        obj.clear()


def reset_simulation(parent_ai,AI_number, makeBabies):
    #clear_drawings()
    obstacles = []
    # this creates a list of turtles in a row, it would be more efficient to create 10 turtles, then use
    # the same turtles agAIn when they left the screen
    rand_distance = random.randint(700,1000)
    for i in range(number_of_obstacles):
        #new_object = Object(800+i*600+random.randint(0,500),0)
        new_object = Object(rand_distance+i*600,0)

        #new_object = Object(270,0)
        new_object.velocityX = -5 # -0.1
        obstacles.append(new_object)
    ais = create_AIs(AI_number)
    # give values to next generation
    if makeBabies:
        print("Making Babies!!!!")
        for ai in ais:
            ai.brain = copy.deepcopy(parent_ai.brain)
            ai.mutate(mutation_strength)
    return ais , obstacles

artificial_players, enemies = reset_simulation(first_AI,number_of_AIs,False)

# don't auto update the screen
wn.tracer(0)
# listen to key events
wn.listen()

# this function is needed as the turtle.onclick() takes a function as argument
def end_Game(x,y,end):
    end = True


# initialise the variable to end the game
end = False

# game loop
while not end:
    # list of indicies of AIs which are alive
    alive = []

    # update positions and draw all objects
    for object in enemies:
        object.update()
        x = object.pos()[0]
        # only draw objects within the screen, improves performance
        if x < CANVAS_WIDTH and x > -50:  
            object.draw()
    
    # let all the AIs play
    for i,AI in enumerate(artificial_players):
        # AI is dead --> skip it
        if AI.accelerationY == 0: 
            continue
        # allow jump by pressing a key (so one can still play as a player)
        wn.onkeypress(AI.jump,"w") 
        # update position, sensor readings for AIs
        AI.update(enemies)
        # AIs have to be alive to be drawn (they could just have died in this loop)
        if not AI.dead:
            AI.draw()
        else: # make sure the dead artificial_players dont move anymore
            AI.accelerationY=0
            # clear the dead AIs drawings
            AI.clear_all()
        # Add living AIs to a list to check later how many remain
        alive.append(i)
    #print(alive)
    wn.update()
    
    # go to the next generation if only 1 AI remains
    if len(alive) <= 1:
        clear_drawings(artificial_players,enemies)
        if len(alive) ==1:
            # reset game and make babies
            artificial_players, enemies  = reset_simulation(artificial_players[alive[0]],number_of_AIs,True)
            # reset the list of indicator for living AIs

        # in case no AI is left, try saved one
        if len(alive) == 0:  
            try:  
                artificial_players, enemies = reset_simulation(parentAI,number_of_AIs, True)
            except: # if no AI could be saved, start new
                artificial_players, enemies  = reset_simulation(first_AI,number_of_AIs,False)
        alive=[]

    # this controls how fast the game runs, if its not anyway slower cause of bottlenecks
    time.sleep(0.001)

    # save an AI in case all remaning AIs die at once, keep one, maybe this can be more elegant?
    try:
        parentAI = artificial_players[alive[0]]     
    except:
        print("Exception!! Why?")
        time.sleep(1)

    wn.onclick(end_Game)    # end the game

wn.exitonclick()
