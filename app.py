import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import random
import pygame
from copy import deepcopy


from utils import *
from classes import *
from config import *

# _______________________ Constantes _______________________
WHITE = (230,230,230)
GRAY = (190, 190, 190)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

WIDTH, HEIGHT = 210, 264
FPS = 60
SCALING_FACTOR = 3

# _______________ Application / Code du Jeu ________________
class App:

    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        
        # _____ Initialisation de la fenêtre _____
        self.config = Config("assets/config.json")
                
        self.window = pygame.display.set_mode((WIDTH*SCALING_FACTOR, HEIGHT*SCALING_FACTOR))
        self.screen = pygame.Surface((WIDTH, HEIGHT))

        # _____ Importation des textures _____
        icon = pygame.image.load('./assets/textures/icon.png').convert_alpha()
        
        self.font_6 = pygame.font.Font("./assets/fonts/space_invaders.ttf", 6)
        self.font_8 = pygame.font.Font("./assets/fonts/space_invaders.ttf", 8)
        self.font_14 = pygame.font.Font("./assets/fonts/space_invaders.ttf", 16)

        self.logo = pygame.image.load('./assets/textures/title.png').convert_alpha()
        self.logo = pygame.transform.scale(self.logo,(193,83))
        
        self.life_icon = pygame.image.load('./assets/textures/player.png').convert_alpha()

        # _____ Esthétique fenêtre _____
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Space Invaders v0.1")

        # _____ Variables in-game _____
        self.in_main_menu = True
        self.enemies = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.running = True
        self.is_init = False
        self.x_group = -1
        
        self.dy = 0.09
        self.vy = 0
        
        self.options = [None, "option.number_of_life", "option.ennemies_speed", "option.unbreakable_shield", "option.retro_mode", "option.music"]
        self.color_opacity = 0

    # _____ Lancement du jeu _____
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
                    
                    elif event.key == pygame.K_ESCAPE:
                        # Touche ESCAPE en jeu
                        if self.menu_id == 1:
                            self.enemies.empty()
                            self.shields.empty()
                            self.enemy_projectile_1 = None
                            self.enemy_projectile_2 = None
                            self.is_init = False
                            self.menu_id = 0
                    
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
                                new_value = self.current_menu_options[self.pointeur_vert][self.pointeur_hori-1]
                                if selected_option == "option.number_of_life":
                                    if new_value != self.config.get("option.number_of_life"):
                                        self.config.put("option.number_of_life", new_value)
                                        self.color_opacity = 255
                                elif selected_option == "option.ennemies_speed":
                                    if new_value != self.config.get("option.ennemies_speed"):
                                        self.config.put("option.ennemies_speed", new_value)
                                        self.color_opacity = 255
                                elif selected_option == "option.unbreakable_shield":
                                    if new_value != self.config.get("option.unbreakable_shield"):
                                        self.config.put("option.unbreakable_shield", new_value)
                                        self.color_opacity = 255
                                elif selected_option == "option.retro_mode":
                                    if new_value != self.config.get("option.retro_mode"):
                                        self.config.put("option.retro_mode", new_value)
                                        self.color_opacity = 255
                                else:
                                    if new_value != self.config.get("option.music"):
                                        self.config.put("option.music", new_value)
                                        self.color_opacity = 255
                        
                        # Touche RETURN pour le menu des credits   
                        elif self.menu_id == 3:
                            if self.pointeur_vert == 0:
                                self.menu_id = 0
                                
            # --- IN-GAME ---
            if self.menu_id == 1:
                # controls
                if self.keys_pressed[pygame.K_LEFT] and self.player.rect.x - 1 > 0:
                    self.player.rect.x -= 1
                if self.keys_pressed[pygame.K_RIGHT] and self.player.rect.x + 1 + self.player.image.get_rect().width < WIDTH:
                    self.player.rect.x += 1
                if self.keys_pressed[pygame.K_SPACE] and self.player_projectile == None :
                    self.player_projectile = Projectile((self.player.rect.x + (0.5*self.player.rect.width)), self.player.rect.y)
            self.draw_on_screen()
                    
        pygame.quit()
        sys.exit()
        
    # _____ Screen Manager _____
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
        
    # _____ Affichage du menu principal _____
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
    
    # _____ Affichage du menu des options _____
    def draw_options(self):
        
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
            
        # SAVED TAUST
        if self.color_opacity > 0:
            self.color_opacity -= 5
        
        self._draw_text("Sauvegarde !", (self.color_opacity, self.color_opacity, self.color_opacity), self.font_8, 7, HEIGHT - 15)

    # _____ Affichage du menu des crédits _____
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
       
    # _____ Initialisation du jeu _____ 
    def game_init(self):
        # Création des entités
            # - Joueur
        self.player = Player(0, 0)
        self.player.move(WIDTH/2-(self.player.image.get_width()/2), 201)
            # - Projectiles
        self.ennemi_projectile=None
        self.player_projectile=None

        self.timer_missile_1 = 0
        self.timer_missile_2 = 0
        self.enemy_projectile_1 = None
        self.enemy_projectile_2 = None
        
        self.shield_size = 1
        self.shields = pygame.sprite.Group()
        self.shield_amount = 4
        self.shield_x_positions = [num * (WIDTH / self.shield_amount-10) for num in range(self.shield_amount)]
        self.create_multiple_shield(*self.shield_x_positions, x_start = 32, y_start = 180)
        
        self.remaining_life = self.config.get("option.number_of_life")
        self.score = 70
        self.hi_score = self.config.get("option.highest_score")
        
        # Couleur vert pour les icones de vies
        if not self.config.get("option.retro_mode"):
            self._replace_color(self.life_icon, GREEN)
        else:
            self._replace_color(self.life_icon, WHITE)

            # - Ennemis
        rang = 0
        for y in range(40, HEIGHT-130, 15):
            for x in range(25, WIDTH-30, 15):
                if rang == 0:
                    self.enemies.add(Meduse(x+1.9, y))
                elif rang <= 2:
                    self.enemies.add(Crabe(x+0.5, y))
                elif rang <= 4:
                    self.enemies.add(Poulpe(x, y))
            rang += 1
    
    # _____ Affichage de l'écran de jeu _____
    def draw_game(self):
        
        if not self.is_init:
            self.game_init()
            self.is_init = True

        # Affichage du texte
        self._draw_text("SCORE<1>                HI-SCORE<2>", WHITE, self.font_8, None, 10, True)
        self._draw_text(f"{self.score:04d}", WHITE, self.font_8, 45, 21)
        self._draw_text(f"{self.hi_score:04d}", WHITE, self.font_8, WIDTH-83, 21)
        self._draw_text("CREDIT 00", WHITE, self.font_8, WIDTH-68, HEIGHT-20)
        self._draw_text(f"{self.remaining_life}", WHITE, self.font_8, 20, HEIGHT-20)
        pygame.draw.line(self.screen, WHITE if self.config.get("option.retro_mode") else GREEN, (0,HEIGHT-30), (WIDTH, HEIGHT-30))
        
        # Affichage du nombre de vie.s restant.s
        for x in range(30, 30+self.remaining_life*17, 17):
            self.screen.blit(self.life_icon, (x, HEIGHT-20))
        
        # Affichage des entitées
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        self.player.update()
        
        # Affichage des groupes
        self.shields.draw(self.screen)     
        self.enemies.draw(self.screen)

        for enemy in self.enemies:
            #self.screen.blit(enemy.image, (enemy.rect.x,enemy.rect.y))
            enemy.update()
            
            if self.player_projectile != None:
                if pygame.sprite.collide_rect(self.player_projectile, enemy):
                    self.player_projectile = None
                    self.enemies.remove(enemy)
            
        # Tirs Ennemis
        if len(self.enemies) != 0:
            if self.timer_missile_1 >= 130:
                self.timer_missile_1 = 0
                self.random_enemy = random.choice(self.enemies.sprites())
                self.enemy_projectile_1 = Projectile((self.random_enemy.rect.x + (0.5*self.random_enemy.rect.width)) ,self.random_enemy.rect.y)

            if self.timer_missile_2 >= 155:
                self.timer_missile_2 = 0
                self.random_enemy = random.choice(self.enemies.sprites())
                self.enemy_projectile_2 = Projectile((self.random_enemy.rect.x + (0.5*self.random_enemy.rect.width)) ,self.random_enemy.rect.y)

            self.timer_missile_1 += 1
            self.timer_missile_2 += 1

        # Détection collision missiles ennemis
        if self.enemy_projectile_1 != None:
                if pygame.sprite.collide_rect(self.enemy_projectile_1, self.player):
                    self.enemy_projectile_1 = None
                    print("Joueur touché")
                    self.player.death()
        
        if self.enemy_projectile_2 != None:
                if pygame.sprite.collide_rect(self.enemy_projectile_2, self.player):
                    self.enemy_projectile_2 = None
                    print("Joueur touché")
                    self.player.death()
        
        for shield in self.shields:
            if self.enemy_projectile_1 != None:
                if pygame.sprite.collide_rect(self.enemy_projectile_1, shield):
                    if not self.config.get("option.unbreakable_shield"):
                        self.destroy_shield(self.enemy_projectile_1)
                    self.enemy_projectile_1 = None
            if self.enemy_projectile_2 != None:
                if pygame.sprite.collide_rect(self.enemy_projectile_2, shield):
                    if not self.config.get("option.unbreakable_shield"):
                        self.destroy_shield(self.enemy_projectile_2)
                    self.enemy_projectile_2 = None

        # Affichage des projectiles
        # - Missile Joueur
        if self.player_projectile != None and self.player_projectile.rect.y > 0:
            self.screen.blit(self.player_projectile.image , (self.player_projectile.rect.x , self.player_projectile.rect.y ))
        else:
            self.player_projectile = None
        
        # - Missile Ennemi n°1
        if self.enemy_projectile_1 != None and self.enemy_projectile_1.rect.y < HEIGHT:
            self.screen.blit(self.enemy_projectile_1.image , (self.enemy_projectile_1.rect.x , self.enemy_projectile_1.rect.y ))
        else: 
            self.enemy_projectile_1 = None

        # - Missile Ennemi n°2
        if self.enemy_projectile_2 != None and self.enemy_projectile_2.rect.y < HEIGHT:
            self.screen.blit(self.enemy_projectile_2.image , (self.enemy_projectile_2.rect.x , self.enemy_projectile_2.rect.y ))
        else: 
            self.enemy_projectile_2 = None
                
        # enemies moving
        """
        for enemy in self.enemies:

            if enemy.rect.x == 0: # Si collision gauche
                self.x_group = 1
            
            if (enemy.rect.x + enemy.rect.width) == WIDTH: # Si collision droite
                self.x_group = -1

            enemy.rect.x += self.x_group
        """
            
        # Déplacement des Projectiles
        if self.player_projectile != None:
            self.player_projectile.update_player()
            
        if self.enemy_projectile_1 != None:
            self.enemy_projectile_1.update_enemy()

        if self.enemy_projectile_2 != None:
            self.enemy_projectile_2.update_enemy()

        
    def create_shield(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(get_shield_shape()):
            for col_index,col in enumerate(row):
                if col == '*':
                    x = x_start + col_index * self.shield_size + offset_x
                    y = y_start + row_index * self.shield_size
                    shield = Shield(self.shield_size, x, y, WHITE if self.config.get("option.retro_mode") else GREEN)
                    self.shields.add(shield)
                    
    def create_multiple_shield(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_shield(x_start, y_start, offset_x)
        
    def destroy_shield(self, projectile):
        shield_hit_list_random = pygame.sprite.spritecollide(projectile, self.shields, False, pygame.sprite.collide_rect_ratio(3))
        shield_hit_list_random_center = pygame.sprite.spritecollide(projectile, self.shields, False, pygame.sprite.collide_rect_ratio(2))
        
        for shield in shield_hit_list_random:
                pourcentage = random.randint(0,6)
                if pourcentage == 4:
                    shield.kill()
        for shield in shield_hit_list_random_center:
                pourcentage = random.randint(1, 2)
                if pourcentage == 1:
                    shield.kill()
                    
    def _replace_color(self, surface: pygame.Surface, color):
        w, h = surface.get_size()
        r, g, b = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(r, g, b, a))
        
    def _draw_text(self, text, color, font, x, y, align_center=False):
        tmp_font = font.render(text, 0.2, color)
        if align_center:
            self.screen.blit(tmp_font, ((WIDTH - tmp_font.get_width())/2, y))
        else:
            self.screen.blit(tmp_font, (x,y))

if __name__ == "__main__":
    app = App()
    app.run()

