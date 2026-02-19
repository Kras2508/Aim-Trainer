"""
Mode Selection Screen - Choose between Classic and Tracking modes
"""

import pygame
from config import *
from classes import Button


class ModeSelectScreen:
    """Game mode selection screen"""
    
    def __init__(self):
        cx = BASE_WIDTH // 2
        cy = BASE_HEIGHT // 2
        
        self.classic_button = Button(cx - 140, cy - 80, 280, 70, "CLASSIC", (50, 100, 150), (80, 150, 200))
        self.tracking_button = Button(cx - 140, cy + 40, 280, 70, "TRACKING", (150, 80, 50), (200, 120, 80))
        self.back_button = Button(50, BASE_HEIGHT - 70, 120, 50, "BACK", (100, 100, 100), (150, 150, 150))
    
    def handle_events(self, event, mouse_pos):
        """Handle mode selection events. Returns (new_state, mode) or None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.classic_button.is_clicked(mouse_pos):
                return (STATE_DIFFICULTY, MODE_CLASSIC)
            elif self.tracking_button.is_clicked(mouse_pos):
                return (STATE_COUNTDOWN, MODE_TRACKING)
            elif self.back_button.is_clicked(mouse_pos):
                return (STATE_MENU, None)
        return None
    
    def update(self, mouse_pos):
        """Update button hover states"""
        self.classic_button.update(mouse_pos)
        self.tracking_button.update(mouse_pos)
        self.back_button.update(mouse_pos)
        pygame.mouse.set_visible(True)
    
    def draw(self, screen, fonts, scale_x=1.0, scale_y=1.0):
        """Draw the mode selection screen with scaling"""
        font_title, font_large, font, font_small = fonts
        
        center_x = int(BASE_WIDTH // 2 * scale_x)
        
        title = font_large.render("SELECT MODE", True, UI_COLOR)
        screen.blit(title, title.get_rect(center=(center_x, int(55 * scale_y))))
        
        # Mode descriptions
        self.classic_button.draw(screen, font, scale_x, scale_y)
        classic_desc = font_small.render("Click targets before they vanish", True, (150, 180, 220))
        screen.blit(classic_desc, classic_desc.get_rect(center=(center_x, int(310 * scale_y))))
        
        self.tracking_button.draw(screen, font, scale_x, scale_y)
        tracking_desc = font_small.render("Keep crosshair on a moving target", True, (220, 170, 140))
        screen.blit(tracking_desc, tracking_desc.get_rect(center=(center_x, int(425 * scale_y))))
        
        self.back_button.draw(screen, font_small, scale_x, scale_y)
