from __future__ import annotations
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


def is_turn_direction_valid(current_dir: str, current_pos: tuple[float, float],
                            target_pos: tuple[float, float],
                            target_dir: str, target_lane_number: int) -> bool:
    """
    Kiểm tra xem với hướng hiện tại của xe (current_dir) và điểm hiện tại (current_pos)
    thì liệu việc chuyển sang lane có hướng target_dir với số thứ tự target_lane_number
    có hợp lệ hay không.

    Điều kiện gồm 2 phần:
      1. Positional check (logic cũ):
         - Nếu current_dir là UP: thì nếu target_dir là LEFT thì dx < 0, nếu RIGHT thì dx > 0.
         - Nếu current_dir là DOWN: thì nếu target_dir là LEFT thì dx > 0, nếu RIGHT thì dx < 0.
         - Nếu current_dir là LEFT: thì nếu target_dir là UP thì dy < 0, nếu DOWN thì dy > 0.
         - Nếu current_dir là RIGHT: thì nếu target_dir là UP thì dy > 0, nếu DOWN thì dy < 0.
         (Lưu ý: các điều kiện này có thể cần điều chỉnh tùy vào cách bạn định nghĩa vị trí tương đối.)
      2. Lane number check (logic mới):
         - Nếu đi thẳng (target_dir == current_dir): luôn hợp lệ.
         - Nếu quay đầu (target_dir == reverseDirection(current_dir)): hợp lệ nếu lane_number của lane đó thỏa mãn quy tắc (ví dụ: chỉ cho phép từ lane số 1).
         - Nếu rẽ trái/phải: áp dụng các quy tắc:
            * Nếu current_dir == UP:
                - Rẽ trái chỉ hợp lệ nếu target_lane_number == 1.
                - Rẽ phải chỉ hợp lệ nếu target_lane_number == 2.
            * Nếu current_dir == DOWN:
                - Rẽ trái chỉ hợp lệ nếu target_lane_number == 2.
                - Rẽ phải chỉ hợp lệ nếu target_lane_number == 1.
            * Nếu current_dir == LEFT:
                - Rẽ lên chỉ hợp lệ nếu target_lane_number == 1.
                - Rẽ xuống chỉ hợp lệ nếu target_lane_number == 2.
            * Nếu current_dir == RIGHT:
                - Rẽ lên chỉ hợp lệ nếu target_lane_number == 2.
                - Rẽ xuống chỉ hợp lệ nếu target_lane_number == 1.
    """
    cx, cy = current_pos
    tx, ty = target_pos
    dx = tx - cx
    dy = ty - cy

    # --- Positional check ---
    pos_valid = False
    if current_dir == UP:
        if target_dir == LEFT:
            pos_valid = dx < 0
        elif target_dir == RIGHT:
            pos_valid = dx > 0
        else:  # target_dir == UP
            pos_valid = True
    elif current_dir == DOWN:
        if target_dir == LEFT:
            pos_valid = dx > 0
        elif target_dir == RIGHT:
            pos_valid = dx < 0
        else:  # target_dir == DOWN
            pos_valid = True
    elif current_dir == LEFT:
        if target_dir == UP:
            pos_valid = dy < 0
        elif target_dir == DOWN:
            pos_valid = dy > 0
        else:  # target_dir == LEFT
            pos_valid = True
    elif current_dir == RIGHT:
        if target_dir == UP:
            pos_valid = dy > 0
        elif target_dir == DOWN:
            pos_valid = dy < 0
        else:  # target_dir == RIGHT
            pos_valid = True
    else:
        pos_valid = False

    # --- Lane number check ---
    lane_valid = False
    # Hợp lệ nếu đi thẳng luôn (vẫn có thể kiểm tra khác way nếu cần)
    if target_dir == current_dir:
        lane_valid = True
    # Quay đầu: chỉ cho phép từ lane số 1 (có thể điều chỉnh lại nếu cần)
    elif target_dir == reverseDirection(current_dir):
        lane_valid = (target_lane_number == 1)
    # Rẽ trái/phải: áp dụng quy tắc như đã mô tả
    else:
        if current_dir == UP:
            if target_dir == LEFT and target_lane_number == 1:
                lane_valid = True
            elif target_dir == RIGHT and target_lane_number == 2:
                lane_valid = True
        elif current_dir == DOWN:
            if target_dir == LEFT and target_lane_number == 2:
                lane_valid = True
            elif target_dir == RIGHT and target_lane_number == 1:
                lane_valid = True
        elif current_dir == LEFT:
            if target_dir == UP and target_lane_number == 1:
                lane_valid = True
            elif target_dir == DOWN and target_lane_number == 2:
                lane_valid = True
        elif current_dir == RIGHT:
            if target_dir == UP and target_lane_number == 2:
                lane_valid = True
            elif target_dir == DOWN and target_lane_number == 1:
                lane_valid = True

    return pos_valid and lane_valid

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
    
    raise Exception(f"Invalid direction `from: {fr}`, `to: {to}`, relative angle diff ${relativeAngleDiff}")


def normalizeAngle(angle: float) -> float:
    angle = angle % (2 * math.pi)
    print(angle)
    if angle < 0:
        angle += 2 * math.pi
    if abs(angle - 2 * math.pi) < EPSILON:
        angle = 0.0
    return angle