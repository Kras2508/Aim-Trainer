"""
Game helper utilities for Aim Trainer
Contains spawn logic and other game-related helper functions
"""

import random
import math
import sys
sys.path.append('..')
from config import *


def random_spawn_position(existing_targets, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
    """Generate random spawn position with margins, avoiding overlap"""
    max_attempts = 50
    for _ in range(max_attempts):
        x = random.randint(MARGIN, screen_width - MARGIN)
        y = random.randint(MARGIN, screen_height - MARGIN)
        # Check if position overlaps with existing targets
        valid = True
        for target in existing_targets:
            if target.alive:
                dist = math.hypot(x - target.x, y - target.y)
                if dist < (target.radius + 80):  # Minimum spacing
                    valid = False
                    break
        if valid:
            return (x, y)
    # If no valid position found, return random anyway
    return (random.randint(MARGIN, screen_width - MARGIN), 
            random.randint(MARGIN, screen_height - MARGIN))


def random_target_size():
    """Random target size like Aimlab difficulty"""
    return random.choice([TARGET_SIZE_SMALL, TARGET_SIZE_MEDIUM, TARGET_SIZE_LARGE])
