import pygame

class Entity(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = [pygame.image.load('./assets/textures/player.png').convert_alpha(),
                        pygame.image.load('./assets/textures/player.png').convert_alpha()]
        self.death_sprites = [pygame.image.load("./assets/textures/player_death_0.png").convert_alpha(),
                              pygame.image.load("./assets/textures/player_death_1.png").convert_alpha()]
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = pygame.Rect(12, 8, 12, 8)
        self.rect.topleft = [pos_x,pos_y]

    def update(self, direction):
        self.current_sprite += 0.015

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
            
        self.image = self.sprites[int(self.current_sprite)]
        
        self.rect.x += direction
        
    def move(self, pos_x, pos_y):
        self.rect.topleft = [pos_x, pos_y]
        
        
class Player(Entity, pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.sprites = [pygame.image.load('./assets/textures/player.png').convert_alpha(),
                        pygame.image.load('./assets/textures/player.png').convert_alpha()]
        self.death_sprites = [pygame.image.load("./assets/textures/player_death_0.png").convert_alpha(),
                              pygame.image.load("./assets/textures/player_death_1.png").convert_alpha()]
        
    def update(self):
        self.current_sprite += 0.015

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
            
        self.image = self.sprites[int(self.current_sprite)]
        
class Crabe(Entity, pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.sprites = [pygame.image.load('./assets/textures/crabe_0.png').convert_alpha(),
                        pygame.image.load('./assets/textures/crabe_1.png').convert_alpha()]
        self.death_sprites = [pygame.image.load("./assets/textures/enemy_explosion.png").convert_alpha(),
                              pygame.image.load("./assets/textures/enemy_explosion.png").convert_alpha()]
        
class Poulpe(Entity, pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.sprites = [pygame.image.load('./assets/textures/poulpe_0.png').convert_alpha(),
                        pygame.image.load('./assets/textures/poulpe_1.png').convert_alpha()]
        self.death_sprites = [pygame.image.load("./assets/textures/enemy_explosion.png").convert_alpha(),
                              pygame.image.load("./assets/textures/enemy_explosion.png").convert_alpha()]
        
class Meduse(Entity, pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.sprites = [pygame.image.load('./assets/textures/meduse_0.png').convert_alpha(),
                        pygame.image.load('./assets/textures/meduse_1.png').convert_alpha()]
        self.death_sprites = [pygame.image.load("./assets/textures/enemy_explosion.png").convert_alpha(),
                              pygame.image.load("./assets/textures/enemy_explosion.png").convert_alpha()]

class Projectile(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((2,5))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(center = (x, y))
        
    def update_enemy(self):
        self.rect.y += 2
        
    def update_player(self):
        self.rect.y -= 5
        
class Shield(pygame.sprite.Sprite):
    
    def __init__(self, size, x, y, color):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))

def get_shield_shape():
    with open("assets/shield_pattern.txt") as fd:
        shape_str = fd.read().split("\n")
        shape = list(zip(*shape_str))[::-1]
    return shape