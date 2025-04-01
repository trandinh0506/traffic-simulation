import pygame
import math
from constant import *
class Car:
    def __init__(self, pos: list[int], direction: str = "right"):
        self.pos = pos
        self.speed = [0, 0]
        self.speed = [0, 0]
        self.direction: str = direction
        self.mass: int = 1500
        self.wheelbase = 2.5
        self.steeringAngle: float = 0
        self.frictionForce: float = MEE * self.mass * GRAVITY
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
        if self.frame % 10 == 0:
            # Nếu xe đang quay và có vận tốc, cập nhật góc quay
            if self.action == TURNING and (abs(self.speed[0]) > 0.1 or abs(self.speed[1]) > 0.1):
                turnRadius = self.wheelbase / math.tan(self.steeringAngle)
                speedMagnitude = math.sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)
                yawRate = speedMagnitude / turnRadius

                target_angle = DIRECTION2ANGLE[self.turnTo]  # Góc đích

                if abs(self.currentAngle - target_angle) > 0.01:
                    turnAngle = math.copysign(
                        min(abs(yawRate * delta_t), abs(self.currentAngle - target_angle)),
                        target_angle - self.currentAngle)
                    
                    self.currentAngle += turnAngle

                else:
                    self.currentAngle = target_angle
                    self.direction = self.turnTo
                    self.action = RUNNING

                # Cập nhật vận tốc dựa trên góc mới (giữ nguyên độ lớn)
                self.speed[0] = speedMagnitude * math.cos(self.currentAngle)
                self.speed[1] = speedMagnitude * -math.sin(self.currentAngle)

        # Tính toán lực và gia tốc
        if self.tracionForce > self.frictionForce:
            forceNet = self.tracionForce - self.frictionForce
            accelerationMagnitude = forceNet / self.mass
            self.acceleration[0] = accelerationMagnitude * math.cos(self.currentAngle)
            self.acceleration[1] = accelerationMagnitude * -math.sin(self.currentAngle)

        # Cập nhật tốc độ từ gia tốc
        self.speed[0] += self.acceleration[0] * delta_t
        self.speed[1] += self.acceleration[1] * delta_t

        # Giữ nguyên tốc độ tổng sau khi cập nhật góc quay
        speedMagnitude = math.sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)
        self.speed[0] = speedMagnitude * math.cos(self.currentAngle)
        self.speed[1] = speedMagnitude * -math.sin(self.currentAngle)

        # Cập nhật vị trí
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
        
    def turn(self, newDirection: str) -> bool:
        if abs(self.speed[0]) < 0.1 and abs(self.speed[1]) < 0.1:
            return False
        
        if self.action == TURNING:
            return False
        if newDirection not in DIRECTIONS:
            return False
        if newDirection == self.direction:
            return False
        
        if self.direction > newDirection:
            self.steeringAngle = -math.radians(4)
        else:
            self.steeringAngle = math.radians(4)
        
        self.action = TURNING
        self.turnTo = newDirection
        
        return True
    def render(self, display: pygame.Surface, offset: tuple[int, int]):
        rotated_image = pygame.transform.rotate(self.image, math.degrees(self.currentAngle))
        rect = rotated_image.get_rect(center=self.pos)
        display.blit(rotated_image, (rect.left - offset[0], rect.top - offset[1]))