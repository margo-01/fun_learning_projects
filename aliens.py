import random
import turtle
import math
import time


class Enemy(turtle.Turtle):
    speed_range = 0.5, 10
    max_turn_angle = 90
    turning_period_range = 0.5, 2
    
    def __init__(self):
       
        super().__init__()

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
    
    def is_out_of_bounds(self, w,h):
        return (abs(self.ycor()) > h/2 or abs(self.xcor()) > w/2)
        