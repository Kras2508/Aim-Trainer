"""
Button class for Aim Trainer UI
"""

import pygame
import sys
sys.path.append('..')
from config import WHITE


class Button:
    """Interactive button for UI"""
    
    def __init__(self, x, y, width, height, text, color, hover_color):
        # Store position in base coordinates (800x600)
        self.base_rect = pygame.Rect(x, y, width, height)
        self.rect = pygame.Rect(x, y, width, height)  # For collision detection (in base coords)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def draw(self, screen, font, scale_x=1.0, scale_y=1.0):
        """Draw the button with scaling"""
        color = self.hover_color if self.is_hovered else self.color
        
        # Scale rect for drawing
        scaled_rect = pygame.Rect(
            int(self.base_rect.x * scale_x),
            int(self.base_rect.y * scale_y),
            int(self.base_rect.width * scale_x),
            int(self.base_rect.height * scale_y)
        )
        
        border_width = max(2, int(3 * (scale_x + scale_y) / 2))
        pygame.draw.rect(screen, color, scaled_rect)
        pygame.draw.rect(screen, WHITE, scaled_rect, border_width)
        
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        screen.blit(text_surface, text_rect)
    
    def update(self, mouse_pos):
        """Update hover state (mouse_pos in base coords)"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos):
        """Check if button was clicked (mouse_pos in base coords)"""
        return self.rect.collidepoint(mouse_pos)
