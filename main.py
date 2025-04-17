import pygame
import sys
from traffic_network import TrafficNetwork
from car import Car
from constant import *
pygame.init()

class Simulation(object):
    def __init__(self):
        self.screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # main screen used for blit display
        pygame.display.set_caption("TRAFFIC SIMULATION")
        self.running: bool = True
        self.trafficNetwork: TrafficNetwork = TrafficNetwork()
        # Car([490, 1200], UP)
        # Car([100, 430], RIGHT)
        # Car([430, 1000], UP)
        # Car([370, -50], DOWN)
        # Car([700, 370], LEFT)
        # , Car([490, 1200], UP), Car([370, -50], DOWN), Car([100, 430], RIGHT)
        # Car([700, 370], LEFT), Car([490, 1200], UP), Car([370, -50], DOWN),
        #                         Car([100, 430], RIGHT), Car([430, 1200], UP), Car([320, -50], DOWN)
        self.cars: list[Car] = [Car([700, 370], LEFT), Car([490, 900], UP), Car([370, -50], DOWN),
                                Car([100, 430], RIGHT), Car([430, 900], UP), Car([320, -50], DOWN)]
        self.scoll: list[int] = [0, 0]  
        self.leftMouseDown: bool = False
        self.leftMouseDownPos: tuple[int, int] = (0, 0)  
        self.startScroll: list[int] = self.scoll.copy()
        self.scaleRatio: float = 0.5
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            delta_t = self.clock.tick(60) / 1000
            mPos = pygame.mouse.get_pos()

            # if left mouse button pressed, calculate diff and update camera position
            if self.leftMouseDown:
                diff = (mPos[0] - self.leftMouseDownPos[0], mPos[1] - self.leftMouseDownPos[1])
                scrollRender = (int(self.startScroll[0] - diff[0]), int(self.startScroll[1] - diff[1]))
            else:
                scrollRender = (int(self.scoll[0]), int(self.scoll[1]))

            self.trafficNetwork.render(self.screen, scrollRender)
            for car in self.cars:
                car.update(delta_t, self.trafficNetwork.getIntersections(), self.trafficNetwork.roads, self.cars)
                car.render(self.screen, scrollRender)
                car.debug_render(self.screen, scrollRender)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftMouseDown = True
                        self.leftMouseDownPos = pygame.mouse.get_pos()
                        self.startScroll = self.scoll.copy()  # keep track of scroll when starting
                    if event.button == 4:
                        self.scaleRatio = min(2, self.scaleRatio + 0.1)
                        # self.screen = pygame.Surface((WORLD_WIDTH * self.scaleRatio, WORLD_HEIGHT * self.scaleRatio))
                    if event.button == 5:
                        self.scaleRatio = max(0.1, self.scaleRatio - 0.1)
                        # self.screen = pygame.Surface((WORLD_WIDTH * self.scaleRatio, WORLD_HEIGHT * self.scaleRatio))
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.leftMouseDown = False
                        # update scroll position base on last scroll position when unpressed mouse
                        self.scoll = [scrollRender[0], scrollRender[1]]
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit(0)
                    
            # pygame.draw.rect(self.screen, (255, 0, 0), (self.cars[0].get_rect().x - scrollRender[0], self.cars[0].get_rect().y - scrollRender[1], self.cars[0].get_rect().width, self.cars[0].get_rect().height))
            pygame.display.update()


def main():
    Simulation().run()


if __name__ == "__main__":
    main()
