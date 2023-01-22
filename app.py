import pygame, os, sys
from utils import *
from classes import *

# Constantes
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

WIDTH, HEIGHT = 256, 224
FPS = 60
SCALING_FACTOR = 3




class App:

    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        
        # Initialisation de la fenêtre
        self.window = pygame.display.set_mode((WIDTH*SCALING_FACTOR, HEIGHT*SCALING_FACTOR))
        self.screen = pygame.Surface((WIDTH, HEIGHT))

        self.player_img = pygame.image.load("./assets/textures/player.png").convert_alpha()
        self.crabe_0_img = pygame.image.load("./assets/textures/crabe_0.png").convert_alpha()
        icon = pygame.image.load('./assets/textures/icon.png').convert_alpha()

        pygame.display.set_icon(icon)
        pygame.display.set_caption("Space Invaders v0.1")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Importation de la font
        self.font = pygame.font.Font("./assets/fonts/space_invaders.ttf", 8)

        # Variables in-game
        self.in_main_menu = True
        self.enemies = []
        
        # Création des entités
        self.player = Player(gen_rect(WIDTH/2-(self.player_img.get_width()/2), 201, self.player_img), self.player_img)
        for y in range(10, HEIGHT-50, 10):
            for x in range(10, WIDTH-10, 10):
                self.enemies.append(Enemy(Type.CRABE, gen_rect(x, y, self.crabe_0_img), self.crabe_0_img, 5))
                
    
    # Lancement de l'application
    def run(self):
        
        while self.running:
            self.clock.tick(FPS)

            self.keys_pressed = pygame.key.get_pressed()
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass                
                    
            self.dos()
                    
        pygame.quit()
        sys.exit()
    

    # Update de la fenêtre - Draw on screen
    def dos(self):
        self.screen.fill(BLACK)

        # Affichage du texte
        tmp_test_font = self.font.render("HI-SCORE <1>", 0, WHITE)
        self.screen.blit(tmp_test_font, (WIDTH - tmp_test_font.get_width() - 10, 10))
        
        # Affichage des entitées
        self.screen.blit(self.player.texture, (self.player.rect.x, self.player.rect.y))
        for enemy in self.enemies:
            self.screen.blit(enemy.texture, (enemy.rect.x,enemy.rect.y))

        # Redimension de la fenêtre
        self.window.blit(pygame.transform.scale(self.screen, self.window.get_rect().size), (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()

