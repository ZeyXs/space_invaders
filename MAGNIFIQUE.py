import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 768, 672
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

FPS = 60
BULLET_VEL = 7

HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

ENEMY_HIT = pygame.USEREVENT + 1


PLAYER_SHIP_IMAGE = pygame.image.load(os.path.join('assets', 'player_ship.png'))
PLAYER_SHIP = pygame.transform.scale(PLAYER_SHIP_IMAGE, (55,40))

ENEMY_SHIP_IMAGE = pygame.image.load(os.path.join('assets', 'enemy_ship.png'))
ENEMY_SHIP = pygame.transform.scale(ENEMY_SHIP_IMAGE, (55,40))

def draw_window(rect_a,rect_b,player_bullets,enemy_health):
    WIN.fill(BLACK)

    enemy_health_text = HEALTH_FONT.render("Health: " + str(enemy_health),1,WHITE)
    WIN.blit(enemy_health_text, (WIDTH - enemy_health_text.get_width() - 10, 10))


    WIN.blit(PLAYER_SHIP, (rect_a.x,rect_a.y))
    WIN.blit(ENEMY_SHIP, (rect_b.x,rect_b.y))

    for bullet in player_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    pygame.display.update()

def player_handle_movement(keys_pressed, rect_p_ship):
    if keys_pressed[pygame.K_q] and rect_p_ship.x - 1 > 0: #LEFT
        rect_p_ship.x -= 1
    if keys_pressed[pygame.K_d] and rect_p_ship.x + 1 + rect_p_ship.width < WIDTH: #RIGHT
        rect_p_ship.x += 1

def handle_bullets(player_bullets, rect_e_ship):
    for bullet in player_bullets:
        bullet.y -= BULLET_VEL
        if rect_e_ship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ENEMY_HIT))
            player_bullets.remove(bullet)
        elif bullet.y < 0:
            player_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    rect_p_ship = pygame.Rect(100,300,55,40)
    rect_e_ship = pygame.Rect(400,140,55,40)

    player_bullets = []
    enemy_health = 1

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(player_bullets) < 1:
                    bullet = pygame.Rect(rect_p_ship.x + rect_p_ship.width//2 - 2, rect_p_ship.y + rect_p_ship.height,10,5)
                    player_bullets.append(bullet)

            if event.type == ENEMY_HIT:
                enemy_health -= 1

        winner_text = ""
        if enemy_health <= 0:
            winner_text = "You WON!"

        if winner_text != "":
            draw_winner(winner_text)
            break


        keys_pressed = pygame.key.get_pressed()
        player_handle_movement(keys_pressed, rect_p_ship)
        
        handle_bullets(player_bullets, rect_e_ship)

        draw_window(rect_p_ship,rect_e_ship,player_bullets,enemy_health)


    main()

if __name__ == "__main__":
    main()