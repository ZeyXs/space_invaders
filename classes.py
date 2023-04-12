import pygame
import utils

class Entity(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = [pygame.image.load('./assets/textures/player.png').convert_alpha(),
                        pygame.image.load('./assets/textures/player.png').convert_alpha()]
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.direction_timer = 0
        
        self.rect = pygame.Rect(12, 8, 12, 8)
        self.rect.topleft = [pos_x,pos_y]

    def update(self, enemies_alive):
        self.current_sprite += (0.8/enemies_alive)
        print(self.current_sprite)

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
            
        self.image = self.sprites[int(self.current_sprite)]

    def move_down(self, direction):
        self.rect.y += 4
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
    
    def __init__(self, pos_x, pos_y, retro_mode):
        super().__init__(pos_x, pos_y)
        self.sprites = [pygame.image.load('./assets/textures/crabe_0.png').convert_alpha(),
                        pygame.image.load('./assets/textures/crabe_1.png').convert_alpha()]
        self.death_sprites = [pygame.image.load("./assets/textures/enemy_explosion.png").convert_alpha(),
                              pygame.image.load("./assets/textures/enemy_explosion.png").convert_alpha()]
                
        if not retro_mode:
            utils.replace_color(self.sprites[0], (0, 255, 255))
            utils.replace_color(self.sprites[1], (0, 255, 255))
            
    def update(self, direction, enemies_alive, speed):
        super().update(enemies_alive)
        self.direction_timer += 1
        if self.direction_timer >= (12*enemies_alive)//55:
            self.direction_timer = 0
            self.rect.x += direction * (1 if speed == 1 else 1.5 if speed == 2 else 2)
        
class Poulpe(Entity, pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y, retro_mode):
        super().__init__(pos_x, pos_y)
        self.sprites = [pygame.image.load('./assets/textures/poulpe_0.png').convert_alpha(),
                        pygame.image.load('./assets/textures/poulpe_1.png').convert_alpha()]
        self.death_sprites = [pygame.image.load("./assets/textures/enemy_explosion.png").convert_alpha(),
                              pygame.image.load("./assets/textures/enemy_explosion.png").convert_alpha()]
        
        if not retro_mode:
            utils.replace_color(self.sprites[0], (255, 0, 255))
            utils.replace_color(self.sprites[1], (255, 0, 255))
            
    def update(self, direction, enemies_alive, speed):
        super().update(enemies_alive)
        self.direction_timer += 1
        if self.direction_timer >= (12*enemies_alive)//55:
            self.direction_timer = 0
            self.rect.x += direction * (1 if speed == 1 else 1.5 if speed == 2 else 2)
        
class Meduse(Entity, pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y, retro_mode):
        super().__init__(pos_x, pos_y)
        self.sprites = [pygame.image.load('./assets/textures/meduse_0.png').convert_alpha(),
                        pygame.image.load('./assets/textures/meduse_1.png').convert_alpha()]
        self.death_sprites = [pygame.image.load("./assets/textures/enemy_explosion.png").convert_alpha(),
                              pygame.image.load("./assets/textures/enemy_explosion.png").convert_alpha()]
        
        if not retro_mode:
            utils.replace_color(self.sprites[0], (255, 255, 0))
            utils.replace_color(self.sprites[1], (255, 255, 0))
            
    def update(self, direction, enemies_alive, speed):
        super().update(enemies_alive)
        self.direction_timer += 1
        if self.direction_timer >= (12*enemies_alive)//55:
            self.direction_timer = 0
            self.rect.x += direction * (1 if speed == 1 else 1.5 if speed == 2 else 2)
            print(direction * (1 if speed == 1 else 1.5 if speed == 2 else 2))

class VaisseauMere(Entity, pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, retro_mode):
        super().__init__(pos_x, pos_y)
        self.sprites = [pygame.image.load('./assets/textures/mothership.png').convert_alpha()]
        self.death_sprites = [pygame.image.load("./assets/textures/mothership_explosion.png").convert_alpha()]
        
        if not retro_mode:
            utils.replace_color(self.sprites[0], (255, 0, 0))

    def update(self):
        self.image = self.sprites[int(self.current_sprite)]

    def move(self, direction):
        if direction == 1:
            self.rect.x += 1
        else:
            self.rect.x -= 1

class Projectile(pygame.sprite.Sprite):

    def __init__(self, x, y, enemy_shot):
        super().__init__()
        if enemy_shot == False:
            self.image = pygame.Surface((2,5))
            self.image.fill((255,255,255))
            self.rect = self.image.get_rect(center = (x, y))
        else:
            self.sprites = [pygame.image.load('./assets/textures/emissile_0.png').convert_alpha(),
                        pygame.image.load('./assets/textures/emissile_1.png').convert_alpha(),
                        pygame.image.load('./assets/textures/emissile_2.png').convert_alpha()]
            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]
            self.rect = self.image.get_rect(center = (x, y))
        
    def update_enemy(self):
        self.rect.y += 2

        self.current_sprite += 0.05
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        
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