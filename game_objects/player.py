import pygame as pg

'''
    fisierul care implementeaza functionalitatea obiectelor player
'''

class Player:
    width = 20
    height = 80

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.score = 0

    #se deseneaza un dreptunghi
    def render(self):
        pg.draw.rect(self.screen, (120, 120, 120), pg.Rect(self.x, self.y, 20, 80))

    def tick(self, dir, delta_time):
        self.y += dir * delta_time
