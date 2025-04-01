import pygame
import math
from constant import *
class Car:
    def __init__(self, pos: list[int], speed: list[float], direction: str = "right"):
        self.pos = pos
        self.speed = speed
        self.speed = [0, 0]
        self.direction: str = direction
        self.mass: int = 1500
        self.frictionForce: float = MEE * self.mass * GRAVITY
        print(self.frictionForce)
        self.tracionForce: float = 35000
        self.acceleration: list[float] = [0, 0]
        self.currentAngle: float = DIRECTION2ANGLE[self.direction]
        self.action: str = RUNNING
        self.turnTo: str = ""
        self.frame: int = 0
        
        # 
        
        self.image = pygame.image.load("images/car.png").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
    def update(self, delta_t: float):
        if self.action == TURNING and self.frame % 10 == 0:
            pass
            # self.currentAngle += () # todo
        
        if self.tracionForce >= self.frictionForce:
            self.acceleration = [(self.tracionForce - self.frictionForce) / self.mass] * 2
        self.acceleration[0] = self.acceleration[0] * math.cos(self.currentAngle)
        self.acceleration[1] = self.acceleration[1] * math.sin(self.currentAngle)
        # print(self.acceleration)
        self.speed[0] += self.acceleration[0] * delta_t
        self.speed[1] += self.acceleration[1] * delta_t
        # print("speed:", self.speed)

        self.pos[0] += self.speed[0] * delta_t
        self.pos[1] += self.speed[1] * delta_t
        self.frame += 1
        
    def addForce(self, force: float):
        self.tracionForce += force
    
    def brake(self, intensity: float):
        self.tracionForce = 0 # cancel traction force when braking
        brake_force = intensity * self.frictionForce * 2
        net_force = self.tracionForce - brake_force
        self.acceleration = [net_force / self.mass] * 2    
        
    def turn(self, direction: str) -> bool:
        if self.action == TURNING:
            return False
        if direction not in DIRECTIONS:
            return False
        
        self.action = TURNING
        self.turnTo = direction
        
        return True
    def render(self, display: pygame.Surface, offset: tuple[int, int]):
        if self.direction == "up":
            rotated_image = pygame.transform.rotate(self.image, 90)
        elif self.direction == "down":
            rotated_image = pygame.transform.rotate(self.image, -90)
        elif self.direction == "left":
            rotated_image = pygame.transform.rotate(self.image, 180)
        else:
            rotated_image = self.image
            
        rect = rotated_image.get_rect(center=self.pos)
        display.blit(rotated_image, (rect.left - offset[0], rect.top - offset[1]))