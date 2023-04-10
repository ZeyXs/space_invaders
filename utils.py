import pygame

def gen_rect(x, y, texture):
        img_height = texture.get_height()
        img_width = texture.get_width()
        return pygame.Rect(x, y, img_height, img_width)

def replace_color(surface: pygame.Surface, color):
        w, h = surface.get_size()
        r, g, b = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(r, g, b, a))