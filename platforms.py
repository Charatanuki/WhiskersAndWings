import pygame

BLACK = (0, 0, 0)

class Platform:
    def __init__(self, c, d, width, height):
        self.c = c
        self.d = d
        self.width = width
        self.height = height

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, (self.c, self.d, self.width, self.height))
