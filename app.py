import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import random
import pygame

import utils
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

MUSIC_LINK = "assets/sounds/music2.wav"
HIT_SOUND_LINK = "assets/sounds/hitHurt.wav"
EXPLOSION_SOUND_LINK = "assets/sounds/explosion.wav"
LASER_SOUND_LINK = "assets/sounds/laserShoot.wav"

MUSIC_VOLUME = 0.08
HIT_VOLUME = 0.4
EXPLOSION_VOLUME = 0.2
LASER_VOLUME = 0.3

MOTHERSHIP_SHOW = 600

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
        self.logo = pygame.transform.scale(self.logo, (193,83))
        
        self.life_icon = pygame.image.load('./assets/textures/player.png').convert_alpha()

        # _____ Importation musique & SFX _____
        pygame.mixer.init()

        self.music = pygame.mixer.music.load(MUSIC_LINK)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        self.music_enable = self.config.get("option.music")

        self.hit_sound = pygame.mixer.Sound(HIT_SOUND_LINK)
        self.explosion_sound = pygame.mixer.Sound(EXPLOSION_SOUND_LINK)
        self.laser_sound = pygame.mixer.Sound(LASER_SOUND_LINK)

        self.hit_sound.set_volume(HIT_VOLUME)
        self.explosion_sound.set_volume(EXPLOSION_VOLUME)
        self.laser_sound.set_volume(LASER_VOLUME)

        # _____ Esthétique fenêtre _____
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Space Invaders v0.1")
        
        # _____ Esthétique des menus ______
        self.star_field_slow = []
        self.star_field_medium = []
        self.star_field_fast = []

        for slow_stars in range(25): #birth those plasma balls, baby
            star_loc_x = random.randrange(0, WIDTH)
            star_loc_y = random.randrange(0, HEIGHT)
            self.star_field_slow.append([star_loc_x, star_loc_y])

        for medium_stars in range(15):
            star_loc_x = random.randrange(0, WIDTH)
            star_loc_y = random.randrange(0, HEIGHT)
            self.star_field_medium.append([star_loc_x, star_loc_y])

        for fast_stars in range(5):
            star_loc_x = random.randrange(0, WIDTH)
            star_loc_y = random.randrange(0, HEIGHT)
            self.star_field_fast.append([star_loc_x, star_loc_y])

        # _____ Variables in-game _____
        self.in_main_menu = True
        self.enemies = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.running = True
        self.is_init = False
        self.playing_game = False 
        self.x_group = -1
        
        self.dy = 0.09
        self.vy = 0
        
        self.options = [
            None,
            "option.number_of_life",
            "option.ennemies_speed",
            "option.unbreakable_shield",
            "option.retro_mode",
            "option.music"
        ]
        

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
        self.pointeur_hori = 0
        
        while self.running:
            self.clock.tick(FPS)
            self.keys_pressed = pygame.key.get_pressed()
            
            if self.menu_id == 0 or self.menu_id == 3:
                self.current_menu_options = [[0],[0],[0]]

            elif self.menu_id == 2:
                self.current_menu_options = [
                    [0],
                    [1,2,3,4],
                    [1,2,3],
                    [True,False],
                    [True,False],
                    [True,False]
                ]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_k:
                        if self.menu_id == 1:
                            self.remaining_life -= 1
                            
                    if event.key == pygame.K_w:
                        if self.menu_id == 1:
                            self.enemies.empty()
                    
                    if event.key == pygame.K_UP:
                        self.pointeur_vert -= 1
                        if self.pointeur_vert < 0:
                            self.pointeur_vert = len(self.current_menu_options)-1
                        if self.menu_id == 2:
                            if self.options[self.pointeur_vert] != None:
                                self.pointeur_hori = self.current_menu_options[self.pointeur_vert].index(self.config.get(self.options[self.pointeur_vert]))

                    elif event.key == pygame.K_DOWN:
                        self.pointeur_vert += 1
                        if self.pointeur_vert > len(self.current_menu_options)-1:
                            self.pointeur_vert = 0
                        if self.menu_id == 2:
                            if self.options[self.pointeur_vert] != None:
                                self.pointeur_hori = self.current_menu_options[self.pointeur_vert].index(self.config.get(self.options[self.pointeur_vert]))
                        
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
                            self.game_reset()
                    
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
                                new_value = self.current_menu_options[self.pointeur_vert][self.pointeur_hori]

                                if new_value != self.config.get(selected_option):
                                    self.config.put(selected_option, new_value)
                                    self.color_opacity = 255

                                    if selected_option == "option.music":
                                        self.music_enable = new_value

                        # Touche RETURN pour le menu des credits   
                        elif self.menu_id == 3:
                            self.menu_id = 0
                                
            # --- IN-GAME ---
            if self.menu_id == 1 and self.playing_game:
                # controls
                if self.keys_pressed[pygame.K_LEFT] and self.player.rect.x - 1 > 0:
                    self.player.rect.x -= 1
                if self.keys_pressed[pygame.K_RIGHT] and self.player.rect.x + 1 + self.player.image.get_rect().width < WIDTH:
                    self.player.rect.x += 1
                if self.keys_pressed[pygame.K_SPACE] and self.player_projectile == None:
                    if self.shoot_cooldown < 0:
                        self.player_projectile = Projectile((self.player.rect.x + (0.5*self.player.rect.width)), self.player.rect.y, False)
                        self.laser_sound.play()
                        self.shoot_cooldown = 30
                # music
                if self.music_enable == True and self.playing_music == False:
                    pygame.mixer.music.play(-1)
                    self.playing_music = True
            if self.menu_id == 1 and not self.playing_game:
                if self.keys_pressed[pygame.K_RETURN]:
                    self.game_reset()
                    self.is_init = False
                    self.draw_game()
            
            if self.menu_id != 1:
                pygame.mixer.music.stop()
                self.playing_music = False

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
        
        self.draw_stars()
        
        # Display Game Icon
        self.screen.blit(self.logo,((WIDTH - self.logo.get_width())/2, 20 + self.vy))
        
        self.vy += self.dy
        if self.vy > 5 or self.vy < -5:
            self.dy *= -1
        
        # Display text
        menu = [["> JOUER <","OPTIONS","CREDITS"],["JOUER","> OPTIONS <","CREDITS"],["JOUER","OPTIONS","> CREDITS <"]]    
        for i in range(3):
            self._draw_text(menu[self.pointeur_vert][i], WHITE, self.font_14, None, 140+(i*30), True)
    
    # _____ Affichage du menu des options _____
    def draw_options(self):
        
        self.draw_stars()
        
        # RETOUR
        self._draw_text("> RETOUR <" if self.pointeur_vert == 0 else "RETOUR", WHITE, self.font_8, None, 60, True)
        
        # NOMBRES DE VIES
        self._draw_text("> NOMBRE DE VIES : <" if self.pointeur_vert == 1 else "NOMBRE DE VIES :", WHITE, self.font_8, None, 80, True)
        if self.pointeur_vert == 1:
            if self.pointeur_hori == 0:
                self._draw_text("[ 1 ] / 2 / 3 / 4", GRAY, self.font_8, None, 90, True)
            elif self.pointeur_hori == 1:
                self._draw_text("1 / [ 2 ] / 3 / 4", GRAY, self.font_8, None, 90, True)
            elif self.pointeur_hori == 2:
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
            if self.pointeur_hori == 0:
                self._draw_text("[ LENT ] / MOYEN / RAPIDE", GRAY, self.font_8, None, 120, True)
            elif self.pointeur_hori == 1:
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
            self._draw_text("[ OUI ] / NON" if self.pointeur_hori == 0 else "OUI / [ NON ]", GRAY, self.font_8, None, 150, True)
        else:
            choice = self.config.get("option.unbreakable_shield")
            self._draw_text("[ OUI ] / NON" if choice else "OUI / [ NON ]", GRAY, self.font_8, None, 150, True)
                
        # MODE RETRO
        self._draw_text("> MODE RETRO : <" if self.pointeur_vert == 4 else "MODE RETRO :", WHITE, self.font_8, None, 170, True)
        if self.pointeur_vert == 4:
            self._draw_text("[ OUI ] / NON" if self.pointeur_hori == 0 else "OUI / [ NON ]", GRAY, self.font_8, None, 180, True)
        else:
            choice = self.config.get("option.retro_mode")
            self._draw_text("[ OUI ] / NON" if choice else "OUI / [ NON ]", GRAY, self.font_8, None, 180, True)
        
        # MUSIQUE
        self._draw_text("> MUSIQUE : <" if self.pointeur_vert == 5 else "MUSIQUE :", WHITE, self.font_8, None, 200, True)
        if self.pointeur_vert == 5:
            self._draw_text("[ OUI ] / NON" if self.pointeur_hori == 0 else "OUI / [ NON ]", GRAY, self.font_8, None, 210, True)
        else:
            choice = self.config.get("option.music")
            self._draw_text("[ OUI ] / NON" if choice else "OUI / [ NON ]", GRAY, self.font_8, None, 210, True)
            
        # SAVED TAUST
        if self.color_opacity > 0:
            self.color_opacity -= 5
        
        self._draw_text("Sauvegarde !", (self.color_opacity, self.color_opacity, self.color_opacity), self.font_8, 7, HEIGHT - 15)

    # _____ Affichage du menu des crédits _____
    def draw_credits(self):
        
        self.draw_stars()
        
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
        for i in range(9):
            self._draw_text(str_credits[i][0], WHITE, str_credits[i][1] , None, str_credits[i][2], True)
       
    # ____ Affichage des étoiles _____
    def draw_stars(self):
        for star in self.star_field_slow:
            star[1] += 0.5
            if star[1] > HEIGHT:
                star[0] = random.randrange(0, WIDTH)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(self.screen, GRAY, star, 1)

        for star in self.star_field_medium:
            star[1] += 1.5
            if star[1] > HEIGHT:
                star[0] = random.randrange(0, WIDTH)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(self.screen, GRAY, star, 1)

        for star in self.star_field_fast:
            star[1] += 2
            if star[1] > HEIGHT:
                star[0] = random.randrange(0, WIDTH)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(self.screen, (255, 255, 0), star, 1)
       
    # _____ Initialisation du jeu _____ 
    def game_init(self):
        
        self.player = Player(0, 0)
        self.player.move(WIDTH/2-(self.player.image.get_width()/2), 201)
        
        self.enemy_direction = 1
        self.player_projectile = None

        self.mothership = None
        self.mothership_timer = MOTHERSHIP_SHOW
        self.mothership_direction = -1

        self.timer_missile_1 = 0
        self.timer_missile_2 = 0
        self.timer_movement = 5
        self.shoot_cooldown = 0
        self.enemy_projectile_1 = None
        self.enemy_projectile_2 = None
        
        self.shield_size = 1
        self.shields = pygame.sprite.Group()
        self.shield_amount = 4
        self.shield_x_positions = [num * (WIDTH / self.shield_amount-10) for num in range(self.shield_amount)]
        self.create_multiple_shield(*self.shield_x_positions, x_start = 32, y_start = 180)
        
        self.remaining_life = self.config.get("option.number_of_life")
        self.hi_score = self.config.get("option.highest_score")
        self.music_enable = self.config.get("option.music")
        self.playing_music = False
        self.score = 0
        self.playing_game = True
        self.mothership_killed = 0
        
        # Couleur vert pour les icones de vies
        if not self.config.get("option.retro_mode"):
            utils.replace_color(self.life_icon, GREEN)
        else:
            utils.replace_color(self.life_icon, WHITE)

        # Ennemis
        rang = 0
        for y in range(40, HEIGHT-130, 15):
            for x in range(25, WIDTH-30, 15):
                if rang == 0:
                    self.enemies.add(Meduse(x, y, self.config.get("option.retro_mode")))
                elif rang <= 2:
                    self.enemies.add(Crabe(x, y, self.config.get("option.retro_mode")))
                elif rang <= 4:
                    self.enemies.add(Poulpe(x, y, self.config.get("option.retro_mode")))
            rang += 1
    
    # _____ Réitinialisation du jeu _____
    def game_reset(self):
        self.enemies.empty()
        self.shields.empty()
        self.enemy_projectile_1 = None
        self.enemy_projectile_2 = None
        self.is_init = False
        self.menu_id = 0
    
    # _____ Affichage de l'écran de jeu _____
    def draw_game(self):
        
        if not self.is_init:
            self.game_init()
            self.is_init = True
        

        # Displaying text & decorations
        self._draw_text("SCORE<1>                HI-SCORE<2>", WHITE, self.font_8, None, 10, True)
        self._draw_text(f"{self.score:04d}", WHITE, self.font_8, 45, 21)
        self._draw_text(f"{self.hi_score:04d}", WHITE, self.font_8, WIDTH-83, 21)
        self._draw_text("CREDIT 00", WHITE, self.font_8, WIDTH-68, HEIGHT-20)
        self._draw_text(f"{self.remaining_life}", WHITE, self.font_8, 20, HEIGHT-20)
        pygame.draw.line(self.screen, WHITE if self.config.get("option.retro_mode") else GREEN, (0,HEIGHT-30), (WIDTH, HEIGHT-30))
            
        # Displaying the remaining life
        for x in range(30, 30+self.remaining_life*17, 17):
            self.screen.blit(self.life_icon, (x, HEIGHT-20))
             
        # Displaying elements on the screen
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        if self.mothership != None:
            self.screen.blit(self.mothership.image, (self.mothership.rect.x, self.mothership.rect.y))
        self.shields.draw(self.screen)
        self.enemies.draw(self.screen)

        if self.playing_game:
            
            # Displaying the mothership
            if self.mothership_timer <= 0:
                if self.mothership == None:
                    self.mothership_direction *= -1 #1 if self.mothership_direction == -1 else -1
                    self.mothership = VaisseauMere(WIDTH if self.mothership_direction == -1 else -5, 33, self.config.get("option.retro_mode"))

                if self.mothership.rect.x < WIDTH and self.mothership_direction == 1:
                    self.mothership.move(self.mothership_direction)
                elif self.mothership.rect.right > 0 and self.mothership_direction == -1:
                    self.mothership.move(self.mothership_direction)

                else:
                    self.mothership = None
                    self.mothership_timer = MOTHERSHIP_SHOW
            else:
                self.mothership_timer -= 1
        
            self.player.update()
                
            has_to_move = False
            all_enemies = self.enemies.sprites()
            for enemy in all_enemies:
                
                # Enemies movement
                if enemy.rect.right >= WIDTH:
                    self.enemy_direction = -1
                    has_to_move = True

                elif enemy.rect.left < 2:
                    self.enemy_direction = 1
                    has_to_move = True

            if has_to_move:
                for enemy in all_enemies:
                    enemy.move_down(self.enemy_direction)
                has_to_move = False

            self.enemies.update(self.enemy_direction, len(all_enemies), self.config.get("option.ennemies_speed"))
            self.draw_projectile()
            self.check_projectile_collisions()
            self.check_shield_destruction()
            self.shoot_cooldown -= 1
            
            if self.mothership != None :
                self.mothership.update()

            
            if not self.enemies and self.remaining_life > 0 :
                self.playing_game = False
                if self.config.get("option.highest_score") < self.score:
                    self.config.put("option.highest_score", self.score)
                self.draw_victory()
            if self.remaining_life <= 0 or self.check_enemy_collision_shield():
                self.playing_game = False
                self.draw_defeat()
        else: 
            if not self.enemies and self.remaining_life > 0 :
                self.draw_victory()
            elif self.remaining_life <= 0 or self.check_enemy_collision_shield():
                self.draw_defeat()
                
    # _____ Affichage des projectiles _____     
    def draw_projectile(self):
        
        # Enemies' projectile
        if len(self.enemies) != 0:
            if self.timer_missile_1 >= 130:
                self.timer_missile_1 = 0
                self.random_enemy = random.choice(self.enemies.sprites())
                self.enemy_projectile_1 = Projectile((self.random_enemy.rect.x + (0.5*self.random_enemy.rect.width)) ,self.random_enemy.rect.y, True)

            if self.timer_missile_2 >= 155:
                self.timer_missile_2 = 0
                self.random_enemy = random.choice(self.enemies.sprites())
                self.enemy_projectile_2 = Projectile((self.random_enemy.rect.x + (0.5*self.random_enemy.rect.width)) ,self.random_enemy.rect.y, True)

            self.timer_missile_1 += 1
            self.timer_missile_2 += 1
        
        # Player's projectile
        if self.player_projectile != None:
            if self.player_projectile.rect.y > 0:
                self.screen.blit(self.player_projectile.image , (self.player_projectile.rect.x , self.player_projectile.rect.y ))
                self.player_projectile.update_player()
            else:
                self.player_projectile = None
        
        # First enemy's projectile
        if self.enemy_projectile_1 != None:
            if self.enemy_projectile_1.rect.y < HEIGHT:
                self.screen.blit(self.enemy_projectile_1.image , (self.enemy_projectile_1.rect.x , self.enemy_projectile_1.rect.y ))
                self.enemy_projectile_1.update_enemy()
            else: 
                self.enemy_projectile_1 = None

        # Second enemy's projectile
        if self.enemy_projectile_2 != None:
            if self.enemy_projectile_2.rect.y < HEIGHT:
                self.screen.blit(self.enemy_projectile_2.image , (self.enemy_projectile_2.rect.x , self.enemy_projectile_2.rect.y ))
                self.enemy_projectile_2.update_enemy()
            else: 
                self.enemy_projectile_2 = None
    
    # _____ Collision entre projectiles et ennemis _____ 
    def check_projectile_collisions(self):        
        
        for enemy in self.enemies:
            if self.player_projectile != None:
                if pygame.sprite.collide_rect(self.player_projectile, enemy):
                    self.calcul_score(type(enemy).__name__)
                    self.player_projectile = None
                    self.enemies.remove(enemy)
                    self.explosion_sound.play()
            
        if self.mothership != None and self.player_projectile != None:
            if pygame.sprite.collide_rect(self.player_projectile, self.mothership):
                self.calcul_score(type(self.mothership).__name__)
                self.player_projectile = None
                self.mothership = None
                self.explosion_sound.play()
                self.mothership_timer = MOTHERSHIP_SHOW
                self.mothership_killed += 1

        if self.enemy_projectile_1 != None:
                if pygame.sprite.collide_rect(self.enemy_projectile_1, self.player):
                    self.enemy_projectile_1 = None
                    self.remaining_life = self.remaining_life - 1
                    self.hit_sound.play()
        
        if self.enemy_projectile_2 != None:
                if pygame.sprite.collide_rect(self.enemy_projectile_2, self.player):
                    self.enemy_projectile_2 = None
                    self.remaining_life = self.remaining_life - 1
                    self.hit_sound.play()
    
    # _____ Calcul du score _____                       
    def calcul_score(self,enemy_type):
        if enemy_type == 'Poulpe':
            self.score += 10
        elif enemy_type == 'Crabe':
            self.score += 20
        elif enemy_type == 'Meduse':
            self.score += 30
        elif enemy_type == 'VaisseauMere':
            self.score += 100
    
    # _____ Destruction des boucliers _____         
    def check_shield_destruction(self):
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
                    
            if self.player_projectile != None:
                if pygame.sprite.collide_rect(self.player_projectile, shield):
                    if not self.config.get("option.unbreakable_shield"):
                        self.destroy_shield(self.player_projectile)
                    self.player_projectile = None
    
    # _____ Collision entre boucliers et ennemis _____
    def check_enemy_collision_shield(self):
        for enemy in self.enemies:
            if enemy.rect.bottom >= 180:
                return True
        return False
    
    # _____ Création des boucliers _____
    def create_shield(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(get_shield_shape()):
            for col_index,col in enumerate(row):
                if col == '*':
                    x = x_start + col_index * self.shield_size + offset_x
                    y = y_start + row_index * self.shield_size
                    shield = Shield(self.shield_size, x, y, WHITE if self.config.get("option.retro_mode") else GREEN)
                    self.shields.add(shield)
    
    # _____ Création de plusieurs boucliers _____     
    def create_multiple_shield(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_shield(x_start, y_start, offset_x)
    
    # _____ Explosion sur les boucliers _____ 
    def destroy_shield(self, projectile):
        shield_hit_list_random = pygame.sprite.spritecollide(projectile, self.shields, False, pygame.sprite.collide_rect_ratio(3))
        shield_hit_list_random_center = pygame.sprite.spritecollide(projectile, self.shields, False, pygame.sprite.collide_rect_ratio(2))
        
        for shield in shield_hit_list_random:
                pourcentage = random.randint(0,4)
                if pourcentage == 4:
                    shield.kill()
        for shield in shield_hit_list_random_center:
                pourcentage = random.randint(1, 2)
                if pourcentage == 1:
                    shield.kill()
    
    # _____ Affichage de l'écran du Game Over _____
    def draw_defeat(self):
        game_over_screen_fade = pygame.Surface((WIDTH, HEIGHT))
        game_over_screen_fade.fill((0, 0, 0))
        game_over_screen_fade.set_alpha(160)
        self.screen.blit(game_over_screen_fade, (0, 0))
        
        self._draw_text("GAME OVER", RED, self.font_14, None, HEIGHT/2-60, True)
        self._draw_text(f"SCORE : {self.score}", WHITE, self.font_8, None, HEIGHT/2-20, True)
        self._draw_text(f"VAISSEAU MERE DETRUIT : {self.mothership_killed}" if self.mothership_killed < 1 else f"VAISSEAUX MERE DETRUITS : {self.mothership_killed}", WHITE, self.font_8, None, HEIGHT/2-10, True)
        self._draw_text("> RETOUR <", WHITE, self.font_8, None, HEIGHT/2+20, True)
        
    # _____ Affichage de l'écran de victoire _____
    def draw_victory(self):
        game_over_screen_fade = pygame.Surface((WIDTH, HEIGHT))
        game_over_screen_fade.fill((0, 0, 0))
        game_over_screen_fade.set_alpha(160)
        self.screen.blit(game_over_screen_fade, (0, 0))
        
        hi_score = self.config.get("option.highest_score")
        self._draw_text("VICTOIRE", GREEN, self.font_14, None, HEIGHT/2-60, True)
        self._draw_text(f"SCORE : {self.score}", WHITE, self.font_8, None, HEIGHT/2-20, True)
        self._draw_text(f"HI-SCORE : {hi_score}", WHITE, self.font_8, None, HEIGHT/2-10, True)
        self._draw_text(f"VAISSEAU MERE DETRUIT : {self.mothership_killed}" if self.mothership_killed < 1 else f"VAISSEAUX MERE DETRUITS : {self.mothership_killed}", WHITE, self.font_8, None, HEIGHT/2, True)
        self._draw_text("> RETOUR <", WHITE, self.font_8, None, HEIGHT/2+30, True)
    
    # _____ Fonction utilitaire pour afficher du texte _____  
    def _draw_text(self, text, color, font, x, y, align_center=False):
        tmp_font = font.render(text, 0.2, color)
        if align_center:
            self.screen.blit(tmp_font, ((WIDTH - tmp_font.get_width())/2, y))
        else:
            self.screen.blit(tmp_font, (x,y))

# _____ Fonction principale _____
if __name__ == "__main__":
    app = App()
    app.run()

