import math

GRAVITY = 9.80665
MEE = 0.7 #μ
PI = math.pi


LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"
TURN_AROUND = "turn around"

DIRECTIONS: tuple[str] = (LEFT, RIGHT, DOWN, UP)


DIRECTION2ANGLE: dict[str, float] = {
    UP: PI / 2,
    LEFT: PI,
    DOWN: 3 * PI / 2,
    RIGHT: 0
}

DIRECTION_CHANGE_MAP: dict[str, dict[str, str]] = {
        UP: {
            LEFT: LEFT,
            RIGHT: RIGHT,
            TURN_AROUND: DOWN
        },
        DOWN: {
            LEFT: RIGHT,
            RIGHT: LEFT,
            TURN_AROUND: UP
        },
        LEFT: {
            LEFT: DOWN,
            RIGHT: UP,
            TURN_AROUND: RIGHT
        },
        RIGHT: {
            LEFT: UP,
            RIGHT: DOWN,
            TURN_AROUND: LEFT
        }
    }


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

YELLOW_DURATION = 3

EPSILON = 0.18

STOPLINE_HEIGHT = 20

SPAWN_COOLDOWN_TIME = 5.0

SPWAN_POINTS = []

for offset in range(5):
    SPWAN_POINTS.append({"pos": [2000 + offset * 100, 370], "dir": LEFT, "cooldown": 0})
    SPWAN_POINTS.append({"pos": [2000 + offset * 100, 310], "dir": LEFT, "cooldown": 0})

    SPWAN_POINTS.append({"pos": [-900 + offset * 100, 430], "dir": RIGHT, "cooldown": 0})
    SPWAN_POINTS.append({"pos": [-900 + offset * 100, 490], "dir": RIGHT, "cooldown": 0})

    SPWAN_POINTS.append({"pos": [490, 2000 + offset * 100], "dir": UP, "cooldown": 0})
    SPWAN_POINTS.append({"pos": [430, 2000 + offset * 100], "dir": UP, "cooldown": 0})

    SPWAN_POINTS.append({"pos": [370, -600 + offset * 100], "dir": DOWN, "cooldown": 0})
    SPWAN_POINTS.append({"pos": [315, -600 + offset * 100], "dir": DOWN, "cooldown": 0})
