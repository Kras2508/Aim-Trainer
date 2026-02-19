"""
Difficulty Selection Screen
"""

import pygame
from config import *
from classes import Button


class DifficultyScreen:
    """Difficulty selection screen"""
    
    def __init__(self):
        cx = BASE_WIDTH // 2
        cy = BASE_HEIGHT // 2
        self.easy_button = Button(cx - 120, cy - 80, 240, 60, "EASY", (50, 150, 50), (80, 200, 80))
        self.medium_button = Button(cx - 120, cy + 10, 240, 60, "MEDIUM", (200, 150, 50), (255, 200, 80))
        self.hard_button = Button(cx - 120, cy + 100, 240, 60, "HARD", (200, 50, 50), (255, 80, 80))
        self.back_button = Button(50, BASE_HEIGHT - 70, 120, 50, "BACK", (100, 100, 100), (150, 150, 150))
    
    def handle_events(self, event, mouse_pos):
        """Handle difficulty events. Returns (new_state, difficulty) or None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.easy_button.is_clicked(mouse_pos):
                return (STATE_COUNTDOWN, 'EASY')
            elif self.medium_button.is_clicked(mouse_pos):
                return (STATE_COUNTDOWN, 'MEDIUM')
            elif self.hard_button.is_clicked(mouse_pos):
                return (STATE_COUNTDOWN, 'HARD')
            elif self.back_button.is_clicked(mouse_pos):
                return (STATE_MODE_SELECT, None)
        return None
    
    def update(self, mouse_pos):
        """Update button hover states"""
        self.easy_button.update(mouse_pos)
        self.medium_button.update(mouse_pos)
        self.hard_button.update(mouse_pos)
        self.back_button.update(mouse_pos)
        pygame.mouse.set_visible(True)
    
    def draw(self, screen, fonts, scale_x=1.0, scale_y=1.0):
        """Draw the difficulty selection screen with scaling"""
        font_title, font_large, font, font_small = fonts
        
        center_x = int(BASE_WIDTH // 2 * scale_x)
        title = font_large.render("SELECT DIFFICULTY", True, UI_COLOR)
        screen.blit(title, title.get_rect(center=(center_x, int(120 * scale_y))))
        
        self.easy_button.draw(screen, font, scale_x, scale_y)
        self.medium_button.draw(screen, font, scale_x, scale_y)
        self.hard_button.draw(screen, font, scale_x, scale_y)
        self.back_button.draw(screen, font_small, scale_x, scale_y)
