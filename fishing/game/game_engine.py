"""
GameEngine: owns the hook, fish, score, and round timer.

Task 4 adds a 30-second round timer and round reset.
"""

import pygame

from game.hook import Hook, IDLE
from game.fish import SlowFish, FastFish
from game.catch import check_catch
from game.renderer import WIDTH, SURFACE_Y, MAX_DEPTH_Y


ROUND_DURATION = 30


class GameEngine:
    def __init__(self):
        self.hook = Hook(
            x=WIDTH / 2,
            surface_y=SURFACE_Y,
            max_depth_y=MAX_DEPTH_Y,
            speed=5,
        )

        self.fish_list = [
            SlowFish(x=100, y=180),
            FastFish(x=400, y=280),
            SlowFish(x=250, y=380),
        ]

        self.hooked_fish = None
        self.score = 0

        self.round_time = ROUND_DURATION
        self.round_over = False
        self.last_time = pygame.time.get_ticks()

    def start_cast(self):
        if not self.round_over and self.hook.state == IDLE:
            self.hook.start_cast()

    def reset_round(self):
        self.hook = Hook(
            x=WIDTH / 2,
            surface_y=SURFACE_Y,
            max_depth_y=MAX_DEPTH_Y,
            speed=5,
        )

        self.fish_list = [
            SlowFish(x=100, y=180),
            FastFish(x=400, y=280),
            SlowFish(x=250, y=380),
        ]

        self.hooked_fish = None
        self.score = 0
        self.round_time = ROUND_DURATION
        self.round_over = False
        self.last_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_time) / 1000.0
        self.last_time = current_time

        if not self.round_over:
            self.round_time -= elapsed

            if self.round_time <= 0:
                self.round_time = 0
                self.round_over = True

                # Stop the hook at the surface.
                self.hook.y = self.hook.surface_y
                self.hook.state = IDLE
                self.hooked_fish = None

                return

        if self.round_over:
            return

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y

            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                self.hooked_fish = None

        else:
            caught = check_catch(
                self.hook,
                self.fish_list
            )

            if caught is not None:
                self.fish_list.remove(caught)

                self.hooked_fish = caught

                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y

                self.hook.catch_fish()

    def draw(self, surface, font):
        from game import renderer

        draw_list = list(self.fish_list)

        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)

        renderer.draw_scene(
            surface,
            self.hook,
            draw_list
        )

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10)
        )

        renderer.draw_text(
            surface,
            font,
            f"Time: {max(0, int(self.round_time + 0.999))}",
            (10, 40)
        )

        if self.round_over:
            renderer.draw_banner(
                surface,
                font,
                f"ROUND OVER  -  Final Score: {self.score}  -  Press R to restart"
            )