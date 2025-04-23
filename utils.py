from __future__ import annotations
import random
import pygame
from constant import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from intersection import Intersection

def drawDashedLine(surface: pygame.Surface,
                     color: tuple[int, int, int],
                     start_pos: tuple[int, int],
                     end_pos: tuple[int, int],
                     width=2, dash_length=24, space_length=36):
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


def compute_road_start_pos(center: tuple[int, int], direction: str, length: int) -> tuple[int, int]:
    cx, cy = center
    if direction == RIGHT:
        return cx, cy - 120  # dịch ra theo trục X
    elif direction == LEFT:
        return cx - length, cy - 120
    elif direction == DOWN:
        return cx - 120, cy
    elif direction == UP:
        return cx - 120, cy - length
    return cx, cy


def get_edge_pos(intersection: Intersection, direction: str, offset: int = 0) -> tuple[int, int]:
    half_size = intersection.size // 2
    if direction == RIGHT:
        return (intersection.x + half_size + offset, intersection.y)
    if direction == LEFT:
        return (intersection.x - half_size - offset, intersection.y)
    if direction == DOWN:
        return (intersection.x, intersection.y + half_size + offset)
    if direction == UP:
        return (intersection.x, intersection.y - half_size - offset)
    
def getRelativeTurnningDirection(fr: str, to: str) -> str:
    relativeAngleDiff = DIRECTION2ANGLE[to] - DIRECTION2ANGLE[fr]
    if relativeAngleDiff == math.pi/2 or relativeAngleDiff == - 3 * math.pi/2:
        return LEFT
    if relativeAngleDiff == -math.pi/2 or relativeAngleDiff == 3 * math.pi/2:
        return RIGHT
    if abs(relativeAngleDiff) == math.pi:
        return TURN_AROUND
    
    return GO_STRAIGHT


def normalizeAngle(angle: float) -> float:
    angle = angle % (2 * math.pi)
    if angle < 0:
        angle += 2 * math.pi
    if abs(angle - 2 * math.pi) < EPSILON:
        angle = 0.0
    return angle

def parse_param_string(param_str: str):
    param_dict = {}
    for item in param_str.split(','):
        key, value = item.split('=')
        param_dict[key.strip()] = int(value.strip()) if value.strip().isdigit() else value.strip()
    return param_dict

def get_available_spawn_point():
    random.shuffle(SPWAN_POINTS)
    for point in SPWAN_POINTS:
        if point["cooldown"] <= 0:
            point["cooldown"] = SPAWN_COOLDOWN_TIME
            return point
    return None 