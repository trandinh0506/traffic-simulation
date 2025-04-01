import math

GRAVITY = 9.80665
MEE = 0.7 #μ
PI = math.pi

DIRECTION2ANGLE: dict[str, float] = {
    "up": PI / 2,
    "left": PI,
    "down": 3 * PI / 2,
    "right": 0
}

LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"

DIRECTIONS: tuple[str] = (LEFT, RIGHT, DOWN, UP)
RUNNING = "running"
TURNING = "tuning"

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

MAX_STEERING_ANGLE = math.radians(30)
