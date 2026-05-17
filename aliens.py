import random
import turtle
import math
import time

class OutOfBounsMixin:
    def is_out_of_bounds(self, screen_width, screen_height):
        return (
            abs(self.xcor())> screen_width/2 
            or abs(self.ycor()) > screen_height/2
            )


class Enemy(turtle.Turtle, OutOfBounsMixin):
    speed_range = 0.1, 1
    max_turn_angle = 90
    turning_period_range = 0.5, 2
    
    def __init__(self):
       
        super().__init__ ()

        self.shape("turtle")
        self.penup()
        self.color(random.random(), random.random(), random.random())
        self.left(random.randint(1,359))
        self.enemy_speed = random.uniform(*self.speed_range)
        self.turning_period = random.uniform(*self.turning_period_range)
        self.start_timer = time.time()
    def move(self):
        self.forward(self.enemy_speed)
        
    def set_start_position(self, w,h):
        self.backward(
            math.sqrt(
                (w/2)**2
                +(h/2)**2
                )
            )
        if self.ycor() > h/2:
            self.sety(h/2)
        if self.ycor() < -h/2:
            self.sety(-h/2)
        if self.xcor() > w/2:
            self.setx(w/2)
        if self.xcor() < -w/2:
            self.setx(-w/2)
    
    def change_direction(self):
        if (time.time() - self.start_timer > self.turning_period):
            self.left(random.uniform(-self.max_turn_angle, self.max_turn_angle))
            self.start_timer = time.time()
    
  #  def is_out_of_bounds(self, w,h):
   #     return ( (abs(self.ycor()) > h/2 or abs(self.xcor()) > w/2))







class Laser(turtle.Turtle, OutOfBounsMixin):
    length = 10
    thickness = 5
    default_speed = 1
    collision_tolerance = 20
    def __init__(self, player):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color('red')
        self.pensize(self.thickness)
        self.setposition(player.position())
        self.setheading(player.heading())
        self.laser_speed = self.default_speed
        
    def set_speed(self, speed):
        self.laser_speed = speed

    def _draw(self):
        self.clear()
        self.pendown()
        self.forward(self.length)
        self.forward(-self.length)
        self.penup()
        
    def move(self):
        self.forward(self.laser_speed)
        self._draw()
    
    def has_collided_with(self, entity):
        return(
            self.distance(entity) <= self.collision_tolerance
            )



























        