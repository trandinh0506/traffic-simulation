import pygame

class Way:
    def __init__(self, pos: list[int], size: list[int], lanes: int, direction: str):
        self.pos = pos
        self.size = size
        self.lanes = lanes
        self.direction = direction
        if self.direction in ("up", "down"):
            self.size = [self.size[1], self.size[0]]
            
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos, self.size)

    def render(self, display: pygame.Surface) -> None:
        
        pygame.draw.rect(display, (128, 128, 128), self.rect())
        
        if self.direction in ("left", "right"):
            lane_width = self.size[1] / self.lanes
            for i in range(1, self.lanes):
                y = self.pos[1] + int(i * lane_width)
                pygame.draw.line(display, (255, 255, 255), (self.pos[0], y), (self.pos[0] + self.size[0], y), 2)

        else:
            lane_width = self.size[0] / self.lanes
            for i in range(1, self.lanes):
                x = self.pos[0] + int(i * lane_width)
                pygame.draw.line(display, (255, 255, 255), (x, self.pos[1]), (x, self.pos[1] + self.size[1]), 2)
