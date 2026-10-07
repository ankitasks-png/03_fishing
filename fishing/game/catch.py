def check_catch(hook, fish_list):
    """
    Returns the fish the hook has caught, or None.

    A catch occurs only when the hook's rectangle overlaps
    the fish's rectangle.
    """
    hook_rect = hook.get_rect()

    for fish in fish_list:
        if hook_rect.colliderect(fish.get_rect()):
            return fish

    return None