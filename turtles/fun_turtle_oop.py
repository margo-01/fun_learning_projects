# Fun tutrle OOP project

import random 
import time
import turtle


from aliens import Enemy, Laser

player = turtle.Turtle()
player.shape("triangle")
player.shapesize(stretch_len=1.5)
player.color("purple")



def turn_left():
    player.rotation = player_rot_step

def turn_right():
    player.rotation = -player_rot_step

def stop_turning():
    player.rotation = 0

def shoot_laser():
    laser = Laser(player)
    laser.set_speed(laser_speed)
    lasers.append(laser)
    player.ammunition -= 1
    if not player.ammunition:
        screen.onkey(None, 'space')

def cleanup_entity(entity, entities_list):
        entity.hideturtle()
        entity.clear()
        screen.update()
        entities_list.remove(entity)
        turtle.turtles().remove(entity)
    

#create screen

w = 600
h = 600

screen = turtle.Screen()
screen.tracer(0)
screen.setup(w,h)
screen.bgcolor("black")
screen.listen()

screen.onkeypress(turn_left, 'Left')
screen.onkeyrelease(stop_turning, 'Left')
screen.onkeypress(turn_right, 'Right')
screen.onkeyrelease(stop_turning, 'Right')
screen.onkeypress(shoot_laser, "space")

#General setup


player_rot_step = 0.5
spawn_interval_range = 1,3
laser_speed = 1
total_ammunition = 100
player.rotation = 0


enemies = []
lasers = []
score = 0



player.ammunition = total_ammunition


#Main game loop
start_enemy_spawn_timer = time.time()
next_enemy_spawn_delay = 0 

while True:
    screen.title(f'Score: {int(score):3}'
                 f'| Ammunition: {player.ammunition}')
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
            cleanup_entity(enemy, enemies)
    
    for laser in lasers.copy():
        laser.move()
        if laser.is_out_of_bounds(w,h):
            cleanup_entity(laser, lasers)
        
        for enemy in enemies:
            if laser.has_collided_with(enemy):
                score += enemy.enemy_speed
                cleanup_entity(enemy, enemies)
                cleanup_entity(laser,lasers)
                
    
    screen.update()
   # print(len(enemies), len(lasers), len(turtle.turtles()))
        
