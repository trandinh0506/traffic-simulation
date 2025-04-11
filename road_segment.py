from __future__ import annotations
import pygame
from typing import Optional, TYPE_CHECKING

from way import Way
from constant import UP, DOWN, LEFT, RIGHT
from utils import *

if TYPE_CHECKING:
    from intersection import Intersection

class RoadSegment:
    def __init__(
        self,
        start_intersection: Optional["Intersection"],
        end_intersection: Optional["Intersection"],
        direction: str,
        road_length: int,
        half_lane_total: int,
        lane_widths_dir1: list[int],
        lane_widths_dir2: list[int]
    ) -> None:
        self.start = start_intersection
        self.end = end_intersection
        self.direction = direction
        self.road_length = road_length
        self.half_lane_total = half_lane_total
        self.lane_widths_dir1 = lane_widths_dir1
        self.lane_widths_dir2 = lane_widths_dir2

        gap = self.start.size if self.start else 0  # Dùng 'size' thay vì 'gap'

        # Tính toạ độ đoạn đường dựa vào hướng
        if direction in (RIGHT, LEFT):
            pos_x = (self.start.x + gap // 2) if self.start and direction == RIGHT else \
                    (self.start.x - gap // 2 - road_length if self.start else 0)
            pos_y = self.start.y - half_lane_total if self.start else 0
            self.pos = [pos_x, pos_y]
            self.size = [road_length, half_lane_total]
        elif direction in (DOWN, UP):
            pos_y = (self.start.y + gap // 2) if self.start and direction == DOWN else \
                    (self.start.y - gap // 2 - road_length if self.start else 0)
            pos_x = self.start.x - half_lane_total if self.start else 0
            self.pos = [pos_x, pos_y]
            self.size = [half_lane_total, road_length]
        else:
            raise ValueError(f"Invalid direction: {direction}")

        self.way = Way(self.pos, self.size, direction, lane_widths_dir1, lane_widths_dir2)

        if self.start:
            self.start.add_road(self)
        if self.end:
            self.end.add_road(self)

    def render(self, display: pygame.Surface, offset: tuple[int, int]) -> None:
        self.way.render(display, offset)
