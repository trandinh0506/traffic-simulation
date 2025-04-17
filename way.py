import pygame
from lane import Lane
from utils import drawDashedLine, is_turn_direction_valid, reverseDirection
from constant import LEFT, RIGHT, UP, DOWN

class Way:
    def __init__(
        self,
        pos: list[int],
        size: list[int],
        direction: str,
        lane_widths_dir1: list[int],
        lane_widths_dir2: list[int] = None
    ):
        self.pos = pos
        self.size = size[:]
        self.direction = direction
        self.lane_widths_dir1 = lane_widths_dir1
        self.lane_widths_dir2 = lane_widths_dir2
        self.is_two_way = (lane_widths_dir2 is not None)

        self.lanes_list: list[Lane] = []
        self.boundary_between_two_dir = None

        if self.direction in (LEFT, RIGHT):
            current_y = self.pos[1]

            # Tạo các lane cho "chiều 1"
            if self.direction == LEFT:
                # Ở chiều LEFT, lane_widths_dir1 nằm sát median trước => ta đảo ngược để lane 1 sát median
                self.lanes_list += self._build_lanes_horizontal_reversed(
                    self.pos[0],
                    current_y,
                    self.size[0],
                    self.lane_widths_dir1,
                    direction=LEFT,
                    isReversedLaneNumber=True
                )
                current_y += sum(self.lane_widths_dir1)

            elif self.direction == RIGHT:
                # Ở chiều RIGHT, lane_widths_dir1 cũng cần đảo thứ tự, để lane 1 sát median
                # nhưng ta gán lane hướng reverseDirection(RIGHT) để tạo lane “chiều 1”.
                self.lanes_list += self._build_lanes_horizontal_reversed(
                    self.pos[0],
                    current_y,
                    self.size[0],
                    self.lane_widths_dir1,
                    direction=reverseDirection(RIGHT),
                    isReversedLaneNumber=True
                )
                current_y += sum(self.lane_widths_dir1)

            self.boundary_between_two_dir = current_y

            # Chiều 2 (nếu có)
            if self.is_two_way:
                # Nếu là LEFT thì chiều 2 sẽ mang hướng reverseDirection(LEFT) => RIGHT
                # Nếu là RIGHT thì chiều 2 sẽ là RIGHT
                dir2 = reverseDirection(self.direction) if self.direction == LEFT else self.direction
                self.lanes_list += self._build_lanes_horizontal_reversed(
                    self.pos[0],
                    current_y,
                    self.size[0],
                    self.lane_widths_dir2,
                    direction=dir2
                )

        else:
            # direction in (UP, DOWN)
            current_x = self.pos[0]

            if self.direction == UP and self.is_two_way:
                # Tạo lane chiều ngược (DOWN) trước, đảo để lane 1 sát median
                self.lanes_list += self._build_lanes_vertical_reversed(
                    current_x,
                    self.pos[1],
                    self.lane_widths_dir2,
                    self.size[1],
                    reverseDirection(UP),
                    isReversedLaneNumber=True
                )
                current_x += sum(self.lane_widths_dir2)
                self.boundary_between_two_dir = current_x

            # Tạo lane cho chiều chính
            self.lanes_list += self._build_lanes_vertical_reversed(
                current_x,
                self.pos[1],
                self.lane_widths_dir1,
                self.size[1],
                self.direction,
                isReversedLaneNumber=True
            )
            current_x += sum(self.lane_widths_dir1)

            if self.direction == DOWN and self.is_two_way:
                self.boundary_between_two_dir = current_x
                self.lanes_list += self._build_lanes_vertical_reversed(
                    current_x,
                    self.pos[1],
                    self.lane_widths_dir2,
                    self.size[1],
                    reverseDirection(DOWN),
                )

    def _build_lanes_horizontal_reversed(self, x, start_y, width, lane_widths, direction, isReversedLaneNumber=False):
        """
        Tạo lane theo chiều ngang, với lane_number đảo ngược:
         - lane 1 sẽ là lane sát median,
         - lane cuối cùng sẽ là lane xa median nhất.
        """
        lanes = []
        # Đảo ngược lane_widths để lane đầu tiên trong danh sách được đánh lane_number lớn
        # lane cuối cùng trong danh sách => lane_number = 1.
        # Ta sẽ duyệt ngược, nhưng khi tạo Lane, gán lane_number theo thứ tự 1..n để lane 1 luôn sát median.
        total_lanes = len(lane_widths)
        # lane_widths_reversed = list(reversed(lane_widths))
        # Thay vì reversed thực sự, ta chỉ tính lane_number = total_lanes - i + 1

        y = start_y
        for i, w in enumerate(reversed(lane_widths), start=1):
            lane_number = total_lanes - i + 1 if isReversedLaneNumber else i  # lane 1 là lane sát median (tức i=1 trong reversed)
            lanes.append(Lane(x, y, width, w, direction, self, lane_number=lane_number))
            y += w
        return lanes

    def _build_lanes_vertical_reversed(self, start_x, y, lane_widths, height, direction, isReversedLaneNumber=False):
        """
        Tương tự như horizontal, nhưng cho chiều dọc.
        """
        lanes = []
        total_lanes = len(lane_widths)
        x = start_x
        for i, w in enumerate(reversed(lane_widths), start=1):
            lane_number = total_lanes - i + 1 if isReversedLaneNumber else i
            lanes.append(Lane(x, y, w, height, direction, self, lane_number=lane_number))
            x += w
        return lanes

    def render(self, display: pygame.Surface, offset: tuple[int, int]) -> None:
        for lane in self.lanes_list:
            lane.render(display, offset)

        self.drawOuterBorder(display, offset)
        self.drawLaneDividers(display, offset)
        self.drawCenterLine(display, offset)

    def drawOuterBorder(self, display, offset):
        if not self.lanes_list:
            return
        first = self.lanes_list[0]
        last = self.lanes_list[-1]

        if self.direction in (LEFT, RIGHT):
            y_top = first.y - offset[1]
            y_bot = last.y + last.height - offset[1]
            x1 = first.x - offset[0]
            x2 = first.x + first.width - offset[0]

            pygame.draw.line(display, (255, 255, 255), (x1, y_top), (x2, y_top), 2)
            pygame.draw.line(display, (255, 255, 255), (x1, y_bot), (x2, y_bot), 2)
        else:
            x_left = first.x - offset[0]
            x_right = last.x + last.width - offset[0]
            y1 = first.y - offset[1]
            y2 = first.y + first.height - offset[1]

            pygame.draw.line(display, (255, 255, 255), (x_left, y1), (x_left, y2), 2)
            pygame.draw.line(display, (255, 255, 255), (x_right, y1), (x_right, y2), 2)

    def drawLaneDividers(self, display, offset):
        if len(self.lanes_list) < 2:
            return

        for i in range(1, len(self.lanes_list)):
            prev_lane = self.lanes_list[i - 1]
            curr_lane = self.lanes_list[i]

            if self.direction in (LEFT, RIGHT):
                y_div = (prev_lane.y + prev_lane.height + curr_lane.y) / 2.0
                y_div -= offset[1]

                x1 = curr_lane.x - offset[0]
                x2 = curr_lane.x + curr_lane.width - offset[0]

                drawDashedLine(display, (255, 255, 255), (x1, y_div), (x2, y_div), width=2)
            else:
                x_div = (prev_lane.x + prev_lane.width + curr_lane.x) / 2.0
                x_div -= offset[0]

                y1 = curr_lane.y - offset[1]
                y2 = curr_lane.y + curr_lane.height - offset[1]

                drawDashedLine(display, (255, 255, 255), (x_div, y1), (x_div, y2), width=2)

    def drawCenterLine(self, display, offset):
        if not self.is_two_way:
            return

        if self.direction in (LEFT, RIGHT):
            y_mid = self.boundary_between_two_dir - offset[1]
            x1 = self.pos[0] - offset[0]
            x2 = self.pos[0] + self.size[0] - offset[0]
            drawDashedLine(display, (255, 255, 0), (x1, y_mid), (x2, y_mid), width=4)
        else:
            x_mid = self.boundary_between_two_dir - offset[0]
            y1 = self.pos[1] - offset[1]
            y2 = self.pos[1] + self.size[1] - offset[1]
            drawDashedLine(display, (255, 255, 0), (x_mid, y1), (x_mid, y2), width=4)

    def get_valid_lanes_for_turn(self, current_lane: Lane, currentLaneNumber: int) -> list[Lane]:
        """
        Trả về danh sách lane hợp lệ để chuyển hướng từ current_lane.
        """
        valid_lanes = []
        if not current_lane:
            return valid_lanes

        cx, cy = current_lane.get_center()
        cur_dir = current_lane.direction

        for lane in self.lanes_list:
            if lane is current_lane:
                continue

            lx, ly = lane.get_center()
            target_dir = lane.direction

            # Đi thẳng
            if target_dir == cur_dir and lane.way != current_lane.way:
                valid_lanes.append(lane)
            # Quay đầu
            elif target_dir == reverseDirection(cur_dir) and lane.way == current_lane.way and currentLaneNumber == 1:
                valid_lanes.append(lane)
            # Rẽ trái/phải
            elif lane.way != current_lane.way and is_turn_direction_valid(cur_dir, (cx, cy), (lx, ly), target_dir, currentLaneNumber):
                valid_lanes.append(lane)
        return valid_lanes

    def get_same_direction_lanes(self, direction: str) -> list[Lane]:
        return [lane for lane in self.lanes_list if lane.direction == direction]
