"""
Countdown Screen - 3-2-1-GO before game starts
"""

import pygame
from config import *


class CountdownScreen:
    """Countdown screen before game starts"""
    
    def __init__(self):
        self._last_number = None  # Track which number was last shown for beep
    
    def handle_events(self, event, selected_mode=None):
        """Handle countdown events. Returns new state or None."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.mouse.set_visible(True)
            return STATE_MODE_SELECT if selected_mode == MODE_TRACKING else STATE_DIFFICULTY
        return None
    
    def update(self, current_time, countdown_start_time, sound_manager=None):
        """Check if countdown is finished. Returns True if done."""
        countdown_elapsed = current_time - countdown_start_time
        
        # Play beep on each number change
        if sound_manager:
            remaining = max(0, COUNTDOWN_DURATION - countdown_elapsed)
            if remaining > 2000:
                num = 3
            elif remaining > 1000:
                num = 2
            elif remaining > 0:
                num = 1
            else:
                num = 0
            if num != self._last_number and num > 0:
                sound_manager.play_countdown()
            self._last_number = num
        
        return countdown_elapsed >= COUNTDOWN_DURATION
    
    def draw(self, screen, fonts, current_time, countdown_start_time, selected_difficulty, scale_x=1.0, scale_y=1.0, selected_mode=None):
        """Draw the countdown screen with scaling"""
        font_title, font_large, font, font_small = fonts
        
        center_x = int(BASE_WIDTH // 2 * scale_x)
        center_y = int(BASE_HEIGHT // 2 * scale_y)
        actual_width = int(BASE_WIDTH * scale_x)
        actual_height = int(BASE_HEIGHT * scale_y)
        
        countdown_elapsed = current_time - countdown_start_time
        remaining = max(0, COUNTDOWN_DURATION - countdown_elapsed)
        
        if remaining > 2000:
            text, color = "3", (255, 100, 100)
        elif remaining > 1000:
            text, color = "2", (255, 200, 100)
        elif remaining > 0:
            text, color = "1", (100, 255, 100)
        else:
            text, color = "GO!", SCORE_COLOR
        
        surface = font_title.render(text, True, color)
        screen.blit(surface, surface.get_rect(center=(center_x, center_y)))
        
        if selected_mode != MODE_TRACKING:
            diff_text = font.render(f"Difficulty: {selected_difficulty}", True, UI_COLOR)
            screen.blit(diff_text, diff_text.get_rect(center=(center_x, center_y + int(100 * scale_y))))
        
        esc_text = font_small.render("Press ESC to cancel", True, (100, 100, 100))
        screen.blit(esc_text, (actual_width - int(220 * scale_x), actual_height - int(30 * scale_y)))
