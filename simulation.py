import random
import pygame
import sys
from traffic_light import TrafficLight
from traffic_network import TrafficNetwork
from car import Car
from constant import *
from utils import get_available_spawn_point, parse_param_string
pygame.init()

class Simulation():
    def __init__(self, stringParam):
        self.param: dict[str, any] = parse_param_string(stringParam)
        print("param:", self.param)
        self.totalCarCount = int(self.param.get('totalCarCount', 10))
        self.screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("TRAFFIC SIMULATION")
        self.running: bool = True
        self.trafficNetwork: TrafficNetwork = TrafficNetwork()
        self.cars: list[Car] = []
        self.activeCars: list[Car] = []
        self.scoll: list[int] = [0, 0]
        self.leftMouseDown: bool = False
        self.leftMouseDownPos: tuple[int, int] = (0, 0)  
        self.startScroll: list[int] = self.scoll.copy()
        self.clock = pygame.time.Clock()
        self.trafficLights: list[TrafficLight] = self.trafficNetwork.trafficLights
        EXPAND = 50
        self.cameraRect = pygame.Rect(self.scoll[0], self.scoll[1], SCREEN_WIDTH + EXPAND, SCREEN_HEIGHT + EXPAND)
        self.carsRender: list[Car] = []
    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            delta_t = self.clock.tick(60) / 1000
            mPos = pygame.mouse.get_pos()
            self.cameraRect.x = self.scoll[0]
            self.cameraRect.y = self.scoll[1]
            self.activeCars = [car for car in self.cars if car.isActive]
            self.carsRender = [car for car in self.activeCars if self.cameraRect.colliderect(car.get_rect())]
            for point in SPWAN_POINTS:
                if point["cooldown"] > 0:
                    point["cooldown"] -= delta_t
            
            if len(self.cars) < self.totalCarCount:
                point = get_available_spawn_point()
                for road in self.trafficNetwork.roads:
                    for lane in road.way.lanes_list:
                        if point and lane.rect.collidepoint(point["pos"]):
                            if lane.direction == point["dir"]:
                                new_car = Car(point["pos"][:], point["dir"])
                                self.cars.append(new_car)
                            

            if self.leftMouseDown:
                diff = (mPos[0] - self.leftMouseDownPos[0], mPos[1] - self.leftMouseDownPos[1])
                scrollRender = (int(self.startScroll[0] - diff[0]), int(self.startScroll[1] - diff[1]))
            else:
                scrollRender = (int(self.scoll[0]), int(self.scoll[1]))

            for trafficLight in self.trafficLights:
                trafficLight.update(delta_t)
                
            self.trafficNetwork.render(self.screen, scrollRender)
            
            for car in self.activeCars:
                car.update(delta_t, self.trafficNetwork.getIntersections(), self.trafficNetwork.roads, self.activeCars, self.trafficLights)
            
            for car in self.cars:
                if not car.isActive:
                    point = get_available_spawn_point()
                    for road in self.trafficNetwork.roads:
                        for lane in road.way.lanes_list:
                            if point and lane.rect.collidepoint(point["pos"]):
                                if lane.direction == point["dir"]:
                                    car.reset(point["pos"], point["dir"])
                                else:
                                    print(point)
            
            for car in self.carsRender:
                car.render(self.screen, scrollRender)
                # car.debug_render(self.screen, scrollRender)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftMouseDown = True
                        self.leftMouseDownPos = pygame.mouse.get_pos()
                        self.startScroll = self.scoll.copy()  # keep track of scroll when starting
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.leftMouseDown = False
                        # update scroll position base on last scroll position when unpressed mouse
                        self.scoll = [scrollRender[0], scrollRender[1]]
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit(0)
                    
            font = pygame.font.SysFont("sans", 15)
            mRender = font.render(str([mPos[0] + scrollRender[0], mPos[1] + scrollRender[1]]), True, (255, 0, 255))
            totalCarRender = font.render(str(len(self.cars)), True, (0, 255, 255))
            self.screen.blit(mRender, (0, 0))
            self.screen.blit(totalCarRender, (0, 30))
            pygame.display.update()


# def main():
#     Simulation().run()


# if __name__ == "__main__":
#     main()
