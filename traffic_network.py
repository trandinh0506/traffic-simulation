from typing import Optional
import pygame
from intersection import Intersection
from road_segment import RoadSegment
from traffic_light import TrafficLight
from constant import *
from utils import *
class TrafficNetwork:
    def __init__(self) -> None:
        self.intersections: dict[str, Intersection] = {}
        self.roads: list[RoadSegment] = []
        self.trafficLights: list[TrafficLight] = []

        self._create_intersections()
        self._create_roads()
        self._createTrafficLight()
    def _create_intersections(self) -> None:
        # Tạo ngã tư inter0 và inter1
        self.intersections["inter0"] = Intersection(400, 400, 240)
        self.intersections["inter1"] = Intersection(400 + 1600, 400, 240)
        self.intersections["inter2"] = Intersection(400, 400+1600, 240)

    def _create_roads(self) -> None:
        inter0 = self.intersections["inter0"]
        inter1 = self.intersections["inter1"]
        inter2 = self.intersections["inter2"]
        def add_road(start: Optional[Intersection], end: Optional[Intersection], direction: str, length=700):
            road = RoadSegment(
                start_intersection=start,
                end_intersection=end,
                direction=direction,
                road_length=length,
                half_lane_total=120,
                lane_widths_dir1=[60, 60],
                lane_widths_dir2=[60, 60],
            )
            self.roads.append(road)

        add_road(inter0, inter1, RIGHT, 1200)
        add_road(inter1, None, RIGHT)
        add_road(inter0, None, LEFT)
        add_road(inter0, None, DOWN)
        add_road(inter0, None, UP)
        add_road(inter1, None, DOWN)
        add_road(inter1, None, UP)
        add_road(inter1, None, LEFT)
        add_road(inter0, inter2, DOWN, 1200)
        add_road(inter2, None, RIGHT)
        add_road(inter2, None, LEFT)
        add_road(inter2, None, UP)
        add_road(inter2, None, DOWN)

    def _createTrafficLight(self):
        def addTrafficLight(pos: list[int], cycle: int, direction: str, roadWidth: int = 120):
            trafficLight = TrafficLight(pos, cycle, direction, roadWidth)
            self.trafficLights.append(trafficLight)
        
        addTrafficLight([520, 600], 20, UP)
        addTrafficLight([160, 520], 20, RIGHT)
        addTrafficLight([160, 200], 20, DOWN)
        addTrafficLight([600, 160], 20, LEFT)

    def getIntersections(self) -> list[Intersection]:
        intersections = []
        for inter in self.intersections.values():
            intersections.append(inter)
            
        return intersections
    def render(self, display: pygame.Surface, offset: tuple[int, int]) -> None:
        for road in self.roads:
            road.render(display, offset)
        for inter in self.intersections.values():
            inter.render(display, offset)

        for trafficLight in self.trafficLights:
            trafficLight.render(display, offset)