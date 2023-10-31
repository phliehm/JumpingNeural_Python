from turtle import Turtle



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
            self.forward(50)  # Move forward by 100 units (adjust as needed)
            self.left(90)  # Turn left 90 degrees to create a right angle
        self.end_fill()

    # single underscore --> protected but accessible by subclasses
    def _update_position(self):
        
        x,y = self.pos()
        new_y = y + self.velocityY # also no time multiplication
        new_x = x + self.velocityX
        if new_y >= self.baseY:    # check if the y value is still higher than the baseY
            self.setpos((new_x,new_y))

        # this is public
    def update(self):
        self.clear()
        self._update_position()
        

class Player(Object):
    def __init__(self,x,y) -> None:
        super().__init__(x,y)
        self.accelerationY = -0.2  # acceleration acts down  
        self.color("DarkBlue")

    # these methods can be private
    def __update_velocityY(self):
        self.velocityY += self.accelerationY  # we just set the time 1 here, so no need for a multiplication

    
    # this is public
    def update(self):
        self.clear()
        self.__update_velocityY()
        self._update_position()

    def jump(self):
        _,y = self.pos()
        
        if round(y) == self.baseY:
            self.velocityY = 10

            

    