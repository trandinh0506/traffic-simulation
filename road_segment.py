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
        lane_widths_dir2: list[int],
    ) -> None:
        self.start = start_intersection
        self.end = end_intersection
        self.direction = direction
        self.half_lane_total = half_lane_total
        self.lane_widths_dir1 = lane_widths_dir1
        self.lane_widths_dir2 = lane_widths_dir2

        # Tọa độ tâm các intersection
        start_center = get_edge_pos(self.start, direction) if self.start else (0, 0)
        end_center = get_edge_pos(self.end, reverseDirection(direction)) if self.end else None
        half_size = self.half_lane_total

        if direction == RIGHT:
            pos_x = start_center[0]
            end_x = end_center[0] if end_center else pos_x + road_length
            self.road_length = end_x - pos_x
            pos_y = start_center[1] - half_size
            self.pos = [pos_x, pos_y]
            self.size = [self.road_length, 2 * half_size]

        elif direction == LEFT:
            end_x = end_center[0] if end_center else start_center[0] - road_length
            pos_x = end_x
            self.road_length = start_center[0] - end_x
            pos_y = start_center[1] - half_size
            self.pos = [pos_x, pos_y]
            self.size = [self.road_length, 2 * half_size]

        elif direction == DOWN:
            pos_y = start_center[1]
            end_y = end_center[1] if end_center else pos_y + road_length
            self.road_length = end_y - pos_y
            pos_x = start_center[0] - half_size
            self.pos = [pos_x, pos_y]
            self.size = [2 * half_size, self.road_length]

        elif direction == UP:
            end_y = end_center[1] if end_center else start_center[1] - road_length
            pos_y = end_y
            self.road_length = start_center[1] - end_y
            pos_x = start_center[0] - half_size
            self.pos = [pos_x, pos_y]
            self.size = [2 * half_size, self.road_length]

        else:
            raise ValueError(f"Invalid direction: {direction}")

        # Khởi tạo Way
        self.way = Way(self.pos, self.size, direction, lane_widths_dir1, lane_widths_dir2)

        # Gắn road vào intersection nếu có
        if self.start:
            self.start.add_road(self)
        if self.end:
            self.end.add_road(self)

        self.calculate_geometry()

    def calculate_geometry(self):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def get_rect(self, expand: int = 0) -> pygame.Rect:
        return self.rect.inflate(expand, expand)

    def render(self, display: pygame.Surface, offset: tuple[int, int]) -> None:
        self.way.render(display, offset)
