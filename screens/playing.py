"""
Playing Screen - Main gameplay with targets, crosshair, and HUD
"""

import pygame
import random
from config import *
from classes import Target
from utils import (
    draw_crosshair, draw_hit_effect, draw_miss_effect,
    random_spawn_position
)


class PlayingScreen:
    """Main gameplay screen"""
    
    def handle_events(self, event, mouse_pos, game_data):
        """Handle gameplay events. Returns new state or None.
        
        game_data dict keys: targets, hits, misses, score, hit_effects, 
                             miss_effects, reaction_times, hit_sound, current_time
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.mouse.set_visible(True)
            return STATE_PAUSE
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            current_time = game_data['current_time']
            hit_registered = False
            
            for target in game_data['targets']:
                if target.alive and target.check_hit(mouse_pos):
                    game_data['hits'] += 1
                    # Combo system
                    game_data['combo'] = game_data.get('combo', 0) + 1
                    game_data['max_combo'] = max(game_data.get('max_combo', 0), game_data['combo'])
                    combo_mult = min(COMBO_MULTIPLIER_MAX, 1.0 + (game_data['combo'] - 1) * COMBO_MULTIPLIER_STEP)
                    # Calculate score
                    base_points = 100
                    bonus_cap = 50
                    reaction = target.reaction_time
                    ttl = target.lifetime
                    bonus = int(max(0, ttl - reaction) / ttl * bonus_cap)
                    earned = int((base_points + bonus) * combo_mult)
                    game_data['score'] += earned
                    game_data['reaction_times'].append(reaction)
                    game_data['hit_effects'].append((mouse_pos, current_time, earned, game_data['combo']))
                    hit_registered = True
                    if game_data.get('sound_manager'):
                        game_data['sound_manager'].play_hit()
                    break
            
            if not hit_registered:
                game_data['misses'] += 1
                game_data['combo'] = 0  # Reset combo on miss
                game_data['miss_effects'].append((mouse_pos, current_time))
                if game_data.get('sound_manager'):
                    game_data['sound_manager'].play_miss()
        
        return None
    
    def update(self, current_time, game_data, settings):
        """Update game logic. Returns STATE_GAME_OVER if time's up, else None.
        
        game_data dict keys: targets, hits, misses, score, game_start_time,
                             game_duration, last_spawn_time, current_target_size,
                             selected_difficulty, records
        """
        elapsed_time = current_time - game_data['game_start_time']
        game_duration = game_data['game_duration']
        
        if elapsed_time >= game_duration:
            # Game over
            total_clicks = game_data['hits'] + game_data['misses']
            accuracy = (game_data['hits'] / total_clicks * 100) if total_clicks > 0 else 0.0
            records = game_data['records']
            difficulty = game_data['selected_difficulty']
            if accuracy > records[difficulty]:
                records[difficulty] = accuracy
                from utils import save_records
                save_records(records)
            pygame.mouse.set_visible(True)
            return STATE_GAME_OVER
        
        # Get difficulty settings
        difficulty = game_data['selected_difficulty']
        diff_settings = DIFFICULTIES[difficulty]
        target_min_lifetime = diff_settings['min_lifetime']
        target_max_lifetime = diff_settings['max_lifetime']
        spawn_delay = diff_settings['spawn_delay']
        max_targets = diff_settings['max_targets']
        targets = game_data['targets']
        
        # Remove expired targets
        for target in targets[:]:
            if (current_time - target.spawn_time) >= target.lifetime:
                if target.alive:
                    game_data['misses'] += 1
                    game_data['combo'] = 0  # Reset combo on timeout
                targets.remove(target)
        
        # Difficulty progression
        progress = min(1.0, elapsed_time / game_duration)
        if progress < 0.5:
            game_data['current_target_size'] = TARGET_SIZE_START - int((TARGET_SIZE_START - TARGET_SIZE_MEDIUM) * (progress * 2))
        else:
            game_data['current_target_size'] = TARGET_SIZE_MEDIUM - int((TARGET_SIZE_MEDIUM - TARGET_SIZE_SMALL) * ((progress - 0.5) * 2))
        
        adjusted_min = int(target_min_lifetime * (1 - progress * 0.3))
        adjusted_max = int(target_max_lifetime * (1 - progress * 0.3))
        
        # Spawn new targets
        alive_targets = [t for t in targets if t.alive]
        if len(alive_targets) < max_targets and current_time - game_data['last_spawn_time'] >= spawn_delay:
            new_target = Target(random_spawn_position(targets), game_data['current_target_size'])
            new_target.lifetime = random.randint(max(500, adjusted_min), max(800, adjusted_max))
            targets.append(new_target)
            game_data['last_spawn_time'] = current_time
        
        return None
    
    def draw(self, screen, fonts, mouse_pos, current_time, game_data, settings, scale_x=1.0, scale_y=1.0):
        """Draw the gameplay screen with scaling"""
        font_title, font_large, font, font_small = fonts
        
        actual_width = int(BASE_WIDTH * scale_x)
        actual_height = int(BASE_HEIGHT * scale_y)
        center_x = int(BASE_WIDTH // 2 * scale_x)
        
        targets = game_data['targets']
        hit_effects = game_data['hit_effects']
        miss_effects = game_data['miss_effects']
        hits = game_data['hits']
        misses = game_data['misses']
        score = game_data['score']
        reaction_times = game_data['reaction_times']
        selected_difficulty = game_data['selected_difficulty']
        game_start_time = game_data['game_start_time']
        game_duration = game_data['game_duration']
        
        # Draw targets (scaled)
        for target in targets:
            if target.alive:
                target.draw(screen, scale_x, scale_y)
        
        # Draw effects
        game_data['hit_effects'] = [e for e in hit_effects if current_time - e[1] < 400]
        for effect in game_data['hit_effects']:
            pos, hit_time, score_earned = effect[0], effect[1], effect[2]
            combo_count = effect[3] if len(effect) > 3 else 0
            draw_hit_effect(screen, pos, current_time - hit_time, score_earned, scale_x, scale_y, combo_count)
        
        game_data['miss_effects'] = [(pos, t) for pos, t in miss_effects if current_time - t < 300]
        for pos, miss_time in game_data['miss_effects']:
            draw_miss_effect(screen, pos, current_time - miss_time, scale_x, scale_y)
        
        # Draw crosshair
        crosshair_color = CROSSHAIR_COLORS.get(settings['crosshair_color'], CROSSHAIR_COLOR)
        draw_crosshair(screen, mouse_pos,
                      settings['crosshair_size'],
                      crosshair_color,
                      settings.get('crosshair_thickness', 2),
                      settings.get('crosshair_gap', 5),
                      settings.get('crosshair_length', 12),
                      settings.get('crosshair_outline', True),
                      settings.get('crosshair_dot', True),
                      settings.get('crosshair_dot_size', 2),
                      scale_x, scale_y)
        
        # HUD
        total_clicks = hits + misses
        accuracy = (hits / total_clicks * 100) if total_clicks > 0 else 0
        avg_reaction = sum(reaction_times) / len(reaction_times) if reaction_times else 0
        best_reaction = min(reaction_times) if reaction_times else 0
        combo = game_data.get('combo', 0)
        combo_mult = min(COMBO_MULTIPLIER_MAX, 1.0 + (combo - 1) * COMBO_MULTIPLIER_STEP) if combo > 0 else 1.0
        
        elapsed_time = current_time - game_start_time
        remaining_time = max(0, (game_duration - elapsed_time) // 1000)
        timer_color = UI_COLOR if remaining_time > 10 else MISS_EFFECT_COLOR
        timer_text = font_large.render(str(remaining_time), True, timer_color)
        screen.blit(timer_text, timer_text.get_rect(center=(center_x, int(40 * scale_y))))
        
        score_text = font.render(f"SCORE: {score}", True, SCORE_COLOR)
        screen.blit(score_text, (actual_width - int(200 * scale_x), int(20 * scale_y)))
        
        # Combo display (right side, below score)
        if combo >= 2:
            combo_color = (
                min(255, 100 + combo * 20),
                max(0, 255 - combo * 15),
                50
            )
            combo_text = font.render(f"COMBO x{combo}", True, combo_color)
            screen.blit(combo_text, (actual_width - int(200 * scale_x), int(55 * scale_y)))
            mult_text = font_small.render(f"{combo_mult:.1f}x multiplier", True, ACCENT_COLOR)
            screen.blit(mult_text, (actual_width - int(200 * scale_x), int(85 * scale_y)))
        
        stats = [
            (f"DIFFICULTY: {selected_difficulty}", UI_COLOR),
            (f"HITS: {hits}", SCORE_COLOR),
            (f"MISSES: {misses}", MISS_EFFECT_COLOR),
            (f"ACCURACY: {accuracy:.1f}%", ACCENT_COLOR),
            (f"AVG: {avg_reaction:.0f}ms", WHITE),
            (f"BEST: {best_reaction:.0f}ms" if best_reaction > 0 else "BEST: ---", WHITE),
        ]
        y_offset = int(20 * scale_y)
        line_h = int(28 * scale_y)
        for i, (stat, color) in enumerate(stats):
            text_surface = font_small.render(stat, True, color)
            screen.blit(text_surface, (int(20 * scale_x), y_offset + i * line_h))
        
        esc_text = font_small.render("Press ESC to pause", True, (100, 100, 100))
        screen.blit(esc_text, (actual_width - int(200 * scale_x), actual_height - int(30 * scale_y)))
