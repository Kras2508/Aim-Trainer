"""
Game Over Screen - Results display
"""

import pygame
from config import *
from classes import Button


class GameOverScreen:
    """Game over / results screen"""
    
    def __init__(self):
        cx = BASE_WIDTH // 2
        self.play_again_button = Button(cx - 120, BASE_HEIGHT // 2 + 130, 240, 60, "PLAY AGAIN", (50, 150, 50), (80, 200, 80))
        self.menu_button = Button(cx - 120, BASE_HEIGHT // 2 + 210, 240, 60, "MAIN MENU", (100, 100, 150), (150, 150, 200))
    
    def handle_events(self, event, mouse_pos):
        """Handle game over events. Returns new state or None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.play_again_button.is_clicked(mouse_pos):
                return STATE_DIFFICULTY
            elif self.menu_button.is_clicked(mouse_pos):
                return STATE_MENU
        return None
    
    def update(self, mouse_pos):
        """Update button hover states"""
        self.play_again_button.update(mouse_pos)
        self.menu_button.update(mouse_pos)
        pygame.mouse.set_visible(True)
    
    def draw(self, screen, fonts, game_data, scale_x=1.0, scale_y=1.0):
        """Draw the game over screen with scaling"""
        font_title, font_large, font, font_small = fonts
        
        center_x = int(BASE_WIDTH // 2 * scale_x)
        
        hits = game_data['hits']
        misses = game_data['misses']
        score = game_data['score']
        reaction_times = game_data['reaction_times']
        selected_difficulty = game_data['selected_difficulty']
        records = game_data['records']
        
        total_clicks = hits + misses
        accuracy = (hits / total_clicks * 100) if total_clicks > 0 else 0
        avg_reaction = sum(reaction_times) / len(reaction_times) if reaction_times else 0
        best_reaction = min(reaction_times) if reaction_times else 0
        
        # Title
        title = font_title.render("RESULTS", True, TARGET_PRIMARY)
        screen.blit(title, title.get_rect(center=(center_x, int(50 * scale_y))))
        
        # Score display
        score_display = font_large.render(str(score), True, SCORE_COLOR)
        screen.blit(score_display, score_display.get_rect(center=(center_x, int(120 * scale_y))))
        score_label = font_small.render("TOTAL SCORE", True, WHITE)
        screen.blit(score_label, score_label.get_rect(center=(center_x, int(155 * scale_y))))
        
        # Results stats
        results = [
            (f"Difficulty: {selected_difficulty}", UI_COLOR),
            (f"Hits: {hits}", SCORE_COLOR),
            (f"Misses: {misses}", MISS_EFFECT_COLOR),
            (f"Accuracy: {accuracy:.1f}%", ACCENT_COLOR),
            (f"Avg Reaction: {avg_reaction:.0f}ms", WHITE),
            (f"Best Reaction: {best_reaction:.0f}ms" if best_reaction > 0 else "Best Reaction: ---", WHITE),
        ]
        y_start = int(190 * scale_y)
        line_h = int(26 * scale_y)
        for i, (result, color) in enumerate(results):
            text = font_small.render(result, True, color)
            screen.blit(text, text.get_rect(center=(center_x, y_start + i * line_h)))
        
        # Record display
        record_y = y_start + len(results) * line_h + int(15 * scale_y)
        if accuracy >= records[selected_difficulty] and total_clicks > 0:
            record_text = font.render("NEW RECORD!", True, SCORE_COLOR)
        else:
            record_text = font_small.render(f"Record: {records[selected_difficulty]:.2f}%", True, UI_COLOR)
        screen.blit(record_text, record_text.get_rect(center=(center_x, record_y)))
        
        # Buttons
        self.play_again_button.draw(screen, font, scale_x, scale_y)
        self.menu_button.draw(screen, font, scale_x, scale_y)
