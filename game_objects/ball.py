import pygame as pg
import random
import math

'''
    fisierul care implementeaza functionalitatea obiectului minge
'''

class Ball:
    radius = 10
    speed = 400

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

        #se seteaza un unghi random pentru inceput pentru bila
        angle = random.randint(140, 220)
        dir = random.randint(1, 2)

        if dir == 2:
            angle += 180

        self.speed_x = math.cos(math.radians(angle)) * self.speed 
        self.speed_y = math.sin(math.radians(angle)) * self.speed

    #se deseneaza un cerc
    def render(self):
        pg.draw.circle(self.screen, (180, 180, 180), (int(self.x + self.radius / 2), int(self.y + self.radius / 2)), self.radius)

    def tick(self, delta_time):
        self.x += self.speed_x * delta_time
        self.y += self.speed_y * delta_time