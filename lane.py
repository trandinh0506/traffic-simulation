import pygame
import random
from typing import TYPE_CHECKING
from constant import *
from utils import reverseDirection

if TYPE_CHECKING:
    from way import Way

class Lane:
    def __init__(self, x: int, y: int, width: int, height: int, direction: str, way: "Way", lane_number: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.way = way
        self.direction = direction  # "left", "right", "up", "down"
        self.lane_number = lane_number  # Số hiệu của lane
        # Lưu một giá trị offset cố định cho arrow của lane (chọn ngẫu nhiên một lần)
        self.arrow_offset = random.randint(-7, 7) * 4

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    def render(self, display: pygame.Surface, offset: tuple[int, int]) -> None:
        # Vẽ nền lane (màu xám)
        pygame.draw.rect(
            display,
            (128, 128, 128),
            pygame.Rect(
                self.x - offset[0],
                self.y - offset[1],
                self.width,
                self.height
            )
        )
        # Vẽ mũi tên chỉ hướng cho lane
        self.draw_arrows(display, offset)

        # Vẽ số hiệu lane lên trên (cho mục đích debug)
        font = pygame.font.SysFont("times", 12)
        text_surface = font.render(f"{self.lane_number}", True, (255, 255, 255))
        display.blit(text_surface, (self.x - offset[0] + 5, self.y - offset[1] + 5))

    def draw_arrows(self, display: pygame.Surface, offset: tuple[int, int],
                arrow_total_length: int = 25,
                base_gap: int = 180,
                arrow_thickness: int = 10,
                arrow_color: tuple[int, int, int] = (255, 255, 255)
                ) -> None:
        """
        Vẽ arrow composite (shaft + tip) lặp lại dọc theo lane.
        Không vẽ trong vùng thụt đầu dòng 80px ở hai đầu.
        """
        effective_gap = base_gap + self.arrow_offset
        indent = 80  # Khoảng thụt đầu dòng

        if self.direction in ("right", "left"):
            center_y = self.y + self.height // 2 - offset[1]
            if self.direction == "right":
                start_x = self.x + indent + effective_gap // 2 - offset[0]  # Bắt đầu từ indent
                end_x = self.x + self.width - indent - arrow_total_length - offset[0]  # Kết thúc trước indent
                pos = start_x
                while pos < end_x:
                    self.draw_composite_arrow(display, (pos, center_y), self.direction,
                                            arrow_total_length, arrow_thickness, arrow_color)
                    pos += effective_gap
            else:  # left
                start_x = self.x + self.width - indent - effective_gap // 2 - offset[0]
                end_x = self.x + indent + arrow_total_length - offset[0]
                pos = start_x
                while pos > end_x:
                    self.draw_composite_arrow(display, (pos, center_y), self.direction,
                                            arrow_total_length, arrow_thickness, arrow_color)
                    pos -= effective_gap
        else:
            center_x = self.x + self.width // 2 - offset[0]
            if self.direction == "down":
                start_y = self.y + indent + effective_gap // 2 - offset[1]
                end_y = self.y + self.height - indent - arrow_total_length - offset[1]
                pos = start_y
                while pos < end_y:
                    self.draw_composite_arrow(display, (center_x, pos), self.direction,
                                            arrow_total_length, arrow_thickness, arrow_color)
                    pos += effective_gap
            else:  # up
                start_y = self.y + self.height - indent - effective_gap // 2 - offset[1]
                end_y = self.y + indent + arrow_total_length - offset[1]
                pos = start_y
                while pos > end_y:
                    self.draw_composite_arrow(display, (center_x, pos), self.direction,
                                            arrow_total_length, arrow_thickness, arrow_color)
                    pos -= effective_gap

    def draw_composite_arrow(self, display: pygame.Surface, start_pos: tuple[float, float],
                             direction: str,
                             arrow_total_length: int, arrow_thickness: int,
                             arrow_color: tuple[int, int, int]) -> None:
        shaft_length = int(arrow_total_length * 0.7)
        tip_length = arrow_total_length - shaft_length
        x, y = start_pos

        if direction == "right":
            shaft_rect = pygame.Rect(x, y - arrow_thickness // 2, shaft_length, arrow_thickness)
            pygame.draw.rect(display, arrow_color, shaft_rect)
            tip_points = [
                (x + shaft_length, y - arrow_thickness // 2),
                (x + shaft_length, y + arrow_thickness // 2),
                (x + arrow_total_length, y)
            ]
            pygame.draw.polygon(display, arrow_color, tip_points)
        elif direction == "left":
            shaft_rect = pygame.Rect(x - shaft_length, y - arrow_thickness // 2, shaft_length, arrow_thickness)
            pygame.draw.rect(display, arrow_color, shaft_rect)
            tip_points = [
                (x - shaft_length, y - arrow_thickness // 2),
                (x - shaft_length, y + arrow_thickness // 2),
                (x - arrow_total_length, y)
            ]
            pygame.draw.polygon(display, arrow_color, tip_points)
        elif direction == "down":
            shaft_rect = pygame.Rect(x - arrow_thickness // 2, y, arrow_thickness, shaft_length)
            pygame.draw.rect(display, arrow_color, shaft_rect)
            tip_points = [
                (x - arrow_thickness // 2, y + shaft_length),
                (x + arrow_thickness // 2, y + shaft_length),
                (x, y + arrow_total_length)
            ]
            pygame.draw.polygon(display, arrow_color, tip_points)
        elif direction == "up":
            shaft_rect = pygame.Rect(x - arrow_thickness // 2, y - shaft_length, arrow_thickness, shaft_length)
            pygame.draw.rect(display, arrow_color, shaft_rect)
            tip_points = [
                (x - arrow_thickness // 2, y - shaft_length),
                (x + arrow_thickness // 2, y - shaft_length),
                (x, y - arrow_total_length)
            ]
            pygame.draw.polygon(display, arrow_color, tip_points)

    def get_center(self) -> list[float]:
        return [self.rect.centerx, self.rect.centery]

    def get_entry_target_point(self) -> list[float]:
        """
        Trả về một điểm mục tiêu hợp lý để xe hướng tới khi rẽ vào lane này.
        Ví dụ: nếu lane có hướng RIGHT, điểm vào có thể cách mép trái của lane một khoảng nhất định.
        """
        if self.direction == RIGHT:
            return [self.rect.left + 30, self.rect.centery]
        elif self.direction == LEFT:
            return [self.rect.right - 30, self.rect.centery]
        elif self.direction == DOWN:
            return [self.rect.centerx, self.rect.top + 30]
        elif self.direction == UP:
            return [self.rect.centerx, self.rect.bottom - 30]
        return [self.rect.centerx, self.rect.centery]

    def is_same_direction(self, other_lane: "Lane") -> bool:
        return self.direction == other_lane.direction

    def is_opposite_direction(self, other_lane: "Lane") -> bool:
        return reverseDirection(self.direction) == other_lane.direction

    def belongs_to_same_way(self, other_lane: "Lane", way: "Way") -> bool:
        return self in way.lanes_list and other_lane in way.lanes_list
