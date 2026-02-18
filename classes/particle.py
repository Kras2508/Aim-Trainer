"""
Particle class for background effects
"""

import pygame
import random
import sys
sys.path.append('..')
from config import BASE_WIDTH, BASE_HEIGHT


class Particle:
    """Small particle for background animation"""
    
    def __init__(self, x, y, vx, vy, size, color):
        self.x = x  # In base coordinates (800x600)
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = color
    
    def update(self):
        """Update particle position"""
        self.x += self.vx
        self.y += self.vy
        # Wrap around screen (base coordinates)
        if self.x < 0:
            self.x = BASE_WIDTH
        elif self.x > BASE_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = BASE_HEIGHT
        elif self.y > BASE_HEIGHT:
            self.y = 0
    
    def draw(self, screen, scale_x=1.0, scale_y=1.0):
        """Draw the particle with scaling"""
        scaled_x = int(self.x * scale_x)
        scaled_y = int(self.y * scale_y)
        scaled_size = max(1, int(self.size * (scale_x + scale_y) / 2))
        pygame.draw.circle(screen, self.color, (scaled_x, scaled_y), scaled_size)


def create_particles(count=50):
    """Create background particles"""
    particles = []
    for _ in range(count):
        x = random.randint(0, BASE_WIDTH)
        y = random.randint(0, BASE_HEIGHT)
        vx = random.uniform(-0.3, 0.3)
        vy = random.uniform(-0.3, 0.3)
        size = random.randint(1, 3)
        brightness = random.randint(50, 100)
        color = (brightness, brightness, brightness + 50)
        particles.append(Particle(x, y, vx, vy, size, color))
    return particles
