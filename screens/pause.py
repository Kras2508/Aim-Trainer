"""
Pause Screen - Pause overlay with Continue, Settings, Quit
"""

import pygame
from config import *
from classes import Button


class PauseScreen:
    """Pause menu overlay"""
    
    def __init__(self):
        cx = BASE_WIDTH // 2
        cy = BASE_HEIGHT // 2
        self.continue_button = Button(cx - 120, cy - 80, 240, 60, "CONTINUE", (50, 150, 50), (80, 200, 80))
        self.settings_button = Button(cx - 120, cy + 10, 240, 60, "SETTINGS", (100, 50, 150), (150, 80, 200))
        self.quit_button = Button(cx - 120, cy + 100, 240, 60, "QUIT TO MENU", (150, 50, 50), (200, 80, 80))
    
    def handle_events(self, event, mouse_pos):
        """Handle pause events. Returns new state or None."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.mouse.set_visible(False)
            return STATE_PLAYING
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.continue_button.is_clicked(mouse_pos):
                pygame.mouse.set_visible(False)
                return STATE_PLAYING
            elif self.settings_button.is_clicked(mouse_pos):
                return STATE_SETTINGS
            elif self.quit_button.is_clicked(mouse_pos):
                pygame.mouse.set_visible(True)
                return STATE_MENU
        return None
    
    def update(self, mouse_pos):
        """Update button hover states"""
        self.continue_button.update(mouse_pos)
        self.settings_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)
        pygame.mouse.set_visible(True)
    
    def draw(self, screen, fonts, scale_x=1.0, scale_y=1.0):
        """Draw the pause overlay with scaling"""
        font_title, font_large, font, font_small = fonts
        
        actual_width = int(BASE_WIDTH * scale_x)
        actual_height = int(BASE_HEIGHT * scale_y)
        center_x = int(BASE_WIDTH // 2 * scale_x)
        
        # Dim overlay
        overlay = pygame.Surface((actual_width, actual_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        title = font_title.render("PAUSED", True, UI_COLOR)
        screen.blit(title, title.get_rect(center=(center_x, int(120 * scale_y))))
        
        self.continue_button.draw(screen, font, scale_x, scale_y)
        self.settings_button.draw(screen, font, scale_x, scale_y)
        self.quit_button.draw(screen, font, scale_x, scale_y)
        
        hint_text = font_small.render("Press ESC to continue", True, (150, 150, 150))
        screen.blit(hint_text, hint_text.get_rect(center=(center_x, actual_height - int(50 * scale_y))))
