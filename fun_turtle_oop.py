# Fun tutrle OOP project

import random 
import time
import turtle


from aliens import Enemy

#General setup
w = 600
h = 600

player_rot_step = 10
spawn_interval_range = 1,3

enemies = []

#create screen
screen = turtle.Screen()
screen.tracer(0)
screen.setup(w,h)
screen.bgcolor("black")
screen.listen()

player = turtle.Turtle()
player.shape("triangle")
player.shapesize(stretch_len=1.5)
player.color("purple")

player.rotation = 0

def turn_left():
    player.rotation = player_rot_step

def turn_right():
    player.rotation = -player_rot_step

def stop_turning():
    player.rotation = 0

screen.onkeypress(turn_left, 'Left')
screen.onkeyrelease(stop_turning, 'Left')
screen.onkeypress(turn_right, 'Right')
screen.onkeyrelease(stop_turning, 'Right')

#Main game loop
start_enemy_spawn_timer = time.time()
next_enemy_spawn_delay = 0 

while True:

    player.left(player.rotation)

    if (
            time.time() - start_enemy_spawn_timer
            > next_enemy_spawn_delay
        ):
           
            new_enemy = Enemy()
            enemies.append(new_enemy)
            new_enemy.set_start_position(w, h)
        
            next_enemy_spawn_delay = random.uniform( *spawn_interval_range)
        
            start_enemy_spawn_timer = time.time()

    for enemy in enemies.copy():
        enemy.move()
        enemy.change_direction()
        if enemy.is_out_of_bounds(w, h):
            enemy.hideturtle()
            screen.update()
            enemies.remove(enemy)
    screen.update()
        
        
