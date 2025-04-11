import pygame
from intersection import Intersection
from road_segment import RoadSegment
from constant import *

class TrafficNetwork:
    def __init__(self) -> None:
        self.intersections: dict[str, Intersection] = {}
        self.roads: list[RoadSegment] = []

        self._create_intersections()
        self._create_roads()

    def _create_intersections(self) -> None:
        # Tạo ngã tư inter0 và inter1
        self.intersections["inter0"] = Intersection(400, 400, 240)
        self.intersections["inter1"] = Intersection(400 + 1200, 400, 240)

    def _create_roads(self) -> None:
        inter0 = self.intersections["inter0"]
        inter1 = self.intersections["inter1"]

        def add_road(start, end, direction, length=600):
            road = RoadSegment(
                start_intersection=start,
                end_intersection=end,
                direction=direction,
                road_length=length,
                half_lane_total=120,
                lane_widths_dir1=[60, 60],
                lane_widths_dir2=[60, 60]
            )
            self.roads.append(road)

        # inter0 → inter1
        add_road(inter0, inter1, RIGHT, 1200)

        # inter1 → tiếp phải
        add_road(inter1, None, RIGHT)

        # Các hướng từ inter0
        add_road(inter0, None, LEFT)
        add_road(inter0, None, DOWN)
        add_road(inter0, None, UP)

        # Các hướng từ inter1
        add_road(inter1, None, DOWN)
        add_road(inter1, None, UP)

        # (Có thể thêm inter1 ← inter0 nếu muốn hai chiều)

    def render(self, display: pygame.Surface, offset: tuple[int, int]) -> None:
        for road in self.roads:
            road.render(display, offset)
        for inter in self.intersections.values():
            inter.render(display, offset)
