import pygame

class Entity(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        
        self.sprites = [pygame.image.load('./assets/textures/player.png').convert_alpha(),
                        pygame.image.load('./assets/textures/player.png').convert_alpha()]
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]

    def update(self):
        self.current_sprite += 0.015

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
            
        
        self.image = self.sprites[int(self.current_sprite)]
        
    def move(self, pos_x, pos_y):
        self.rect.topleft = [pos_x, pos_y]
        
class Player(Entity, pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.sprites = [pygame.image.load('./assets/textures/player.png').convert_alpha(),
                           pygame.image.load('./assets/textures/player.png').convert_alpha()]
        
class Crabe(Entity, pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.sprites = [pygame.image.load('./assets/textures/crabe_0.png').convert_alpha(),
                           pygame.image.load('./assets/textures/crabe_1.png').convert_alpha()]
        
class Poulpe(Entity, pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.sprites = [pygame.image.load('./assets/textures/poulpe_0.png').convert_alpha(),
                           pygame.image.load('./assets/textures/poulpe_1.png').convert_alpha()]
        
class Meduse(Entity, pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.sprites = [pygame.image.load('./assets/textures/meduse_0.png').convert_alpha(),
                           pygame.image.load('./assets/textures/meduse_1.png').convert_alpha()]

class Projectile:

    def __init__(self, rect, texture, speed, team):
        self.rect = rect
        self.texture = texture
        self.speed = speed
        self.team = team
        
class Team:
    PLAYER = 0
    ENEMY = 1
    
#class Bouclier:
