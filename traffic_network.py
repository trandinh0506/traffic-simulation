
import pygame
from intersection import Intersection
from road_segment import RoadSegment
from constant import *
class TrafficNetwork:
    def __init__(self):
        self.intersections = []
        self.roads = []

        # Tạo 2 intersection
        inter0 = Intersection(400, 400, 240)
        inter1 = Intersection(400 + 1200, 400, 240)
        self.intersections.extend([inter0, inter1])

        # inter0 → inter1 (RIGHT)
        self.roads.append(RoadSegment(
            start_intersection=inter0,
            end_intersection=inter1,
            direction=RIGHT,
            road_length=1200,
            half_lane_total=120,
            lane_widths_dir1=[60, 60],
            lane_widths_dir2=[60, 60]
        ))

        # inter1 → phải tiếp (RIGHT)
        self.roads.append(RoadSegment(
            start_intersection=inter1,
            end_intersection=None,
            direction=RIGHT,
            road_length=600,
            half_lane_total=120,
            lane_widths_dir1=[60, 60],
            lane_widths_dir2=[60, 60]
        ))

        # Đường trái từ inter0 (LEFT)
        self.roads.append(RoadSegment(
            start_intersection=inter0,
            end_intersection=None,
            direction=LEFT,
            road_length=600,
            half_lane_total=120,
            lane_widths_dir1=[60, 60],
            lane_widths_dir2=[60, 60]
        ))

        # Đường đi xuống từ inter0
        self.roads.append(RoadSegment(
            start_intersection=inter0,
            end_intersection=None,
            direction=DOWN,
            road_length=600,
            half_lane_total=120,
            lane_widths_dir1=[60, 60],
            lane_widths_dir2=[60, 60]
        ))

        # Đường đi lên từ inter0
        self.roads.append(RoadSegment(
            start_intersection=inter0,
            end_intersection=None,
            direction=UP,
            road_length=600,
            half_lane_total=120,
            lane_widths_dir1=[60, 60],
            lane_widths_dir2=[60, 60]
        ))

        # Đường đi xuống từ inter1
        self.roads.append(RoadSegment(
            start_intersection=inter1,
            end_intersection=None,
            direction=DOWN,
            road_length=600,
            half_lane_total=120,
            lane_widths_dir1=[60, 60],
            lane_widths_dir2=[60, 60]
        ))

        # Đường đi lên từ inter1
        self.roads.append(RoadSegment(
            start_intersection=inter1,
            end_intersection=None,
            direction=UP,
            road_length=600,
            half_lane_total=120,
            lane_widths_dir1=[60, 60],
            lane_widths_dir2=[60, 60]
        ))

        # Nếu muốn inter1 ← trái (quay lại inter0) có thể thêm road ngược lại nếu thích

    def render(self, display: pygame.Surface, offset: tuple[int, int]) -> None:
        for road in self.roads:
            road.render(display, offset)
        for inter in self.intersections:
            inter.render(display, offset)
