"""
Target class for Aim Trainer
"""

import pygame
import random
import math
import sys
sys.path.append('..')
from config import *


class Target:
    """Target that players need to click"""
    
    def __init__(self, position, size):
        self.x, self.y = position
        self.radius = size
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = random.randint(
            TARGET_MIN_LIFETIME, TARGET_MAX_LIFETIME
        )
        self.alive = True
        self.hit = False
        self.hit_time = None
        self.reaction_time = None  # Track reaction time

    def is_expired(self, current_time):
        """Check if target has expired"""
        return (current_time - self.spawn_time) >= self.lifetime

    def check_hit(self, mouse_pos):
        """Check if mouse click hit the target"""
        if self.hit:
            return False

        mx, my = mouse_pos
        distance = math.hypot(mx - self.x, my - self.y)
        if distance <= self.radius:
            self.hit = True
            self.hit_time = pygame.time.get_ticks()
            self.reaction_time = self.hit_time - self.spawn_time  # Calculate reaction time
            self.alive = False
            return True
        return False

    def draw(self, screen, scale_x=1.0, scale_y=1.0):
        """Draw the target (modern circular design) with scaling"""
        current_time = pygame.time.get_ticks()
        time_alive = current_time - self.spawn_time
        progress = min(1.0, time_alive / self.lifetime)
        
        # Scale position and size
        sx = int(self.x * scale_x)
        sy = int(self.y * scale_y)
        scale_avg = (scale_x + scale_y) / 2
        scaled_radius = int(self.radius * scale_avg)
        
        # Outer glow (pulsing effect)
        glow_radius = scaled_radius + int(5 * scale_avg) + int(3 * scale_avg * math.sin(time_alive * 0.01))
        for i in range(3):
            pygame.draw.circle(screen, TARGET_PRIMARY, (sx, sy), glow_radius - i * 2, 1)
        
        # Main target circle (filled)
        pygame.draw.circle(screen, TARGET_PRIMARY, (sx, sy), scaled_radius)
        
        # Inner ring
        pygame.draw.circle(screen, TARGET_SECONDARY, (sx, sy), int(scaled_radius * 0.7))
        
        # Inner circle
        pygame.draw.circle(screen, WHITE, (sx, sy), int(scaled_radius * 0.4))
        
        # Center dot
        pygame.draw.circle(screen, TARGET_PRIMARY, (sx, sy), int(scaled_radius * 0.15))
        
        # Warning ring when about to expire (last 30% of lifetime)
        if progress > 0.7:
            warning_thickness = max(2, int(3 * scale_avg))
            pygame.draw.circle(screen, ACCENT_COLOR, (sx, sy), scaled_radius + int(8 * scale_avg), warning_thickness)
