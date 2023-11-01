import turtle
import time
import random
import copy

from objects import Player,Object

# colors for the different AIs
COLORS  =  ["green","blue","yellow","purple","orange","black","skyblue","gold","maroon","cyan",
            "magenta","lime","pink","navy","coral","olive","brown","teal","violet","salmon"
            ]

CANVAS_HEIGHT = 500
CANVAS_WIDTH = 1000

CANVAS_HEIGHT = 500
CANVAS_WIDTH = 1000
NUMBER_OF_AIS = 20          # How many AIs at the same time per generation
NUMBER_OF_OBSTACLES = 100     # how many obstacles (but they will come back after the passed the player/AI)#
MIN_OBSTACLE_DISTANCE = 400 # obstacles need some minimum distance (depends on how fast the jump is)
NUMBER_OF_NEURONS = 1       # how many neurons in the middle layer 
MUTATION_STRENGTH = 0.4     # mutation strength (1 stronger mutation, 0 no mutation)

# initialise the variable to end the game
end_game = False

# Create a turtle screen
wn = turtle.Screen()



# Setup turtle screen
# Window setup
wn.setup(CANVAS_WIDTH,CANVAS_HEIGHT)
# change the coordinates such that at the bottom left is 0,0
wn.setworldcoordinates(0,0,CANVAS_WIDTH,CANVAS_HEIGHT)
wn.title("Turtle AI")
wn.bgcolor("white")
# don't auto update the screen
wn.tracer(0)


# create one AI, need to because of how we write the"reset_simulation"
first_AI = Player(0,0,"AI",NUMBER_OF_NEURONS)


def create_AIs(number, neuron_count) -> Player:
    """Create and return a list of AI players."""
    ais = []
    for i in range(number-1):
        new_AI = Player(0,0,"AI",neuron_count)
        new_AI.color(COLORS[i])
        ais.append(new_AI)
    return ais


def clear_drawings(ais, obstacles):
    """Remove all drawings from the AIs and Obstacles"""
    for ai in ais:
        ai.clear_all()
    for obj in obstacles:
        obj.clear()


def reset_simulation(parent_ai,AI_number, makeBabies):
    """Reset the simulation by creating new AIs, Obstacles and clear the screen"""
    
    obstacles = []
    # starting distance
    current_distance = CANVAS_WIDTH
    
    # obstacles should be war awy enough, but also a bit random
    for i in range(NUMBER_OF_OBSTACLES):
        obstacles.append(Object(current_distance,0))
        obstacles[i].velocityX = -5
        # change the distance by min amount
        current_distance +=  random.randint(MIN_OBSTACLE_DISTANCE,1000)
        print(current_distance)

    
    ais = create_AIs(AI_number,NUMBER_OF_NEURONS)
    # give values to next generation
    if makeBabies:
        print("Making Babies!!!!")
        for ai in ais:
            ai.brain = copy.deepcopy(parent_ai.brain)
            ai.mutate(MUTATION_STRENGTH)
    return ais , obstacles


# this function is needed as the turtle.onclick() takes a function as argument
def end_game_handler(x,y):
    global end_game
    end_game = True
    

def main():
    artificial_players, enemies = reset_simulation(first_AI,NUMBER_OF_AIS,False)

    
    wn.listen() # listen to key input events

    wn.onclick(end_game_handler)    
    
    # game loop
    while not end_game:
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
                AI.clear_all() # clear the dead AIs drawings
            # Add living AIs to a list to check later how many remain
            alive.append(i)
        #print(alive), useful to see how many AIs are alive, because they often overlap
        wn.update() # update screen
        
        # start next generation if only 1 AI remains
        if len(alive) <= 1:
            clear_drawings(artificial_players,enemies)
            if len(alive) ==1:
                # reset game and make babies
                artificial_players, enemies  = reset_simulation(artificial_players[alive[0]],NUMBER_OF_AIS,True)
                # reset the list of indicator for living AIs

            # in case no AI is left, try using a saved one as parent
            if len(alive) == 0:  
                try:  
                    artificial_players, enemies = reset_simulation(parentAI,NUMBER_OF_AIS, True)
                except: # if no AI could be saved, start new
                    artificial_players, enemies  = reset_simulation(first_AI,NUMBER_OF_AIS,False)
            alive=[]

        # this controls how fast the game runs, if its not anyway slower cause of bottlenecks
        #time.sleep(0.001)

        # save an AI in case all remaning AIs die at once, keep one, maybe this can be more elegant?
        try:
            parentAI = artificial_players[alive[0]]     
        except:
            print("All AIs died at the same time")
            time.sleep(.5)
    

    wn.exitonclick()


if __name__ == "__main__":
    main()

