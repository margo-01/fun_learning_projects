import math
import random
import time
import turtle

class OutOfBoundsMixin:
    def is_out_of_bounds(self, screen_width, screen_height):
        return (
            abs(self.xcor()) > screen_width / 2
            or abs(self.ycor()) > screen_height / 2
        )
class Enemy(turtle.Turtle, OutOfBoundsMixin):
    SPEED_RANGE = 0.1, 1
    MAX_TURN_ANGLE = 90
    TURNING_PERIOD_RANGE = 0.5, 2
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.color(
            random.random(),
            random.random(),
            random.random(),
        )
        self.left(random.randint(1, 359))
        self.enemy_speed = random.uniform(*self.SPEED_RANGE)
        self.turning_period = random.uniform(
            *self.TURNING_PERIOD_RANGE
        )
        self.start_timer = time.time()
    def move(self):
        self.forward(self.enemy_speed)
    def set_start_position(self, screen_width, screen_height):
        self.backward(
            math.sqrt(
                (screen_width / 2) ** 2
                + (screen_height / 2) ** 2
            )
        )
        if self.ycor() > screen_height / 2:
            self.sety(screen_height / 2)
        if self.ycor() < -screen_height / 2:
            self.sety(-screen_height / 2)
        if self.xcor() > screen_width / 2:
            self.setx(screen_width / 2)
        if self.xcor() < -screen_width / 2:
            self.setx(-screen_width / 2)
    def change_direction(self):
        if (
                time.time() - self.start_timer
                > self.turning_period
        ):
            self.left(
                random.uniform(
                    -self.MAX_TURN_ANGLE,
                    self.MAX_TURN_ANGLE,
                )
            )
            self.start_timer = time.time()
class Laser(turtle.Turtle, OutOfBoundsMixin):
    LENGTH = 10
    THICKNESS = 5
    DEFAULT_SPEED = 1
    COLLISION_TOLERANCE = 20  # Default diameter for turtles
    def __init__(self, player):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("red")
        self.pensize(self.THICKNESS)
        self.setposition(player.position())
        self.setheading(player.heading())
        self.laser_speed = self.DEFAULT_SPEED
    def set_speed(self, speed):
        self.laser_speed = speed
    def _draw(self):
        self.clear()
        self.pendown()
        self.forward(self.LENGTH)
        self.forward(-self.LENGTH)
        self.penup()
    def move(self):
        self.forward(self.laser_speed)
        self._draw()
    def has_collided_with(self, entity):
        return (
            self.distance(entity) <= self.COLLISION_TOLERANCE
        )