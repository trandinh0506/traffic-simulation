import pygame
import random

class Lane:
    def __init__(self, x: int, y: int, width: int, height: int, direction: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = direction  # "left", "right", "up", "down"
        # Lưu một giá trị offset cố định cho arrow của lane (chọn random 1 lần)
        # Bạn có thể tùy chỉnh mức độ lệch này (ví dụ ±3 pixel)
        self.arrow_offset = random.randint(-7, 7) * 4
        # Nếu cần hoạt ảnh arrow chạy dọc lane, bạn có thể lưu thêm base_position.
        # Ví dụ: self.arrow_base = 0

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

    def draw_arrows(self, display: pygame.Surface, offset: tuple[int, int],
                    arrow_total_length: int = 25,   # Giảm chiều dài tổng để tip không quá dài
                    base_gap: int = 180,             # Khoảng cách cơ sở giữa các mũi tên
                    arrow_thickness: int = 10,       # Điều chỉnh độ dày cho phù hợp
                    arrow_color: tuple[int, int, int] = (255, 255, 255)
                    ) -> None:
        """
        Vẽ arrow composite (shaft + tip) lặp lại dọc theo lane.
        Sử dụng self.arrow_offset đã lưu để có một gap cố định (có thêm độ lệch nhẹ).
        """
        # Cộng thêm arrow_offset vào base_gap để đảm bảo gap không thay đổi giữa các frame.
        effective_gap = base_gap + self.arrow_offset

        if self.direction in ("right", "left"):
            center_y = self.y + self.height // 2 - offset[1]
            if self.direction == "right":
                start_x = self.x + effective_gap//2 - offset[0]
                end_x = self.x + self.width - arrow_total_length - offset[0]
                pos = start_x
                while pos < end_x:
                    self.draw_composite_arrow(display, (pos, center_y), self.direction,
                                              arrow_total_length, arrow_thickness, arrow_color)
                    pos += effective_gap
            else:  # left
                start_x = self.x + self.width - effective_gap//2 - offset[0]
                end_x = self.x + arrow_total_length - offset[0]
                pos = start_x
                while pos > end_x:
                    self.draw_composite_arrow(display, (pos, center_y), self.direction,
                                              arrow_total_length, arrow_thickness, arrow_color)
                    pos -= effective_gap
        else:
            center_x = self.x + self.width // 2 - offset[0]
            if self.direction == "down":
                start_y = self.y + effective_gap//2 - offset[1]
                end_y = self.y + self.height - arrow_total_length - offset[1]
                pos = start_y
                while pos < end_y:
                    self.draw_composite_arrow(display, (center_x, pos), self.direction,
                                              arrow_total_length, arrow_thickness, arrow_color)
                    pos += effective_gap
            else:  # up
                start_y = self.y + self.height - effective_gap//2 - offset[1]
                end_y = self.y + arrow_total_length - offset[1]
                pos = start_y
                while pos > end_y:
                    self.draw_composite_arrow(display, (center_x, pos), self.direction,
                                              arrow_total_length, arrow_thickness, arrow_color)
                    pos -= effective_gap

    def draw_composite_arrow(self, display: pygame.Surface, start_pos: tuple[float, float],
                             direction: str,
                             arrow_total_length: int, arrow_thickness: int,
                             arrow_color: tuple[int, int, int]) -> None:
        """
        Vẽ arrow composite:
          - Shaft: hình chữ nhật chiếm 70% chiều dài arrow_total_length.
          - Tip: phần tam giác chiếm phần còn lại.
        """
        # Điều chỉnh tỉ lệ cho mũi tên: shaft_length = 70% tổng chiều dài.
        shaft_length = int(arrow_total_length * 0.7)
        tip_length = arrow_total_length - shaft_length
        x, y = start_pos

        if direction == "right":
            shaft_rect = pygame.Rect(x, y - arrow_thickness//2, shaft_length, arrow_thickness)
            pygame.draw.rect(display, arrow_color, shaft_rect)
            tip_points = [
                (x + shaft_length, y - arrow_thickness//2),
                (x + shaft_length, y + arrow_thickness//2),
                (x + arrow_total_length, y)
            ]
            pygame.draw.polygon(display, arrow_color, tip_points)
        elif direction == "left":
            shaft_rect = pygame.Rect(x - shaft_length, y - arrow_thickness//2, shaft_length, arrow_thickness)
            pygame.draw.rect(display, arrow_color, shaft_rect)
            tip_points = [
                (x - shaft_length, y - arrow_thickness//2),
                (x - shaft_length, y + arrow_thickness//2),
                (x - arrow_total_length, y)
            ]
            pygame.draw.polygon(display, arrow_color, tip_points)
        elif direction == "down":
            shaft_rect = pygame.Rect(x - arrow_thickness//2, y, arrow_thickness, shaft_length)
            pygame.draw.rect(display, arrow_color, shaft_rect)
            tip_points = [
                (x - arrow_thickness//2, y + shaft_length),
                (x + arrow_thickness//2, y + shaft_length),
                (x, y + arrow_total_length)
            ]
            pygame.draw.polygon(display, arrow_color, tip_points)
        elif direction == "up":
            shaft_rect = pygame.Rect(x - arrow_thickness//2, y - shaft_length, arrow_thickness, shaft_length)
            pygame.draw.rect(display, arrow_color, shaft_rect)
            tip_points = [
                (x - arrow_thickness//2, y - shaft_length),
                (x + arrow_thickness//2, y - shaft_length),
                (x, y - arrow_total_length)
            ]
            pygame.draw.polygon(display, arrow_color, tip_points)
