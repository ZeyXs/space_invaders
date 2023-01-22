import pygame

def gen_rect(x, y, texture):
        img_height = texture.get_height()
        img_width = texture.get_width()
        return pygame.Rect(x, y, img_height, img_width)