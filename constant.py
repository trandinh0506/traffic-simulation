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
TURN_AROUND = "turn around"

DIRECTIONS: tuple[str] = (LEFT, RIGHT, DOWN, UP)

RUNNING = "running"
TURNING = "tuning"
GO_STRAIGHT = "go straight"
CHANGE_DIRECTION = "change direction"
CHANGE_LANE = "change lane"
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

MAX_STEERING_ANGLE = math.radians(30)

MAX_SPEED = 200.0
MAX_SPEED_TURNING = MAX_SPEED * 0.75

RED = "red"
YELLOW = "yellow"
GREEN = "green"

TEXT2COLOR = {
    RED: (255, 0, 0),
    YELLOW: (255, 255, 0),
    GREEN: (0, 255, 0)
}

EPSILON = 0.1

STOPLINE_HEIGHT = 20