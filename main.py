import pygame
import sys
from map import Map
from car import Car
pygame.init()

class Simulation(object):
    def __init__(self):
        self.screen: pygame.Surface = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("TRAFFIC SIMULATION")
        self.running: bool = True
        self.map: Map = Map()
        self.cars: list[Car] = [Car([350, 120], (0.03, 0), "right")]
    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.map.render(self.screen)
            for car in self.cars:
                car.update()
                car.render(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit(0)
                    
            pygame.display.update()


def main():
    Simulation().run()


if __name__ == "__main__":
    main()