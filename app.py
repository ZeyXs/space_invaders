import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from utils import *
from classes import *

# Constantes
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

WIDTH, HEIGHT = 210, 264
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
        icon = pygame.image.load('./assets/textures/icon.png').convert_alpha()
        
        self.font_6 = pygame.font.Font("./assets/fonts/space_invaders.ttf", 6)
        self.font_8 = pygame.font.Font("./assets/fonts/space_invaders.ttf", 8)
        self.font_14 = pygame.font.Font("./assets/fonts/space_invaders.ttf", 24)

        self.logo = pygame.image.load('./assets/textures/title.png').convert_alpha()
        self.logo = pygame.transform.scale(self.logo,(193,83))

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

            # - Ennemis
        rang = 0
        for y in range(40, HEIGHT-130, 15):
            for x in range(25, WIDTH-30, 15):
                if rang==0:
                    self.enemies.append(Meduse(x+1.9, y))
                elif rang<=2:
                    self.enemies.append(Crabe(x+0.5, y))
                elif rang<=4:
                    self.enemies.append(Poulpe(x, y))
            rang+=1
            

    def run(self):

        self.menu_id = 0
        self.button_choice = 0
        self.button_choice2 = 0
        self.options = []

        while self.running:
            self.clock.tick(FPS)
            self.keys_pressed = pygame.key.get_pressed()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.button_choice -= 1
                            
                    elif event.key == pygame.K_DOWN:
                        self.button_choice += 1
                        
                    elif event.key == pygame.K_LEFT:
                        self.button_choice2 += 1
                    
                    elif event.key == pygame.K_RIGHT:
                        self.button_choice2 -= 1

            # --- MAIN MENU ---
            if self.menu_id == 0:
                # controls
                if self.keys_pressed[pygame.K_RETURN]:
                    # Player chooses PLAY
                    if self.button_choice == 0:
                        self.menu_id = 1
                    # Player chooses OPTIONS
                    if self.button_choice == 1:
                        self.menu_id = 2
                    # Player chooses CREDITS
                    if self.button_choice == 2:
                        self.menu_id = 3
                
                if self.button_choice < 0:
                    self.button_choice = 2

                if self.button_choice > 2:
                    self.button_choice = 0
            
            # --- IN-GAME ---
            elif self.menu_id == 1:
                # controls
                if self.keys_pressed[pygame.K_LEFT] and self.player.rect.x - 1 > 0:
                    self.player.rect.x -= 1
                if self.keys_pressed[pygame.K_RIGHT] and self.player.rect.x + 1 + self.player.image.get_rect().width < WIDTH:
                    self.player.rect.x += 1 
            
            # --- OPTIONS ---
            elif self.menu_id == 2:
                # controls
                    # options verticales
                if self.button_choice < 0:
                    self.button_choice = 2

                elif self.button_choice > 5:
                    self.button_choice = 0
                    # options horizontales
            
            
            self.draw_on_screen()
                    
        pygame.quit()
        sys.exit()
    
    
    def draw_on_screen(self):
        self.screen.fill(BLACK)

        # MAIN MENU
        if self.menu_id == 0:
            self.draw_main_menu()

        # IN-GAME
        elif self.menu_id == 1:
            self.draw_game()
            
        # OPTIONS
        elif self.menu_id == 2:
            self.draw_options()
        
        elif self.menu_id == 3:
            self.draw_credits()

        # Redimension de la fenêtre
        self.window.blit(pygame.transform.scale(self.screen, self.window.get_rect().size), (0, 0))
        pygame.display.flip()
        
        
    def draw_main_menu(self):
        # Display Game Icon
        self.screen.blit(self.logo,((WIDTH - self.logo.get_width())/2, 10))
            
        # Display text
        if self.button_choice == 0:
            self._draw_text("> JOUER <", WHITE, self.font_14, None, 150, True)
            self._draw_text("OPTIONS", WHITE, self.font_14, None, 170, True)
            self._draw_text("CREDITS", WHITE, self.font_14, None, 190, True)
        elif self.button_choice == 1:
            self._draw_text("JOUER", WHITE, self.font_14, None, 150, True)
            self._draw_text("> OPTIONS <", WHITE, self.font_14, None, 170, True)
            self._draw_text("CREDITS", WHITE, self.font_14, None, 190, True)
        elif self.button_choice == 2:
            self._draw_text("JOUER", WHITE, self.font_14, None, 150, True)
            self._draw_text("OPTIONS", WHITE, self.font_14, None, 170, True)
            self._draw_text("> CREDITS <", WHITE, self.font_14, None, 190, True)
    
    
    def draw_options(self):
        # Display text
        self.button_choice = 0
        if self.button_choice == 0:
            self._draw_text("> RETOUR <", WHITE, self.font_14, None, 60, True)
            self._draw_text("NOMBRE DE VIES :", WHITE, self.font_14, None, 80, True)
            self._draw_text("1 / 2 / 3 / 4 / 5", WHITE, self.font_14, None, 90, True)
            self._draw_text("VITESSE DES ENNEMIS :", WHITE, self.font_14, None, 110, True)
            self._draw_text("LENTE / MOYENNE / RAPIDE", WHITE, self.font_14, None, 120, True)
            self._draw_text("BOUCLIERS INCASSABLES :", WHITE, self.font_14, None, 140, True)
            self._draw_text("OUI / NON", WHITE, self.font_14, None, 150, True)
            self._draw_text("MODE RETRO :", WHITE, self.font_14, None, 170, True)
            self._draw_text("OUI / NON", WHITE, self.font_14, None, 180, True)
            self._draw_text("MUSIQUE :", WHITE, self.font_14, None, 200, True)
            self._draw_text("OUI / NON", WHITE, self.font_14, None, 210, True)
    
    
    def draw_credits(self):
    # Display text
        self.button_choice = 0
        if self.button_choice == 0:
            self._draw_text("> RETOUR <", WHITE, self.font_8, None, 60, True)
            self._draw_text("CREE PAR : BASILE GAUTTRON,", WHITE, self.font_8, None, 100, True)
            self._draw_text("ROBIN DEROCH,", WHITE, self.font_8, None, 110, True)
            self._draw_text("LAURE VAN LERBERGHE", WHITE, self.font_8, None, 120, True)
            self._draw_text("DEVELOPPE ORIGINALEMENT PAR :", WHITE, self.font_8, None, 140, True)
            self._draw_text("TAITO", WHITE, self.font_8, None, 150, True)
            self._draw_text("MUSIQUE: EVAN KING - WARNING", WHITE, self.font_8, None, 180, True)
            self._draw_text("https://youtu.be/M7Hw7g8bssY", WHITE, self.font_6, None, 192, True)
            self._draw_text("HTTPS://CONTEXTSENSITIVE.BANDCAMP.COM", WHITE, self.font_6 , None, 200, True)
        
    
    def draw_game(self):

        # Affichage du texte
        tmp_test_font = self.font_8.render("SCORE<1>    HI-SCORE    SCORE<2>", 0, WHITE)
        self.screen.blit(tmp_test_font, (WIDTH - tmp_test_font.get_width()*1.25, 10))
        
        # Affichage des entitées
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        self.player.update()

        for enemy in self.enemies:
            self.screen.blit(enemy.image, (enemy.rect.x,enemy.rect.y))
            enemy.update()
        
        
    def _draw_text(self, text, color, font, x, y, align_center=False):
        tmp_font = font.render(text, 0, color)
        if align_center:
            self.screen.blit(tmp_font, ((WIDTH - tmp_font.get_width())/2, y))
        else:
            self.screen.blit(tmp_font, (x,y))


if __name__ == "__main__":
    app = App()
    app.run()

