"""
Catch detection between the fishing hook and fish.

The collision check uses the hook's current rectangle and a swept
rectangle covering the hook's recent vertical movement. This prevents
the hook from passing through a fish between two frames without
registering the catch.
"""

import pygame


def check_catch(hook, fish_list):
    """
    Returns the fish the hook has caught, or None.

    A catch occurs when the hook overlaps a fish. The swept rectangle
    also checks the space travelled by the hook during the current
    frame so fast vertical movement cannot skip over a fish.
    """

    hook_rect = hook.get_rect()

    # The hook moves vertically by hook.speed pixels per frame.
    # Include the previous/current hook positions in one collision area.
    if hook.state == "casting":
        sweep_top = min(hook.y, hook.y - hook.speed)
        sweep_bottom = max(hook.y, hook.y - hook.speed)
    elif hook.state == "retracting":
        sweep_top = min(hook.y, hook.y + hook.speed)
        sweep_bottom = max(hook.y, hook.y + hook.speed)
    else:
        sweep_top = hook.y
        sweep_bottom = hook.y

    sweep_rect = pygame.Rect(
        int(hook.x - hook.width / 2),
        int(sweep_top - hook.height / 2),
        hook.width,
        int(sweep_bottom - sweep_top + hook.height),
    )

    for fish in fish_list:
        fish_rect = fish.get_rect()

        if hook_rect.colliderect(fish_rect):
            return fish

        if sweep_rect.colliderect(fish_rect):
            return fish

    return None