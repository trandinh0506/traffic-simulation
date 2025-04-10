import pygame
from constant import *
def drawDashedLine(surface: pygame.Surface,
                     color: tuple[int, int, int],
                     start_pos: tuple[int, int],
                     end_pos: tuple[int, int],
                     width=2, dash_length=24, space_length=18):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length + space_length

    # Tính độ dài của đoạn line
    length = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
    # Vector đơn vị hướng từ start -> end
    dx = (x2 - x1) / length
    dy = (y2 - y1) / length

    # Vẽ các đoạn đứt
    dist = 0
    while dist < length:
        start_x = x1 + dx * dist
        start_y = y1 + dy * dist
        end_x   = x1 + dx * min(dist + dash_length, length)
        end_y   = y1 + dy * min(dist + dash_length, length)

        pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), width)
        dist += dl

def reverseDirection(direction: str) -> str:
    mapping = {LEFT: RIGHT, RIGHT: LEFT, UP: DOWN, DOWN: UP}
    return mapping.get(direction, direction)