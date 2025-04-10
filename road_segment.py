from lane import Lane
from utils import *

class RoadSegment:
    def __init__(self, start_intersection, end_intersection, direction: str,
                 road_length: int, half_lane_total: int,
                 lane_widths_dir1: list[int], lane_widths_dir2: list[int]):
        """
        :param start_intersection: Intersection xuất phát.
        :param end_intersection: Intersection kết thúc.
        :param direction: Hướng chung của đoạn đường (VD: "left", "right", "up", "down").
                          Lưu ý, trong một đoạn road 2 chiều, nhóm lane thứ nhất sẽ dùng hướng này,
                          nhóm lane thứ hai sẽ được reverse.
        :param road_length: Chiều dài của road (theo hướng của road).
        :param half_lane_total: Kích thước của nửa road (cho 1 chiều), dùng để tính kích thước lan.
        :param lane_widths_dir1, lane_widths_dir2: Các danh sách kích thước lane (cho 1 chiều).
        """
        self.start = start_intersection
        self.end = end_intersection
        self.direction = direction
        self.road_length = road_length
        self.half_lane_total = half_lane_total
        self.lane_widths_dir1 = lane_widths_dir1
        self.lane_widths_dir2 = lane_widths_dir2

        # Tính toán toạ độ xuất phát dựa trên intersection và hướng của road.
        # Ví dụ, với road ngang:
        #   Nếu road mở sang phải, pos của road = (intersection.x + gap/2, intersection.y - half_lane_total)
        #   Nếu mở sang trái, pos = (intersection.x - gap/2 - road_length, intersection.y - half_lane_total)
        # Với road dọc:
        #   Nếu road mở xuống, pos = (intersection.x - half_lane_total, intersection.y + gap/2)
        #   Nếu mở lên, pos = (intersection.x - half_lane_total, intersection.y - gap/2 - road_length)
        # Ở đây, bạn có thể cung cấp thêm một tham số (như “side”) để chỉ định vị trí tương đối của road tại intersection.
        #
        # Giả sử ta làm đơn giản: pos là tính dựa trên hướng và một offset dựa trên gap của intersection.
        gap = self.start.gap
        if direction in ("right", "left"):
            if direction == "right":
                pos_x = self.start.x + gap // 2
            else:
                pos_x = self.start.x - gap // 2 - road_length
            pos_y = self.start.y - half_lane_total
            self.pos = [pos_x, pos_y]
            self.size = [road_length, half_lane_total]  # Kích thước của nửa road
        else:
            if direction == "down":
                pos_y = self.start.y + gap // 2
            else:
                pos_y = self.start.y - gap // 2 - road_length
            pos_x = self.start.x - half_lane_total
            self.pos = [pos_x, pos_y]
            self.size = [half_lane_total, road_length]

        # Tạo RoadSegment theo logic của Way (có thể tái sử dụng lớp Way)
        from way import Way  # giả sử lớp Way đã được refactor
        self.way = Way(self.pos, self.size, direction,
                       lane_widths_dir1, lane_widths_dir2)

    def render(self, display: pygame.Surface, offset: tuple[int, int]) -> None:
        self.way.render(display, offset)
