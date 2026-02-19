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
        self.play_again_button = Button(cx - 110, 420, 220, 48, "PLAY AGAIN", (50, 150, 50), (80, 200, 80))
        self.menu_button = Button(cx - 110, 480, 220, 48, "MAIN MENU", (100, 100, 150), (150, 150, 200))
    
    def handle_events(self, event, mouse_pos):
        """Handle game over events. Returns new state or None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.play_again_button.is_clicked(mouse_pos):
                return STATE_MODE_SELECT
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
        
        selected_mode = game_data.get('selected_mode', MODE_CLASSIC)
        
        if selected_mode == MODE_TRACKING:
            self._draw_tracking_results(screen, fonts, game_data, center_x, scale_x, scale_y)
        else:
            self._draw_classic_results(screen, fonts, game_data, center_x, scale_x, scale_y)
        
        # Buttons
        self.play_again_button.draw(screen, font, scale_x, scale_y)
        self.menu_button.draw(screen, font, scale_x, scale_y)
    
    def _draw_classic_results(self, screen, fonts, game_data, center_x, scale_x, scale_y):
        """Draw classic mode results"""
        font_title, font_large, font, font_small = fonts
        
        hits = game_data['hits']
        misses = game_data['misses']
        score = game_data['score']
        reaction_times = game_data['reaction_times']
        selected_difficulty = game_data['selected_difficulty']
        records = game_data['records']
        max_combo = game_data.get('max_combo', 0)
        
        total_clicks = hits + misses
        accuracy = (hits / total_clicks * 100) if total_clicks > 0 else 0
        avg_reaction = sum(reaction_times) / len(reaction_times) if reaction_times else 0
        best_reaction = min(reaction_times) if reaction_times else 0
        
        # Title
        title = font_large.render("RESULTS", True, TARGET_PRIMARY)
        screen.blit(title, title.get_rect(center=(center_x, int(35 * scale_y))))
        
        # Score display
        score_display = font_large.render(str(score), True, SCORE_COLOR)
        screen.blit(score_display, score_display.get_rect(center=(center_x, int(100 * scale_y))))
        score_label = font_small.render("TOTAL SCORE", True, WHITE)
        screen.blit(score_label, score_label.get_rect(center=(center_x, int(140 * scale_y))))
        
        # Results stats
        results = [
            (f"Difficulty: {selected_difficulty}", UI_COLOR),
            (f"Hits: {hits}", SCORE_COLOR),
            (f"Misses: {misses}", MISS_EFFECT_COLOR),
            (f"Accuracy: {accuracy:.1f}%", ACCENT_COLOR),
            (f"Avg Reaction: {avg_reaction:.0f}ms", WHITE),
            (f"Best Reaction: {best_reaction:.0f}ms" if best_reaction > 0 else "Best Reaction: ---", WHITE),
            (f"Best Combo: {max_combo}x", (255, 200, 50) if max_combo >= 5 else WHITE),
        ]
        y_start = int(175 * scale_y)
        line_h = int(28 * scale_y)
        for i, (result, color) in enumerate(results):
            text = font_small.render(result, True, color)
            screen.blit(text, text.get_rect(center=(center_x, y_start + i * line_h)))
        
        # Record display
        record_y = y_start + len(results) * line_h + int(18 * scale_y)
        if accuracy >= records[selected_difficulty] and total_clicks > 0:
            record_text = font.render("NEW RECORD!", True, SCORE_COLOR)
        else:
            record_text = font_small.render(f"Record: {records[selected_difficulty]:.2f}%", True, UI_COLOR)
        screen.blit(record_text, record_text.get_rect(center=(center_x, record_y)))
    
    def _draw_tracking_results(self, screen, fonts, game_data, center_x, scale_x, scale_y):
        """Draw tracking mode results"""
        font_title, font_large, font, font_small = fonts
        
        score = game_data['score']
        records = game_data['records']
        total_time = game_data.get('tracking_total_time', 0)
        on_time = game_data.get('tracking_on_target_time', 0)
        accuracy = (on_time / total_time * 100) if total_time > 0 else 0
        
        # Title
        title = font_large.render("RESULTS", True, TARGET_PRIMARY)
        screen.blit(title, title.get_rect(center=(center_x, int(40 * scale_y))))
        
        mode_label = font.render("TRACKING MODE", True, ACCENT_COLOR)
        screen.blit(mode_label, mode_label.get_rect(center=(center_x, int(90 * scale_y))))
        
        # Score display
        score_display = font_large.render(str(score), True, SCORE_COLOR)
        screen.blit(score_display, score_display.get_rect(center=(center_x, int(140 * scale_y))))
        score_label = font_small.render("TOTAL SCORE", True, WHITE)
        screen.blit(score_label, score_label.get_rect(center=(center_x, int(180 * scale_y))))
        
        # Results stats
        results = [
            (f"On-Target Accuracy: {accuracy:.1f}%", ACCENT_COLOR),
            (f"Time On Target: {on_time / 1000:.1f}s", SCORE_COLOR),
            (f"Total Time: {total_time / 1000:.1f}s", WHITE),
        ]
        y_start = int(220 * scale_y)
        line_h = int(38 * scale_y)
        for i, (result, color) in enumerate(results):
            text = font_small.render(result, True, color)
            screen.blit(text, text.get_rect(center=(center_x, y_start + i * line_h)))
        
        # Record display
        record_key = "TRACKING"
        record_val = records.get(record_key, 0.0)
        record_y = y_start + len(results) * line_h + int(20 * scale_y)
        if accuracy >= record_val and total_time > 0:
            record_text = font.render("NEW RECORD!", True, SCORE_COLOR)
        else:
            record_text = font_small.render(f"Record: {record_val:.2f}%", True, UI_COLOR)
        screen.blit(record_text, record_text.get_rect(center=(center_x, record_y)))
