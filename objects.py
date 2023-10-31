from turtle import Turtle
import random
PEN_WIDTH = 3
OBJECT_SIZE = 50
SENSOR_LENGTH = 900

class Object(Turtle):
    def __init__(self,x,y) -> None:
        super().__init__()
        self.speed(0)
        self.hideturtle()
        self.penup()
        self.color("red")
        self.setpos((x,y))
        self.velocityY = 0
        self.velocityX = 0
        self.baseY = y  # thats the y value the player should always return to


    def draw(self):
        # Draw the rectangle
        self.pendown()
        self.begin_fill()
        for _ in range(4):  # Loop 4 times to draw all sides of the rectangle
            self.forward(OBJECT_SIZE)  # Move forward by 100 units (adjust as needed)
            self.left(90)  # Turn left 90 degrees to create a right angle
        self.end_fill()

    # single underscore --> protected but accessible by subclasses
    def _update_position(self):
        
        x,y = self.pos()
        new_y = y + self.velocityY # also no time multiplication
        new_x = x + self.velocityX

        # reuse this  object when it passed the player, this cannot happen to the player itself, as x for the player doesnt change
        if new_x < -OBJECT_SIZE:
            new_x = 3000 + random.randint(0,500)
        if new_y >= self.baseY:    # check if the y value is still higher than the baseY
            self.setpos((new_x,new_y))

    def update(self):
        self.clear()
        self._update_position()


        

class Player(Object):
    def __init__(self,x,y) -> None:
        super().__init__(x,y)
        self.accelerationY = -0.2  # acceleration acts down  
        self.color("DarkBlue")
        self.sensor = Sensor(self.pos())
        self.dead = False

    # these methods can be private
    def __update_velocityY(self):
        self.velocityY += self.accelerationY  # we just set the time 1 here, so no need for a multiplication

    
    # this is public
    def update(self, objs: [Object]):
        self.clear()
        self.__update_velocityY()
        self._update_position()
        self.sensor.update(self.pos())
        self.sensor.measure(objs)
        if self.sensor.detect_collision():
            self.color("gray")
            self.dead = True

    def jump(self):
        _,y = self.pos()
        
        if round(y) == self.baseY:
            self.velocityY = 10

            
class Sensor(Turtle):
    def __init__(self,position):
        super().__init__()
        self.speed(0)
        self.color("orange")
        self.pensize(width=PEN_WIDTH)
        #self.penup()
        self.hideturtle()
        self.setpos(position)
        self.closest = 1000
        self.x = position[0]
        

    def draw(self):
        self.goto((self.closest-PEN_WIDTH,self.pos()[1]))     # only draw the sensor until the closest object
        self.goto((self.x,self.pos()[1]))

    def update(self,position):
        self.clear()
        x,y = position
        self.setpos((x,y+OBJECT_SIZE/2))
        self.draw()

    def measure(self, objs: [Object]):
        # one cannot simply measure the pixel color with turtle and grabbing images with PIL would be too slow
        # --> just take the known coordinates of the objects, sadly that doesnt really compare well to a sensor then
        # but its ok for a simulation and for the neural network
        self.find_closest(objs)
        if self.closest < SENSOR_LENGTH:
            #print("HIT")
            pass
        else:
            #print("No HIT")
            pass
    # the sensor can only track the closest object, but it will be tracked regardeles of the players y position
    def find_closest(self,objs: [Object]):
        closest = 1000
        for object in objs:
            object_x = object.pos()[0]
            if  object_x < closest and object_x > self.x-OBJECT_SIZE: # object must be in front of the player, find closest
                closest = object_x
        self.closest = closest

    def detect_collision(self):
        if self.closest < self.x+OBJECT_SIZE and self.pos()[1]-OBJECT_SIZE/2 < OBJECT_SIZE:
            return True