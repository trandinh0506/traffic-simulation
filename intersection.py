from __future__ import annotations
import pygame
from typing import List, Tuple, TYPE_CHECKING


from lane import Lane

if TYPE_CHECKING:
    from road_segment import RoadSegment
    from car import Car

class Intersection:
    def __init__(self, x: int, y: int, size: int = 40, circular: bool = False) -> None:
        """
        :param x, y: Tọa độ trung tâm của intersection.
        :param size: Kích thước vùng giao cắt (vuông hoặc đường kính nếu circular).
        :param circular: Nếu True thì vẽ giao lộ hình tròn (vòng xuyến).
        """
        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.circular: bool = circular

        self.connected_roads: List[RoadSegment] = []
        self.entry_roads: List[RoadSegment] = []
        self.exit_roads: List[RoadSegment] = []

    def add_road(self, road: RoadSegment) -> None:
        """
        Thêm road vào intersection. Tự động phân loại entry/exit.
        """
        self.connected_roads.append(road)
        if road.end == self:
            self.entry_roads.append(road)
        if road.start == self:
            self.exit_roads.append(road)

    def render(self, display: pygame.Surface, offset: Tuple[int, int]) -> None:
        """
        Vẽ intersection – hình vuông hoặc hình tròn tùy theo chế độ.
        """
        screen_x = self.x - offset[0]
        screen_y = self.y - offset[1]

        if self.circular:
            radius = self.size // 2
            pygame.draw.circle(display, (160, 160, 160), (screen_x, screen_y), radius)
        else:
            rect = pygame.Rect(
                screen_x - self.size // 2,
                screen_y - self.size // 2,
                self.size,
                self.size
            )
            pygame.draw.rect(display, (128, 128, 128), rect)
            
    def get_center(self) -> tuple[int, int]:
        return (self.x, self.y)

    def get_rect(self) -> pygame.Rect:
        OFFSET = 25
        if self.circular:
            radius = self.size // 2
            return pygame.Rect(self.x - radius + OFFSET, self.y - radius + OFFSET, self.size - 2 * OFFSET, self.size - 2 * OFFSET)
        else:
            return pygame.Rect(self.x - self.size // 2 + OFFSET, self.y - self.size // 2 + OFFSET, self.size - 2 * OFFSET, self.size - 2 * OFFSET)
        
    def get_position(self) -> Tuple[int, int]:
        return self.x, self.y

    def get_entry_roads(self) -> List[RoadSegment]:
        return self.entry_roads

    def get_exit_roads(self) -> List[RoadSegment]:
        return self.exit_roads
    
    def get_valid_lanes_for(self, car: Car, currentLaneNumber: int) -> list[Lane]:
        """
        Trả về danh sách các lane hợp lệ mà xe có thể rẽ vào từ vị trí hiện tại.
        Dựa trên các road bắt đầu từ intersection này (exit_roads).
        """
        valid_lanes = []

        # Giả định car có thuộc tính current_lane
        current_lane = getattr(car, "current_lane", None)
        if not current_lane:
            return valid_lanes

        for road in self.exit_roads:
            way = road.way  # giả sử mỗi RoadSegment có thuộc tính `way`
            if way:
                valid_lanes.extend(way.get_valid_lanes_for_turn(current_lane, currentLaneNumber))

        return valid_lanes