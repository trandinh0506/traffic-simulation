import pygame

SCALE_RATIO = 0.3

class Car:
    def __init__(self, pos: list[int], speed: list[float], direction: str = "right"):
        self.pos = pos
        self.speed = speed
        self.acceleration = [0, 0]
        self.direction = direction
        original_image = pygame.image.load("images/car.png").convert_alpha()
        width, height = original_image.get_size()
        new_size = (int(width * SCALE_RATIO), int(height * SCALE_RATIO))
        self.image = pygame.transform.scale(original_image, new_size)
        self.image.set_colorkey((255, 255, 255))
    def update(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
    def render(self, display: pygame.Surface):
        if self.direction == "up":
            rotated_image = pygame.transform.rotate(self.image, 90)
        elif self.direction == "down":
            rotated_image = pygame.transform.rotate(self.image, -90)
        elif self.direction == "left":
            rotated_image = pygame.transform.rotate(self.image, 180)
        else:
            rotated_image = self.image
            
        rect = rotated_image.get_rect(center=self.pos)
        display.blit(rotated_image, rect.topleft)