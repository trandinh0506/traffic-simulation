import pygame
import math
import random
from constant import *
from road_segment import RoadSegment
from intersection import Intersection
from lane import Lane
from typing import Optional, List
from traffic_light import TrafficLight
from utils import *
class Car:
    def __init__(self, pos: list[int], direction: str = RIGHT):
        # Khởi tạo vị trí, vận tốc, hướng ban đầu
        self.pos = pos
        self.speed = [0.0, 0.0]
        self.maxSpeed = MAX_SPEED
        self.direction: str = direction
        self.mass: int = 1500
        self.wheelbase = 4.5
        self.steeringAngle: float = 0.0
        self.frictionForce: float = MEE * self.mass * GRAVITY
        self.tracionForce: float = 1.0
        self.acceleration: List[float] = [0.0, 0.0]
        self.currentAngle: float = DIRECTION2ANGLE[self.direction]
        self.action: str = GO_STRAIGHT
        self.turnTo: str = ""
        self.turningCoolDown = 60   # Frame chờ sau khi bắt đầu turning
        self.desired_angle: float = 0.0
        self.isActive = True
        self.activeCoolDown: int = 10

        self.detection_range = 20   # Khu vực phát hiện xung quanh xe

        # Tải hình xe và tạo mask (để dùng phát hiện va chạm)
        self.image = pygame.image.load("images/car.png").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rotated_image = self.image
        self.mask = pygame.mask.from_surface(self.image)

        # Các thuộc tính liên quan đến môi trường xung quanh
        self.nearby_intersection: Optional[Intersection] = None
        self.nearby_road: Optional[RoadSegment] = None
        self.nearby_cars: List["Car"] = []
        self.collision_imminent: bool = False
        self.collision_close: bool = False
        self.nearby_traffic_light: Optional[TrafficLight] = None

        self.current_lane: Optional[Lane] = None
        self.relativeDirection: str = ""
        self.turnningType: str = ""
    # -------------------- UPDATE & RENDER --------------------
    def update(self, delta_t: float, intersections: List[Intersection],
               roads: List[RoadSegment], cars: List["Car"], trafficLights: List[TrafficLight]) -> None:
        self.detect_surroundings(intersections, roads, cars, trafficLights)
        self.updateDecisionLogic()

        if self.action == TURNING:
            self.updateTurning(delta_t)

        self.updateAcceleration()
        self.updateVelocity(delta_t)
        self.updatePos(delta_t)
        self.turningCoolDown = max(0, self.turningCoolDown - 1)
        
        if not (self.nearby_intersection or  self.current_lane) and self.isActive:
            self.activeCoolDown -= 1
            self.isActive = self.activeCoolDown != 0
        else:
            self.activeCoolDown = 10
            
        for other in self.nearby_cars:
            if self.is_colliding_with(other):
                self.isActive = False
                other.isActive = False
                return
        if self.action == GO_STRAIGHT and self.current_lane and self.direction != self.current_lane.direction:
            self.isActive = False
    # -------------------- COLLISION & SURROUNDING DETECTION --------------------
    def get_rect(self, expand: int = 0) -> pygame.Rect:
        rect = self.rotated_image.get_rect(center=self.pos)
        return rect.inflate(expand, expand)

    def get_mask_rect(self) -> pygame.Rect:
        return self.rotated_image.get_rect(center=self.pos)

    def is_colliding_with(self, other: "Car") -> bool:
        offset_x = int(other.get_mask_rect().left - self.get_mask_rect().left)
        offset_y = int(other.get_mask_rect().top - self.get_mask_rect().top)
        return self.mask.overlap(other.mask, (offset_x, offset_y)) is not None

    def detect_surroundings(self, intersections: List[Intersection],
                            roads: List[RoadSegment], cars: List["Car"], trafficLights: List[TrafficLight]) -> None:
        self.nearby_intersection = None
        self.nearby_road = None
        self.nearby_cars = []
        self.nearby_traffic_light = None
        self.current_lane = None
        self.collision_imminent = False
        self.collision_close = False

        area_rect = self.get_rect()

        # Kiểm tra giao lộ gần
        for inter in intersections:
            if area_rect.colliderect(inter.get_rect()):
                self.nearby_intersection = inter
                break

        # Kiểm tra road và lane (nếu tâm xe nằm trong lane)
        for road in roads:
            if area_rect.colliderect(road.get_rect(expand=10)):
                self.nearby_road = road
                for lane in road.way.lanes_list:
                    if area_rect.colliderect(lane.rect) and lane.rect.collidepoint(self.get_rect().center):
                        self.current_lane = lane
                        break
                break

        # Kiểm tra các xe khác
        for other in cars:
            if other is not self:
                dx = other.pos[0] - self.pos[0]
                dy = other.pos[1] - self.pos[1]
                distance = math.hypot(dx, dy)
                if distance < 120:
                    self.nearby_cars.append(other)
        
        safeDistance = 15
        rectForTrafficLight = self.get_rect(safeDistance)          
        for trafficLight in trafficLights:
            if rectForTrafficLight.colliderect(trafficLight.stopLine) and self.direction == trafficLight.direction:
                self.nearby_traffic_light = trafficLight
                break
                
    # -------------------- DECISION LOGIC --------------------
    def updateDecisionLogic(self) -> None:
        if not self.isActive:
            return
        
        if self.nearby_intersection and self.current_lane and self.action == GO_STRAIGHT and self.turningCoolDown == 0:
            newDirection = None
            if self.current_lane.lane_number == 1:
                newDirection = random.choice([self.direction,
                                             DIRECTION_CHANGE_MAP[self.direction][LEFT],
                                             DIRECTION_CHANGE_MAP[self.direction][TURN_AROUND]])
            else:
                newDirection = random.choice([self.direction, DIRECTION_CHANGE_MAP[self.direction][RIGHT]])

            self.action = TURNING
            self.turnTo = newDirection
            if newDirection != self.direction:
                self.turnningType = CHANGE_DIRECTION
            else:
                self.turnningType = CHANGE_LANE
            self.turningCoolDown = 240  # Giới hạn tần suất chọn lane mới
        if self.action == TURNING and self.turnningType == CHANGE_DIRECTION and getRelativeTurnningDirection(self.direction, self.turnTo) == LEFT:
            self.maxSpeed = min(MAX_SPEED_TURNING, self.maxSpeed + 10)
        else:
            self.maxSpeed = min(MAX_SPEED, self.maxSpeed + 20)
        if self.getSpeedMagnitude() > self.maxSpeed:
            self.brake(0.4)
        elif self.getSpeedMagnitude() < self.maxSpeed:
            self.addForce(4000)
        if abs(self.getSpeedMagnitude() - self.maxSpeed) < 1:
            self.tracionForce = self.frictionForce

    # -------------------- TURNING LOGIC --------------------
    def computeDynamicSteeringAngle(self) -> float:
        if self.turnningType == CHANGE_DIRECTION:
            self.relativeDirection = getRelativeTurnningDirection(self.direction, self.turnTo)
            if self.relativeDirection == RIGHT:
                return -math.radians(6) 
            if self.relativeDirection == LEFT:
                return math.radians(1.6) 
            if self.relativeDirection == TURN_AROUND:
                return math.radians(10) 
        if self.turnningType == CHANGE_LANE:
            return 0.5 # TODO: update logic here
        
        return 0.1 # TODO: update logic here
        

    def updateTurning(self, delta_t: float) -> None:
        speedMagnitude = self.getSpeedMagnitude()
        if speedMagnitude < 12:
            return
        
        if self.relativeDirection == LEFT and self.has_car_on_left():
            self.brake(2)
            return
        dynamic_steer = self.computeDynamicSteeringAngle()
        self.steeringAngle = dynamic_steer

        turnRadius = self.wheelbase / math.tan(self.steeringAngle)
        yawRate = speedMagnitude / turnRadius

        target_angle = DIRECTION2ANGLE[self.turnTo]
        angle_diff = (target_angle - self.currentAngle)

        if abs(angle_diff) > 0.01:
            turnAngle = math.copysign(min(abs(yawRate * delta_t), abs(angle_diff)), -1 if self.relativeDirection == RIGHT else 1)
            self.currentAngle = normalizeAngle(self.currentAngle + turnAngle)
        else:
            self.currentAngle = target_angle
            self.direction = self.turnTo
            self.action = GO_STRAIGHT
    
    def has_car_on_left(self, look_ahead: int = 30, side_offset: int = 20) -> bool:
        """Kiểm tra nhanh có xe nào trong vùng nguy hiểm bên trái không"""
        check_area = self.get_relative_left_front_area(look_ahead, side_offset)
        return any(check_area.colliderect(car.get_mask_rect()) for car in self.nearby_cars)

    def get_relative_left_front_area(self, look_ahead: int = 30, side_offset: int = 20) -> pygame.Rect:
        """Tạo Rect kiểm tra vùng trước-bên trái tương đối"""
        DETECTION_WIDTH = DETECTION_HEIGHT = 40
        if self.direction == RIGHT:
            left_vec = (0, -side_offset)  # Lên trên
            front_vec = (look_ahead, 0)
        elif self.direction == LEFT:
            left_vec = (0, side_offset)   # Xuống dưới
            front_vec = (-look_ahead, 0)
        elif self.direction == UP:
            left_vec = (-side_offset, 0)  # Sang trái
            front_vec = (0, -look_ahead)
        else:  # DOWN
            left_vec = (side_offset, 0)   # Sang phải
            front_vec = (0, look_ahead)
        
        check_center = (
            self.pos[0] + front_vec[0] + left_vec[0],
            self.pos[1] + front_vec[1] + left_vec[1]
        )
        return pygame.Rect(0, 0, DETECTION_WIDTH, DETECTION_HEIGHT).move(
            check_center[0] - DETECTION_WIDTH // 2, check_center[1] - DETECTION_HEIGHT // 2)

    # -------------------- PHYSICS UPDATE --------------------
    def updateAcceleration(self) -> None:
        if self.tracionForce > self.frictionForce:
            forceNet = self.tracionForce - self.frictionForce
            accelMag = forceNet / self.mass
            self.acceleration[0] = accelMag * math.cos(self.currentAngle)
            self.acceleration[1] = accelMag * -math.sin(self.currentAngle)
        else:
            accelMag = -self.frictionForce / self.mass
            self.acceleration[0] = accelMag * math.cos(self.currentAngle)
            self.acceleration[1] = accelMag * -math.sin(self.currentAngle)

    def updateVelocity(self, delta_t: float) -> None:
        self.speed[0] += self.acceleration[0] * delta_t
        self.speed[1] += self.acceleration[1] * delta_t
        speedMagnitude = self.getSpeedMagnitude()
        speedMagnitude = min(speedMagnitude, self.maxSpeed)
        self.speed[0] = speedMagnitude * math.cos(self.currentAngle)
        self.speed[1] = speedMagnitude * -math.sin(self.currentAngle)

    def updatePos(self, delta_t: float) -> None:
        if not self.isActive:
            return
        
        lastPos = [self.pos[0], self.pos[1]]
        if self.relativeDirection == TURN_AROUND:
            collisionControll = 15
        elif self.relativeDirection == LEFT:
            collisionControll = 10
        else:
            collisionControll = 3
            
        self.pos[0] += self.speed[0] * delta_t * collisionControll
        self.pos[1] += self.speed[1] * delta_t * collisionControll
        
        if self.nearby_traffic_light and self.nearby_traffic_light.currentLight != GREEN:
            self.pos = lastPos
            self.brake(3)
            return
        
        if self.relativeDirection == LEFT and self.has_car_on_left():
            self.brake(2)
        
        for other in self.nearby_cars:
            if self.is_colliding_with(other):
                self.pos = lastPos
                self.brake(1.5)
                return
            
        self.pos[0] -= self.speed[0] * delta_t * (collisionControll - 1)
        self.pos[1] -= self.speed[1] * delta_t * (collisionControll - 1)
        
    def addForce(self, force: float) -> None:
        self.tracionForce += force

    def brake(self, intensity: float) -> None:
        speed_mag = self.getSpeedMagnitude()
        if speed_mag < 0.1:
            return
        self.tracionForce = 0
        brake_force = intensity * self.frictionForce
        brake_accel = brake_force / self.mass
        self.acceleration[0] = -brake_accel * (self.speed[0] / speed_mag)
        self.acceleration[1] = -brake_accel * (self.speed[1] / speed_mag)


    def getSpeedMagnitude(self) -> float:
        return math.sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)

    def hasEnterLane(self, lane: Lane) -> bool:
        return self.get_rect().collidepoint(lane.get_entry_target_point())

    # def turn(self, newDirection: str) -> bool:
    #     if self.action == TURNING or newDirection not in DIRECTIONS or newDirection == self.direction:
    #         return False
    #     if abs(self.speed[0]) < 0.1 and abs(self.speed[1]) < 0.1:
    #         return False

    #     self.turnTo = newDirection
    #     self.action = TURNING

    #     if self.target_lane and self.target_lane.direction == newDirection:
    #         self.turn_target_pos = self.target_lane.get_entry_target_point()
    #     else:
    #         self.turn_target_pos = None
    #         self.steeringAngle = math.radians(3) if newDirection in [LEFT, UP] else -math.radians(3)

    #     print(f"[DEBUG] turn to {newDirection}, initial steer: {math.degrees(self.steeringAngle):.2f}°, target: {self.turn_target_pos}")
    #     return True

    def reset(self, pos: list[int], direction: str):
        self.pos = [pos[0], pos[1]]
        self.direction = direction
        self.activeCoolDown = 10
        self.isActive = True
        
    def render(self, display: pygame.Surface, offset: tuple[int, int]) -> None:
        self.rotated_image = pygame.transform.rotate(self.image, math.degrees(self.currentAngle))
        self.mask = pygame.mask.from_surface(self.rotated_image)
        rect = self.rotated_image.get_rect(center=self.pos)
        display.blit(self.rotated_image, (rect.left - offset[0], rect.top - offset[1]))

    def debug_render(self, display: pygame.Surface, offset: tuple[int, int]) -> None:
        if self.current_lane:
            pygame.draw.rect(display, (0, 255, 0), self.current_lane.rect.move(-offset[0], -offset[1]), 2)
        pygame.draw.circle(display, (0, 0, 255), (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1])), 5)
        
        font = pygame.font.SysFont("times", 15)
        
        display.blit(font.render(self.action, True, (0, 255, 0)), (10, 100))
        