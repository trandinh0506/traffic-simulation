import pygame
from random import randint
from way import Way

class Map:
    def __init__(self):
        self.ways: list[Way] = []
        
        w = Way([20, 20], [1500, 150], 3, "up")
        self.ways.append(w)
        self.ways.append(Way([170, 100], [1500, 200], 3, "right"))
    def render(self, display: pygame.Surface, offset: tuple[int, int]) -> None:
        for w in self.ways:
            w.render(display, offset)
    