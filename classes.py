import pygame

class Player:

    def __init__(self, rect, texture):
        self.rect = rect
        self.texture = texture

class Enemy:

    def __init__(self, type, rect, texture, speed):
        self.type = type
        self.rect = rect
        self.texture = texture
        self.speed = speed

class Projectile:

    def __init__(self, rect, texture, speed, team):
        self.rect = rect
        self.texture = texture
        self.speed = speed
        self.team = team
        
class Team:
    PLAYER = 0
    ENEMY = 1
    
class Type:
    MEDUSE = 0
    CRABE = 1
    POULPE = 2