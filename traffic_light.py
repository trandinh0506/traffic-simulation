from typing import Optional
import pygame
from constant import *

class TrafficLight:
    def __init__(self, pos: list[int], cycle: int, direction: str, roadWidth: int, currentLight: str, greenDuration: int, remain: float):
        self.pos = pos
        self.cycle = cycle
        self.currentLight = currentLight
        self.remain: float = remain
        self.greenDuration = greenDuration
        self.yellowDuration = YELLOW_DURATION
        self.redDuration = self.cycle - self.greenDuration - self.yellowDuration
        self.direction = direction
        self.lightRadius: int = 18
        self.stopLine: Optional[pygame.Rect] = None
        self.stopLinePos = [self.pos[0], self.pos[1]]
        self.lightPos = [self.pos[0], self.pos[1]]
        self.timerPos = [0, 0]
        lightOffset = 30
        timerOffset = 35
        if direction == UP:
            self.stopLinePos[0] -= roadWidth
            self.lightPos[0] += lightOffset
            self.lightPos[1] -= STOPLINE_HEIGHT
            self.timerPos[0] = self.lightPos[0] - self.lightRadius
            self.timerPos[1] = self.lightPos[1] - timerOffset - self.lightRadius
        elif direction == DOWN:
            self.stopLinePos[0] += roadWidth
            self.stopLinePos[1] -= STOPLINE_HEIGHT
            self.lightPos[0] += roadWidth - lightOffset
            self.lightPos[1] += STOPLINE_HEIGHT
            self.timerPos[0] = self.lightPos[0] - self.lightRadius
            self.timerPos[1] = self.lightPos[1] + self.lightRadius
        elif direction == LEFT:
            self.stopLinePos[1] += roadWidth
            self.lightPos[1] += roadWidth - lightOffset
            self.lightPos[0] -= STOPLINE_HEIGHT
            self.timerPos[0] = self.lightPos[0] - timerOffset - self.lightRadius
            self.timerPos[1] = self.lightPos[1] - self.lightRadius
        else:
            self.stopLinePos[0] += STOPLINE_HEIGHT
            self.stopLinePos[1] -= roadWidth
            self.lightPos[0] += STOPLINE_HEIGHT * 3
            self.lightPos[1] += lightOffset
            self.timerPos[0] = self.lightPos[0] + STOPLINE_HEIGHT
            self.timerPos[1] = self.lightPos[1] - self.lightRadius
        
        self.stopLine = pygame.Rect(self.stopLinePos, ((STOPLINE_HEIGHT, roadWidth) if  direction in (LEFT, RIGHT) else (roadWidth, STOPLINE_HEIGHT)))
    def update(self, delta_t: float):
        self.remain -= delta_t
        if self.remain <= 0:
            if self.currentLight == RED:
                self.currentLight = GREEN
                self.remain = self.greenDuration
            elif self.currentLight == GREEN:
                self.currentLight = YELLOW
                self.remain = self.yellowDuration
            elif self.currentLight == YELLOW:
                self.currentLight = RED
                self.remain = self.redDuration
    def render(self, display: pygame.Surface, offset: tuple[int, int]):
        font = pygame.font.SysFont("sans", 35)
        color = TEXT2COLOR[self.currentLight]
        remainInt = math.ceil(self.remain)
        textRemainder = str(remainInt) if remainInt > 9 else '0' + str(remainInt)
        timeRender = font.render(textRemainder, True, color)
        
        pygame.draw.circle(display, color, (self.lightPos[0] - offset[0], self.lightPos[1] - offset[1]), self.lightRadius)
        
        pygame.draw.rect(display, (255, 255, 255), (self.stopLine.left - offset[0], self.stopLine.top - offset[1], self.stopLine.width, self.stopLine.height))
        
        display.blit(timeRender, (self.timerPos[0] - offset[0], self.timerPos[1] - offset[1]))