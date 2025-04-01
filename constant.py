import math

GRAVITY = 9.80665
MEE = 0.7 #μ
PI = math.pi
DIRECTION2ANGLE: dict[str, float] = {
    "up": -PI / 2,
    "left": PI,
    "down": 3 * PI / 4,
    "right": 0
}
DIRECTIONS: tuple[str] = ("left", "right", "up", "down")
RUNNING = "running"
TURNING = "tuning"

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
