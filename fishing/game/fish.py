"""
Fish: swims horizontally at a fixed depth and wraps around the screen.
Task 2 introduces multiple fish types with different speeds, values,
sizes, and colors.
"""

import pygame


class Fish:
    def __init__(
        self,
        x,
        y,
        speed,
        width=36,
        height=18,
        point_value=10,
        color=(80, 180, 220),
    ):
        self.x = float(x)
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.point_value = point_value
        self.color = color

    def update(self, screen_width):
        self.x += self.speed

        if self.speed > 0 and self.x > screen_width:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = screen_width

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width,
            self.height,
        )


class SlowFish(Fish):
    """Slow fish: small, blue, and worth 10 points."""

    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            speed=1.5,
            width=32,
            height=16,
            point_value=10,
            color=(80, 180, 220),
        )


class FastFish(Fish):
    """Fast fish: larger, orange, and worth 25 points."""

    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            speed=-4,
            width=44,
            height=22,
            point_value=25,
            color=(255, 150, 60),
        )