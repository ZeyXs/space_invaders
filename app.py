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

# Application / Code du Jeu
class App:

    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        
        # Initialisation de la fenêtre
        self.window = pygame.display.set_mode((WIDTH*SCALING_FACTOR, HEIGHT*SCALING_FACTOR))
        self.screen = pygame.Surface((WIDTH, HEIGHT))

        # Importation des textures
            # - Sprites
        self.player_img = pygame.image.load("./assets/textures/player.png").convert_alpha()
        self.crabe_0_img = pygame.image.load("./assets/textures/crabe_0.png").convert_alpha()
        self.crabe_1_img = pygame.image.load("./assets/textures/crabe_1.png").convert_alpha()
        self.meduse_0_img = pygame.image.load("./assets/textures/meduse_0.png").convert_alpha()
        self.meduse_1_img = pygame.image.load("./assets/textures/meduse_1.png").convert_alpha()
        self.poulpe_0_img = pygame.image.load("./assets/textures/poulpe_0.png").convert_alpha()
        self.poulpe_1_img = pygame.image.load("./assets/textures/poulpe_1.png").convert_alpha()

            # - Icon
        icon = pygame.image.load('./assets/textures/icon.png').convert_alpha()
            # - Font
        self.font = pygame.font.Font("./assets/fonts/space_invaders.ttf", 8)

        # Esthétique fenêtre
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Space Invaders v0.1")

        # Variables in-game
        self.in_main_menu = True
        self.enemies = []

        # Clefs de contact (nom temporaire, ou pas...)
        self.clock = pygame.time.Clock()
        self.running = True
        

        # Création des entités
            # - Joueur
        self.player = Player(0, 0)
        self.player.move(WIDTH/2-(self.player.image.get_width()/2), 201)
        #self.player = Player(gen_rect(WIDTH/2-(self.player_img.get_width()/2), 201, self.player_img), self.player_img)

            # - Ennemis
        rang = 0
        for y in range(30, HEIGHT-130, 15):
            for x in range(30, WIDTH-100, 15):
                if rang==0:
                    self.enemies.append(Meduse(x+1.9, y))
                elif rang<=2:
                    self.enemies.append(Crabe(x+0.5, y))
                elif rang<=4:
                    self.enemies.append(Poulpe(x, y))
            rang+=1
            
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
                    
            self.draw_on_screen()
                    
        pygame.quit()
        sys.exit()
    

    # Update de la fenêtre - Draw on screen
    def draw_on_screen(self):
        self.screen.fill(BLACK)

        # Affichage du texte
        tmp_test_font = self.font.render("SCORE<1> HI-SCORE SCORE<2>", 0, WHITE)
        self.screen.blit(tmp_test_font, (WIDTH - tmp_test_font.get_width() - 100, 10))
        
        # Affichage des entitées
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        self.player.update()

        for enemy in self.enemies:
            self.screen.blit(enemy.image, (enemy.rect.x,enemy.rect.y))
            enemy.update()
        

        # Redimension de la fenêtre
        self.window.blit(pygame.transform.scale(self.screen, self.window.get_rect().size), (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()

