import pygame
from lane import Lane
from utils import *
from constant import *

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

        self.lanes_list = []
        self.boundary_between_two_dir = None

        if self.direction in (LEFT, RIGHT):
            current_y = self.pos[1]
            
            if self.direction == LEFT:
                for w in self.lane_widths_dir1:
                    self.lanes_list.append(Lane(self.pos[0], current_y, self.size[0], w, self.direction))
                    current_y += w
                    
            if self.is_two_way and self.direction == RIGHT:
                for w in self.lane_widths_dir1:
                    self.lanes_list.append(Lane(self.pos[0], current_y, self.size[0], w, reverseDirection(self.direction)))
                    current_y += w
                    
            self.boundary_between_two_dir = current_y
            
            if self.direction == LEFT and self.is_two_way:
                for w in self.lane_widths_dir2:
                    self.lanes_list.append(Lane(self.pos[0], current_y, self.size[0], w, reverseDirection(self.direction)))
                    current_y += w
            
            if self.direction == RIGHT and self.is_two_way:
                for w in self.lane_widths_dir2:
                    self.lanes_list.append(Lane(self.pos[0], current_y, self.size[0], w, (self.direction)))
                    current_y += w
                    
        else:
            current_x = self.pos[0]

            if self.direction == UP and self.is_two_way:
                for w in self.lane_widths_dir2:
                    self.lanes_list.append(Lane(current_x, self.pos[1], w, self.size[1], reverseDirection(self.direction)))
                    current_x += w
                self.boundary_between_two_dir = current_x

            for w in self.lane_widths_dir1:
                self.lanes_list.append(Lane(current_x, self.pos[1], w, self.size[1], self.direction))
                current_x += w

            if self.direction == DOWN and self.is_two_way:
                self.boundary_between_two_dir = current_x
                for w in self.lane_widths_dir2:
                    self.lanes_list.append(Lane(current_x, self.pos[1], w, self.size[1], reverseDirection(self.direction)))
                    current_x += w

    def render(self, display: pygame.Surface, offset: tuple[int, int]) -> None:
        for lane in self.lanes_list:
            lane.render(display, offset)

        self.drawOuterBorder(display, offset)
        self.drawLaneDividers(display, offset)
        self.drawCenterLine(display, offset)

    def drawOuterBorder(self, display, offset):
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