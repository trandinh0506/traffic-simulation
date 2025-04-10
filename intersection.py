import pygame

class Intersection:
    def __init__(self, x: int, y: int, gap: int):
        """
        :param x, y: Tọa độ trung tâm của intersection.
        :param gap: Khoảng trống xung quanh trung tâm để vẽ vùng giao cắt.
        """
        self.x = x
        self.y = y
        self.gap = gap  # Gap thực sự tại trung tâm intersection.
        self.connected_roads = []  # Danh sách RoadSegment nối đến intersection.

    def add_road(self, road):
        self.connected_roads.append(road)

    def render(self, display: pygame.Surface, offset: tuple[int, int]):
        # Vẽ vùng giao cắt với màu xám (hoặc màu khác tuỳ ý)
        rect = pygame.Rect(
            self.x - self.gap//2 - offset[0],
            self.y - self.gap//2 - offset[1],
            self.gap,
            self.gap
        )
        pygame.draw.rect(display, (128, 128, 128), rect)
