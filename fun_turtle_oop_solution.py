# turtle_invasion.py

import random
import time
import turtle

from aliens_solution import Enemy, Laser

WIDTH = 600
HEIGHT = 600

player_rotation_step = 0.5
spawn_interval_range = 1, 3
laser_speed = 1
total_ammunition = 100

# Initialise variables
enemies = []
lasers = []
score = 0

# Create Screen
screen = turtle.Screen()
screen.tracer(0)
screen.setup(WIDTH, HEIGHT)
screen.bgcolor(0.2, 0.2, 0.2)
screen.listen()

# Create player
player = turtle.Turtle()
player.shape("triangle")
player.shapesize(stretch_len=1.5)
player.color("purple")

player.rotation = 0
player.ammunition = total_ammunition

# Control player
def turn_left():
    player.rotation = player_rotation_step

def turn_right():
    player.rotation = -player_rotation_step

def stop_turning():
    player.rotation = 0

screen.onkeypress(turn_left, "Left")
screen.onkeyrelease(stop_turning, "Left")
screen.onkeypress(turn_right, "Right")
screen.onkeyrelease(stop_turning, "Right")

# Shoot lasers
def shoot_laser():
    laser = Laser(player)
    laser.set_speed(laser_speed)
    lasers.append(laser)
    player.ammunition -= 1
    if not player.ammunition:
        screen.onkeypress(None, "space")

screen.onkeypress(shoot_laser, "space")

# Deal with out-of-bounds objects
def cleanup_entity(entity, entities_list):
    entity.hideturtle()
    entity.clear()
    screen.update()
    entities_list.remove(entity)
    turtle.turtles().remove(entity)

# Main game loop
start_enemy_spawn_timer = time.time()
next_enemy_spawn_delay = 0
while player.ammunition > 0 or lasers:
    screen.title(
        f"Ammunition: {player.ammunition} "
        f"| Score: {int(score):3}"
    )
    player.left(player.rotation)

    # Spawn new enemy if time interval elapsed
    if (
        time.time() - start_enemy_spawn_timer
        > next_enemy_spawn_delay
    ):
        new_enemy = Enemy()
        enemies.append(new_enemy)
        new_enemy.set_start_position(WIDTH, HEIGHT)
        next_enemy_spawn_delay = random.uniform(
            *spawn_interval_range
        )
        start_enemy_spawn_timer = time.time()

    # Move enemies
    for enemy in enemies.copy():
        enemy.move()
        enemy.change_direction()
        if enemy.is_out_of_bounds(WIDTH, HEIGHT):
            cleanup_entity(enemy, enemies)
            
    # Move lasers
    for laser in lasers.copy():
        laser.move()
        if laser.is_out_of_bounds(WIDTH, HEIGHT):
            cleanup_entity(laser, lasers)
        # check for collisions
        for enemy in enemies:
            if laser.has_collided_with(enemy):
                score += enemy.enemy_speed
                cleanup_entity(enemy, enemies)
                cleanup_entity(laser, lasers)
                
    screen.update()
    # print(len(enemies), len(lasers), len(turtle.turtles()))

turtle.done()