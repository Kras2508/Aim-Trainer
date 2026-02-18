"""
Instruction Screen - How to play guide
"""

import pygame
from config import *
from classes import Button


class InstructionScreen:
    """Instructions / How to play screen"""
    
    def __init__(self):
        self.back_button = Button(50, BASE_HEIGHT - 70, 120, 50, "BACK", (100, 100, 100), (150, 150, 150))
    
    def handle_events(self, event, mouse_pos):
        """Handle instruction screen events. Returns new state or None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.is_clicked(mouse_pos):
                return STATE_MENU
        return None
    
    def update(self, mouse_pos):
        """Update button hover states"""
        self.back_button.update(mouse_pos)
        pygame.mouse.set_visible(True)
    
    def draw(self, screen, fonts, game_duration_sec, scale_x=1.0, scale_y=1.0):
        """Draw the instruction screen with scaling"""
        font_title, font_large, font, font_small = fonts
        
        center_x = int(BASE_WIDTH // 2 * scale_x)
        title = font_large.render("HOW TO PLAY", True, UI_COLOR)
        screen.blit(title, title.get_rect(center=(center_x, int(60 * scale_y))))
        
        instructions = [
            "Click on targets before they disappear",
            "Faster clicks earn more points",
            f"Game duration: {game_duration_sec}s (configurable)",
            "Targets get smaller and faster over time",
            "",
            "SCORING:",
            "Base: 100 points per hit",
            "Bonus: up to +50 for fast reactions",
            "Miss: clicking empty space or timeout",
            "",
            "CONTROLS:",
            "Left Click: shoot target",
            "ESC: pause game",
        ]
        
        y_start = int(130 * scale_y)
        line_height = int(30 * scale_y)
        for i, line in enumerate(instructions):
            if line.startswith(("SCORING:", "CONTROLS:")):
                text = font.render(line, True, ACCENT_COLOR)
            elif line == "":
                continue
            else:
                text = font_small.render(f"  {line}", True, WHITE)
            screen.blit(text, text.get_rect(center=(center_x, y_start + i * line_height)))
        
        self.back_button.draw(screen, font_small, scale_x, scale_y)
