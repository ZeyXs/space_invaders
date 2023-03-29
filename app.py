import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from utils import *
from classes import *
from config import *

# Constantes
WHITE = (230,230,230)
GRAY = (190, 190, 190)
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
        self.config = Config("assets/config.json")
                
        self.window = pygame.display.set_mode((WIDTH*SCALING_FACTOR, HEIGHT*SCALING_FACTOR))
        self.screen = pygame.Surface((WIDTH, HEIGHT))

        # Importation des textures
        icon = pygame.image.load('./assets/textures/icon.png').convert_alpha()
        
        self.font_6 = pygame.font.Font("./assets/fonts/space_invaders.ttf", 6)
        self.font_8 = pygame.font.Font("./assets/fonts/space_invaders.ttf", 8)
        self.font_14 = pygame.font.Font("./assets/fonts/space_invaders.ttf", 16)

        self.logo = pygame.image.load('./assets/textures/title.png').convert_alpha()
        self.logo = pygame.transform.scale(self.logo,(193,83))

        # Esthétique fenêtre
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Space Invaders v0.1")

        # Variables in-game
        self.in_main_menu = True
        self.enemies = []

        self.clock = pygame.time.Clock()
        self.running = True
        self.is_init = False
        self.x_group = -1
                    
        self.shield_size = 1
        self.shields = pygame.sprite.Group()
        self.shield_amount = 4
        self.shield_x_positions = [num * (WIDTH / self.shield_amount-10) for num in range(self.shield_amount)]
        print(self.shield_x_positions)
        self.create_multiple_shield(*self.shield_x_positions, x_start = 32, y_start = 180)
        
        self.dy = 0.09
        self.vy = 0
        
        self.options = [None, "option.number_of_life", "option.ennemies_speed", "option.unbreakable_shield", "option.retro_mode", "option.music"]

    def run(self):

        self.menu_id = 0
        # Aide :
        #   - 0 = Main Menu
        #   - 1 = In-Game
        #   - 2 = Options
        #   - 3 = Credits

        self.pointeur_vert = 0
        self.pointeur_hori = 1
        
        while self.running:
            self.clock.tick(FPS)
            self.keys_pressed = pygame.key.get_pressed()
            
            if self.menu_id == 0 or self.menu_id == 3:
                self.current_menu_options = [[0],[0],[0]]

            elif self.menu_id == 2:
                self.current_menu_options = [[0], [1,2,3,4], [1,2,3], [True,False], [True,False], [True,False]]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.pointeur_vert -= 1
                        if self.pointeur_vert < 0:
                            self.pointeur_vert = len(self.current_menu_options)-1
                        if self.menu_id == 2:
                            if self.options[self.pointeur_vert] != None:
                                self.pointeur_hori = self.config.get(self.options[self.pointeur_vert])

                    elif event.key == pygame.K_DOWN:
                        self.pointeur_vert += 1
                        if self.pointeur_vert > len(self.current_menu_options)-1:
                            self.pointeur_vert = 0
                        if self.menu_id == 2:
                            if self.options[self.pointeur_vert] != None:
                                self.pointeur_hori = self.config.get(self.options[self.pointeur_vert])
                        
                    elif event.key == pygame.K_LEFT:
                        if self.menu_id == 2:
                            self.pointeur_hori -= 1
                            if self.pointeur_hori < 0:
                                self.pointeur_hori = len(self.current_menu_options[self.pointeur_vert])-1
                    
                    elif event.key == pygame.K_RIGHT:
                        if self.menu_id == 2:
                            self.pointeur_hori += 1
                            if self.pointeur_hori > len(self.current_menu_options[self.pointeur_vert])-1:
                                self.pointeur_hori = 0
                    
                    elif event.key == pygame.K_RETURN:
                        # Touche RETURN pour le menu principal
                        if self.menu_id == 0:
                            if self.pointeur_vert == 0:
                                self.menu_id = 1
                            elif self.pointeur_vert == 1:
                                self.menu_id = 2
                            elif self.pointeur_vert == 2:
                                self.menu_id = 3
                            self.pointeur_vert = 0
                            
                        # Touche RETURN pour le menu des options
                        elif self.menu_id == 2:
                            if self.pointeur_vert == 0:
                                self.menu_id = 0
                            if self.options[self.pointeur_vert] != None:
                                selected_option = self.options[self.pointeur_vert]
                                if selected_option == "option.number_of_life":
                                    self.config.put("option.number_of_life", self.current_menu_options[self.pointeur_vert][self.pointeur_hori-1])
                                elif selected_option == "option.ennemies_speed":
                                    self.config.put("option.ennemies_speed", self.current_menu_options[self.pointeur_vert][self.pointeur_hori-1])
                                elif selected_option == "option.unbreakable_shield":
                                    self.config.put("option.unbreakable_shield", self.current_menu_options[self.pointeur_vert][self.pointeur_hori-1])
                                elif selected_option == "option.retro_mode":
                                    self.config.put("option.retro_mode", self.current_menu_options[self.pointeur_vert][self.pointeur_hori-1])
                                else:
                                    self.config.put("option.music", self.current_menu_options[self.pointeur_vert][self.pointeur_hori-1])

            # --- IN-GAME ---
            if self.menu_id == 1:
                # controls
                if self.keys_pressed[pygame.K_LEFT] and self.player.rect.x - 1 > 0:
                    self.player.rect.x -= 1
                if self.keys_pressed[pygame.K_RIGHT] and self.player.rect.x + 1 + self.player.image.get_rect().width < WIDTH:
                    self.player.rect.x += 1
                if self.keys_pressed[pygame.K_SPACE] and self.player_projectile == None :
                    self.player_projectile=Projectile((self.player.rect.x + (0.5*self.player.rect.width)) ,self.player.rect.y)
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
        self.screen.blit(self.logo,((WIDTH - self.logo.get_width())/2, 20 + self.vy))
        
        self.vy += self.dy
        if self.vy > 5 or self.vy < -5:
            self.dy *= -1
        
        menu = [["> JOUER <","OPTIONS","CREDITS"],["JOUER","> OPTIONS <","CREDITS"],["JOUER","OPTIONS","> CREDITS <"]]    
        # Display text
        for i in range(3):
            self._draw_text(menu[self.pointeur_vert][i], WHITE, self.font_14, None, 140+(i*30), True)
    
    
    def draw_options(self):
        # Display text
        
        # RETOUR
        self._draw_text("> RETOUR <" if self.pointeur_vert == 0 else "RETOUR", WHITE, self.font_8, None, 60, True)
        
        # NOMBRES DE VIES
        self._draw_text("> NOMBRE DE VIES : <" if self.pointeur_vert == 1 else "NOMBRE DE VIES :", WHITE, self.font_8, None, 80, True)
        if self.pointeur_vert == 1:
            if self.pointeur_hori == 1:
                self._draw_text("[ 1 ] / 2 / 3 / 4", GRAY, self.font_8, None, 90, True)
            elif self.pointeur_hori == 2:
                self._draw_text("1 / [ 2 ] / 3 / 4", GRAY, self.font_8, None, 90, True)
            elif self.pointeur_hori == 3:
                self._draw_text("1 / 2 / [ 3 ] / 4", GRAY, self.font_8, None, 90, True)
            else:
                self._draw_text("1 / 2 / 3 / [ 4 ]", GRAY, self.font_8, None, 90, True)
        else:
            choice = self.config.get("option.number_of_life")
            if choice == 1:
                self._draw_text("[ 1 ] / 2 / 3 / 4", GRAY, self.font_8, None, 90, True)
            elif choice == 2:
                self._draw_text("1 / [ 2 ] / 3 / 4", GRAY, self.font_8, None, 90, True)
            elif choice == 3:
                self._draw_text("1 / 2 / [ 3 ] / 4", GRAY, self.font_8, None, 90, True)
            else:
                self._draw_text("1 / 2 / 3 / [ 4 ]", GRAY, self.font_8, None, 90, True)
                        
        # VITESSE DES ENNEMIS
        self._draw_text("> VITESSE DES ENNEMIS : <" if self.pointeur_vert == 2 else "VITESSE DES ENNEMIS :", WHITE, self.font_8, None, 110, True)
        if self.pointeur_vert == 2:
            if self.pointeur_hori == 1:
                self._draw_text("[ LENT ] / MOYEN / RAPIDE", GRAY, self.font_8, None, 120, True)
            elif self.pointeur_hori == 2:
                self._draw_text("LENT / [ MOYEN ] / RAPIDE", GRAY, self.font_8, None, 120, True)
            else:
                self._draw_text("LENT / MOYEN / [ RAPIDE ]", GRAY, self.font_8, None, 120, True)
        else:
            choice = self.config.get("option.ennemies_speed")
            if choice == 1:
                self._draw_text("[ LENT ] / MOYEN / RAPIDE", GRAY, self.font_8, None, 120, True)
            elif choice == 2:
                self._draw_text("LENT / [ MOYEN ] / RAPIDE", GRAY, self.font_8, None, 120, True)
            else:
                self._draw_text("LENT / MOYEN / [ RAPIDE ]", GRAY, self.font_8, None, 120, True)

        # BOUCLIERS INCASSABLES
        self._draw_text("> BOUCLIERS INCASSABLES : <" if self.pointeur_vert == 3 else "BOUCLIERS INCASSABLES :", WHITE, self.font_8, None, 140, True)
        if self.pointeur_vert == 3:
            self._draw_text("[ OUI ] / NON" if self.pointeur_hori == 1 else "OUI / [ NON ]", GRAY, self.font_8, None, 150, True)
        else:
            choice = self.config.get("option.unbreakable_shield")
            self._draw_text("[ OUI ] / NON" if choice else "OUI / [ NON ]", GRAY, self.font_8, None, 150, True)
                
        
        # MODE RETRO
        self._draw_text("> MODE RETRO : <" if self.pointeur_vert == 4 else "MODE RETRO :", WHITE, self.font_8, None, 170, True)
        if self.pointeur_vert == 4:
            self._draw_text("[ OUI ] / NON" if self.pointeur_hori == 1 else "OUI / [ NON ]", GRAY, self.font_8, None, 180, True)
        else:
            choice = self.config.get("option.retro_mode")
            self._draw_text("[ OUI ] / NON" if choice else "OUI / [ NON ]", GRAY, self.font_8, None, 180, True)
        
        # MUSIQUE
        self._draw_text("> MUSIQUE : <" if self.pointeur_vert == 5 else "MUSIQUE :", WHITE, self.font_8, None, 200, True)
        if self.pointeur_vert == 5:
            self._draw_text("[ OUI ] / NON" if self.pointeur_hori == 1 else "OUI / [ NON ]", GRAY, self.font_8, None, 210, True)
        else:
            choice = self.config.get("option.music")
            self._draw_text("[ OUI ] / NON" if choice else "OUI / [ NON ]", GRAY, self.font_8, None, 210, True)

    
    def draw_credits(self):
        # Display text
        str_credits = [
            ["> RETOUR <",self.font_8,60],
            ["CREE PAR : BASILE GAUTTRON,",self.font_8,100],
            ["ROBIN DEROCH,",self.font_8, 110],
            ["LAURE VAN LERBERGHE",self.font_8,120],
            ["DEVELOPPE ORIGINALEMENT PAR :",self.font_8,140],
            ["TAITO",self.font_8,150],
            ["MUSIQUE: EVAN KING - WARNING",self.font_8,180],
            ["https://youtu.be/M7Hw7g8bssY",self.font_6,191],
            ["HTTPS://CONTEXTSENSITIVE.BANDCAMP.COM",self.font_6,200]
        ]
        self.button_choice = 0
        if self.button_choice == 0:
            for i in range(9):
                self._draw_text(str_credits[i][0], WHITE, str_credits[i][1] , None, str_credits[i][2], True)
        
        
    def game_init(self):
        # Création des entités
            # - Joueur
        self.player = Player(0, 0)
        self.player.move(WIDTH/2-(self.player.image.get_width()/2), 201)
            # - Projectiles
        self.ennemi_projectile=None
        self.player_projectile=None

            # - Ennemis
        rang = 0
        for y in range(40, HEIGHT-130, 15):
            for x in range(25, WIDTH-30, 15):
                if rang == 0:
                    self.enemies.append(Meduse(x+1.9, y))
                elif rang <= 2:
                    self.enemies.append(Crabe(x+0.5, y))
                elif rang <= 4:
                    self.enemies.append(Poulpe(x, y))
            rang += 1
            
    
    def draw_game(self):
        
        if not self.is_init:
            self.game_init()
            self.is_init = True

        # Affichage du texte
        self._draw_text("SCORE<1>    HI-SCORE<2>", WHITE, self.font_8, None, 10, True)
        
        # Affichage des entitées
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        self.player.update()
        
        # Affichage des boucliers
        self.shields.draw(self.screen)     

        for enemy in self.enemies:
            self.screen.blit(enemy.image, (enemy.rect.x,enemy.rect.y))
            enemy.update()
            
        # Affichage des projectiles
        if self.player_projectile != None and self.player_projectile.rect.y > 0:
            self.screen.blit(self.player_projectile.image, (self.player_projectile.rect.x , self.player_projectile.rect.y ))
            
        else:
            self.player_projectile = None
            
        if self.ennemi_projectile != None and self.ennemi_projectile.rect.y < HEIGHT:
            self.screen.blit(self.ennemi_projectile.image , (self.ennemi_projectile.rect.x , self.ennemi_projectile.rect.y ))
        
        else: 
            self.ennemi_projectile = None
                
        # enemies moving
        """
        for enemy in self.enemies:

            if enemy.rect.x == 0: # Si collision gauche
                self.x_group = 1
            
            if (enemy.rect.x + enemy.rect.width) == WIDTH: # Si collision droite
                self.x_group = -1

            enemy.rect.x += self.x_group
        """
            
        #Projectiles moving  
        
        if self.player_projectile != None:
            self.player_projectile.update_player()
            
        if self.player_projectile != None:
            pass
            #self.ennemi_projectile.update_ennemi()


    def save_into_json(self, elm):
        self.config.put(elm, self.current_menu_options[self.pointeur_vert][self.pointeur_hori])

    def get_index_from_json(self, elm):
        self.alt_value = self.config.get(elm)
        self.index_vert = self.options_list.index(elm)
        self.index_hori = self.current_menu_options[self.index_vert].index(elm)
        
    def create_shield(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(get_shield_shape()):
            for col_index,col in enumerate(row):
                if col == '*':
                    x = x_start + col_index * self.shield_size + offset_x
                    y = y_start + row_index * self.shield_size
                    shield = Shield(self.shield_size, x, y)
                    self.shields.add(shield)
                    
    def create_multiple_shield(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_shield(x_start, y_start, offset_x)
        
        
    def _draw_text(self, text, color, font, x, y, align_center=False):
        tmp_font = font.render(text, 0.2, color)
        if align_center:
            self.screen.blit(tmp_font, ((WIDTH - tmp_font.get_width())/2, y))
        else:
            self.screen.blit(tmp_font, (x,y))

if __name__ == "__main__":
    app = App()
    app.run()

