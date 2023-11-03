from turtle import Turtle
import random
from neuralNetwork import NeuralNetwork
PEN_WIDTH = 3
OBJECT_STRETCH = 2 # 2*20px = 40px
OBJECT_SIZE = OBJECT_STRETCH*20 # 40px
JUMP_VELOCITY_Y = 10
CANVAS_WIDTH = 1000
SENSOR_LENGTH = CANVAS_WIDTH
ACCELERATION_Y = -0.2

class Object(Turtle):
    def __init__(self,x,y) -> None:
        super().__init__()
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.shape("square")
        self.shapesize(OBJECT_STRETCH,OBJECT_STRETCH)
        self.color("red")

        self.setpos((x,y))
        self.showturtle()
        self.x = x      # x,y can be accessed by the self.pos() method, but storing them like
        self.y = y      # this is much more convenient and easier to read (as this is educational)

        self.velocityY = 0
        self.velocityX = 0
        self.accelerationX = 0
        self.accelerationY = 0
        self.baseY = y  # thats the y value the player should always return to


    # single underscore --> protected but accessible by subclasses
    def _update_position(self):
        
        new_y = self.y + self.velocityY # also no time multiplication
        new_x = self.x + self.velocityX

        if new_y >= self.baseY:    # check if the y value is still higher than the baseY
            self.setpos((new_x,new_y))
            self.x = new_x
            self.y = new_y

    # this is a private method
    def _update_velocity(self):
        self.velocityY += self.accelerationY  # we just set the time 1 here, so no need for a multiplication
        self.velocityX += self.accelerationX

    def update(self):
        self.clear()
        self._update_position()
        # self.update_velocity()
    def set_position(self,x,y):
        self.x = x
        self.y = y
        self.setposition((x,y))
        
        

class Player(Object):
    def __init__(self,x,y,controlType, neurons) -> None:
        super().__init__(x,y)
        self.accelerationY = ACCELERATION_Y  # acceleration acts down  
        self.color("DarkBlue")
        self.sensor = Sensor(self.pos())
        self.dead = False
        self.Ai = controlType == 'AI'
        if self.Ai:
            self.brain = NeuralNetwork([1,neurons,1])
            #for level in self.brain.levels:
                #print(level.weights[0])

    def update(self, objs: [Object]):
        self.clear()
        self._update_velocity()
        self._update_position()
        self.sensor.update(self.pos())
        self.sensor.find_closest(objs)
        if self.sensor.detect_collision():
            self.color("gray")
            self.dead = True
        if self.Ai:
            # input values are normalised with SENSOR_LENGTH to keep values between 0...1
            output = NeuralNetwork.feed_forward(self.brain,[self.sensor.closest/SENSOR_LENGTH]) 
            if output[0] == 1:
                self.jump()
        
    def jump(self):
        if round(self.y) == self.baseY:
            self.velocityY = JUMP_VELOCITY_Y

    def mutate(self,amount):
        NeuralNetwork.mutate(self.brain,amount)

    def clear_sensor(self):
        self.sensor.clear()


    def get_brain_data(self):
        return self.brain.get_brain_data() 
    
    def set_brain_data(self,brain_data):
        self.brain.set_brain_data(brain_data)

    
    def reset_player(self):
        self.setposition(0,0)
        self.clear()
        self.brain.randomize()
        self.accelerationY = ACCELERATION_Y
        self.dead = False
        self.velocityY = 0
        self.showturtle()
        
    def kill(self):
        self.accelerationY=0
        self.hideturtle()
        self.clear()
        self.clear_sensor()
            
class Sensor(Turtle):
    def __init__(self,position):
        super().__init__()
        self.hideturtle()
        self.speed(0)
        self.color("orange")
        self.pensize(width=PEN_WIDTH)
        #self.penup()

        self.setpos(position)
        self.closest = SENSOR_LENGTH
        self.x = position[0]
        self.y = position[1]
        
    # here we need a draw function as we dont use a shape to draw the sensor
    def draw(self):
        self.goto((self.closest-PEN_WIDTH,self.y))     # only draw the sensor until the closest object
        self.goto((self.x,self.y))

    def update(self,player_position):
        player_x,player_y = player_position  
        self.clear()
        self.setpos((player_x,player_y))
        self.y = self.pos()[1]      # update the attributes cause the turtle position has changed
        self.draw()


    # the sensor can only track the closest object, but it will be tracked regardeles of the players y position
    def find_closest(self,objs: [Object]):
        closest = CANVAS_WIDTH
        for object in objs:
            if  object.x < closest and object.x > self.x-OBJECT_SIZE: # object must be in front of the player, find closest
                closest = object.x
        self.closest = closest

    def detect_collision(self):
        if self.closest < self.x+OBJECT_SIZE and self.y-OBJECT_SIZE/2 < OBJECT_SIZE:
            return True