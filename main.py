import turtle
import time
import random
import copy
import json

from objects import Player,Object

# colors for the different AIs
COLORS  =  ["green","blue","yellow","purple","orange","black","skyblue","gold","maroon","cyan",
            "magenta","lime","pink","navy","coral","olive","brown","teal","violet","salmon"
            ]
COLORS = 5*COLORS

CANVAS_HEIGHT = 500
CANVAS_WIDTH = 1000

CANVAS_HEIGHT = 500
CANVAS_WIDTH = 1000
NUMBER_OF_AIS = 20          # How many AIs at the same time per generation
NUMBER_OF_OBSTACLES = 10    # how many obstacles (but they will come back after the passed the player/AI)#
MIN_OBSTACLE_DISTANCE = 500 # obstacles need some minimum distance (depends on how fast the jump is)
NUMBER_OF_NEURONS = 2       # how many neurons in the middle layer 
MUTATION_STRENGTH = 0.1     # mutation strength (1 stronger mutation, 0 no mutation)

PLAYER_X = 20
BASELINE_Y = 20

# initialise the variable to end the game
end_game = False

# Create a turtle screen
wn = turtle.Screen()

# Setup turtle screen
# Window setup
wn.setup(CANVAS_WIDTH,CANVAS_HEIGHT)
# change the coordinates such that at the bottom left is 0,0
wn.setworldcoordinates(-20,-20,CANVAS_WIDTH,CANVAS_HEIGHT)
wn.title("Turtle AI")
wn.bgcolor("white")
# don't auto update the screen
wn.tracer(0)


# create one AI, need to because of how we write the"reset_simulation"
first_AI = Player(0,0,"AI",NUMBER_OF_NEURONS)
file_path = 'neural_network_data.json'
try:
    with open(file_path, 'r') as json_file:
        brain_data = json.load(json_file)
    print(brain_data["Level 1"])
    first_AI.set_brain_data(brain_data)
except:
    pass



artificial_players = []
artificial_players.append(first_AI)


def create_AIs(number, neuron_count,artificial_players) -> Player:
    """Create and return a list of AI players."""

    for i in range(number-1):
        new_AI = Player(0,0,"AI",neuron_count)
        new_AI.color(COLORS[i])
        artificial_players.append(new_AI)
    

def reset_AIs(ais):
    for i,ai in enumerate(ais):
        ai.reset_player()
        ai.color(COLORS[i])

def create_enemies(enemies,number=NUMBER_OF_OBSTACLES):

    # obstacles should be far away enough, but also a bit random
    for i in range(number):
        enemies.append(Object(0,0))
        enemies[i].velocityX = -5
    # move the enemies to the correct positions
    set_all_enemies_position(enemies)

def set_all_enemies_position(enemies):
    # starting distance
    current_distance = CANVAS_WIDTH
    for enemy in enemies:
        enemy.set_position(current_distance,0)
        # the distance should be changed by a minimum and maximum amount
        current_distance += random.randint(MIN_OBSTACLE_DISTANCE,2000)


def start_simulation(ais,enemies):
    create_AIs(NUMBER_OF_AIS,NUMBER_OF_NEURONS,ais)
    create_enemies(enemies)

def reset_simulation(parent_ai,makeBabies,ais,enemies):
    
    """Reset the simulation by creating new AIs, Obstacles and clear the screen"""
    
    set_all_enemies_position(enemies)

    # save the data of the best brain
    best_brain_data = copy.deepcopy(parent_ai.get_brain_data())
    """     # Specify the file path where you want to save the data
    file_path = 'neural_network_data.json'
    with open(file_path, 'w') as json_file:
        json.dump(best_brain_data, json_file, indent=4) 
        """
    reset_AIs(ais)

    # give values to next generation
    if makeBabies:
        print("Making Babies!!!!") 
        # Load the dictionary from the JSON file
        count = 0
        for ai in ais:
            ai.set_brain_data(best_brain_data)
            print(ai.get_brain_data()["Level 0"])
            ai.mutate(MUTATION_STRENGTH)
            print(ai.get_brain_data()["Level 0"])
            

    else:
        reset_AIs(ais)


# this function is needed as the turtle.onclick() takes a function as argument
def end_game_handler(x,y):
    global end_game
    end_game = True


enemies = []

def main():
    global NUMBER_OF_AIS
    global MUTATION_STRENGTH
    start_simulation(artificial_players,enemies)


    print(artificial_players[0].get_brain_data())
    wn.listen() # listen to key input events
    wn.onclick(end_game_handler)    
    enemies_gone = 0
    # game loop
    while not end_game:
        # list of indicies of AIs which are alive
        alive = []
        

        if enemies_gone == NUMBER_OF_OBSTACLES:
            MUTATION_STRENGTH = 0.0001
                # start next generation if only 1 AI remains
            if len(alive) <= 1:
                if len(alive) ==1:
                    print("ONE ALIVE!!!")
                    # reset game and make babies
                    reset_simulation(artificial_players[alive[0]],True,artificial_players,enemies)
                    # reset the list of indicator for living AIs

                # in case no AI is left, try using a saved one as parent
                if len(alive) == 0:  
                    try:  
                        reset_simulation(parentAI,True,artificial_players,enemies)
                    except: # if no AI could be saved, start new
                        reset_simulation(first_AI,False,artificial_players,enemies)
                alive=[]
        # update positions and draw all objects
        enemies_gone = 0
        for enemy in enemies:
            enemy.update()
            if enemy.x < -50:
                enemies_gone += 1

        
        # let all the AIs play
        for i,AI in enumerate(artificial_players):
            # AI is dead --> skip it
            if AI.accelerationY == 0:
                continue

            # allow jump by pressing a key (so one can still play as a player)
            #wn.onkeypress(AI.jump,"w") 
            # update position, sensor readings for AIs
            AI.update(enemies)
            # make sure the dead artificial_players dont move anymore
            if AI.dead: 
                AI.kill()
            # Add living AIs to a list to check later how many remain
            alive.append(i)
        print(alive) # useful to see how many AIs are alive, because they often overlap

        wn.update() # update screen
        #time.sleep(0.001)
        
        # start next generation if only 1 AI remains
        if len(alive) <= 1:
            if len(alive) ==1:
                MUTATION_STRENGTH = 0.01
                print("ONE ALIVE!!!")
                # reset game and make babies
                reset_simulation(artificial_players[alive[0]],True,artificial_players,enemies)
                # reset the list of indicator for living AIs

            # in case no AI is left, try using a saved one as parent
            if len(alive) == 0:
                MUTATION_STRENGTH = 0.1  
                try:  
                    reset_simulation(parentAI,True,artificial_players,enemies)
                except: # if no AI could be saved, start new
                    reset_simulation(first_AI,False,artificial_players,enemies)
            alive=[]

        # this controls how fast the game runs, if its not anyway slower cause of bottlenecks
        time.sleep(0.001)

        # save an AI in case all remaning AIs die at once, keep one, maybe this can be more elegant?
        try:
            parentAI = artificial_players[alive[0]]     
        except:
            print("All AIs died at the same time")
            time.sleep(.5)
    

    wn.exitonclick()
    # Specify the file path where you want to save the data
    file_path = 'neural_network_data.json'
    with open(file_path, 'w') as json_file:
        print(alive[0])
        json.dump(artificial_players[alive[0]].get_brain_data(), json_file, indent=4)




if __name__ == "__main__":
    main()

