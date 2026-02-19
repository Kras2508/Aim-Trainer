"""
Menu Screen - Main menu with Start, Instructions, Settings, Quit buttons
"""

import pygame
from config import *
from classes import Button


class MenuScreen:
    """Main menu screen"""
    
    def __init__(self):
        # Use BASE_WIDTH/HEIGHT for positioning (will be scaled when drawing)
        cx = BASE_WIDTH // 2
        top = 230  # below title + subtitle
        gap = 75   # spacing between buttons
        self.start_button = Button(cx - 120, top, 240, 55, "START GAME", (50, 100, 150), (80, 150, 200))
        self.instruction_button = Button(cx - 120, top + gap, 240, 55, "INSTRUCTIONS", (100, 100, 50), (150, 150, 80))
        self.settings_button = Button(cx - 120, top + gap * 2, 240, 55, "SETTINGS", (100, 50, 150), (150, 80, 200))
        self.quit_button = Button(cx - 120, top + gap * 3, 240, 55, "QUIT", (150, 50, 50), (200, 80, 80))
    
    def handle_events(self, event, mouse_pos):
        """Handle menu events. Returns new game state or None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_button.is_clicked(mouse_pos):
                return STATE_MODE_SELECT
            elif self.instruction_button.is_clicked(mouse_pos):
                return STATE_INSTRUCTION
            elif self.settings_button.is_clicked(mouse_pos):
                return STATE_SETTINGS
            elif self.quit_button.is_clicked(mouse_pos):
                return 'QUIT'
        return None
    
    def update(self, mouse_pos):
        """Update button hover states"""
        self.start_button.update(mouse_pos)
        self.instruction_button.update(mouse_pos)
        self.settings_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)
        pygame.mouse.set_visible(True)
    
    def draw(self, screen, fonts, scale_x=1.0, scale_y=1.0):
        """Draw the menu screen with scaling"""
        font_title, font_large, font, font_small = fonts
        
        # Scale positions for text
        center_x = int(BASE_WIDTH // 2 * scale_x)
        title_y = int(120 * scale_y)
        subtitle_y = int(190 * scale_y)
        
        title = font_title.render("AIM TRAINER", True, TARGET_PRIMARY)
        subtitle = font.render("Train Your Reflexes", True, ACCENT_COLOR)
        screen.blit(title, title.get_rect(center=(center_x, title_y)))
        screen.blit(subtitle, subtitle.get_rect(center=(center_x, subtitle_y)))
        
        self.start_button.draw(screen, font, scale_x, scale_y)
        self.instruction_button.draw(screen, font, scale_x, scale_y)
        self.settings_button.draw(screen, font, scale_x, scale_y)
        self.quit_button.draw(screen, font, scale_x, scale_y)
