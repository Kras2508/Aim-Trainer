"""
Tracking Screen - Tracking mode gameplay
A single target moves smoothly along curved paths. Player must keep crosshair on it.
Score is based on percentage of time on target.
"""

import pygame
import math
import random
from config import *
from utils import draw_crosshair


class TrackingTarget:
    """A target that moves along smooth curved paths"""
    
    def __init__(self):
        self.x = BASE_WIDTH // 2
        self.y = BASE_HEIGHT // 2
        self.radius = TRACKING_TARGET_RADIUS
        self.on_target = False
        
        # Path control - use waypoints with smooth interpolation
        self._generate_new_path()
        self.path_progress = 0.0
        self.speed = 1.0  # Base speed, multiplied by phase speed in update
        
    def _generate_new_path(self):
        """Generate a new curved path using control points"""
        margin = MARGIN + self.radius
        self.path_start = (self.x, self.y)
        # Random destination
        self.path_end = (
            random.randint(margin, BASE_WIDTH - margin),
            random.randint(margin, BASE_HEIGHT - margin)
        )
        # Random control point for bezier curve (creates smooth arcs)
        mid_x = (self.path_start[0] + self.path_end[0]) / 2
        mid_y = (self.path_start[1] + self.path_end[1]) / 2
        offset = random.randint(80, 200)
        angle = random.uniform(0, 2 * math.pi)
        self.path_control = (
            max(margin, min(BASE_WIDTH - margin, mid_x + math.cos(angle) * offset)),
            max(margin, min(BASE_HEIGHT - margin, mid_y + math.sin(angle) * offset))
        )
        self.path_progress = 0.0
    
    def _bezier(self, t):
        """Quadratic bezier interpolation"""
        x = (1 - t) ** 2 * self.path_start[0] + \
            2 * (1 - t) * t * self.path_control[0] + \
            t ** 2 * self.path_end[0]
        y = (1 - t) ** 2 * self.path_start[1] + \
            2 * (1 - t) * t * self.path_control[1] + \
            t ** 2 * self.path_end[1]
        return x, y
    
    def update(self, dt, speed_multiplier=1.0):
        """Move target along path"""
        # Calculate speed based on path length
        dx = self.path_end[0] - self.path_start[0]
        dy = self.path_end[1] - self.path_start[1]
        path_len = max(100, math.hypot(dx, dy) * 1.3)  # Approximate bezier length
        
        step = (self.speed * speed_multiplier * dt) / path_len
        self.path_progress += step
        
        if self.path_progress >= 1.0:
            self.x, self.y = self.path_end
            self._generate_new_path()
        else:
            self.x, self.y = self._bezier(self.path_progress)
    
    def check_on_target(self, mouse_pos):
        """Check if cursor is within the target"""
        mx, my = mouse_pos
        dist = math.hypot(mx - self.x, my - self.y)
        self.on_target = dist <= self.radius
        return self.on_target
    
    def draw(self, screen, scale_x=1.0, scale_y=1.0):
        """Draw the tracking target"""
        sx = int(self.x * scale_x)
        sy = int(self.y * scale_y)
        scale_avg = (scale_x + scale_y) / 2
        scaled_radius = int(self.radius * scale_avg)
        
        # Glow effect based on on_target status
        glow_color = TRACKING_HIT_COLOR if self.on_target else TRACKING_MISS_COLOR
        for i in range(4):
            r = scaled_radius + int((6 - i) * scale_avg)
            alpha_color = (
                glow_color[0] // (i + 1),
                glow_color[1] // (i + 1),
                glow_color[2] // (i + 1)
            )
            pygame.draw.circle(screen, alpha_color, (sx, sy), r, 1)
        
        # Main circle
        circle_color = TRACKING_HIT_COLOR if self.on_target else TARGET_PRIMARY
        pygame.draw.circle(screen, circle_color, (sx, sy), scaled_radius, max(2, int(3 * scale_avg)))
        
        # Inner rings
        pygame.draw.circle(screen, TARGET_SECONDARY, (sx, sy), int(scaled_radius * 0.6), max(1, int(2 * scale_avg)))
        
        # Center dot
        pygame.draw.circle(screen, WHITE, (sx, sy), max(3, int(5 * scale_avg)))
        
        # Direction indicator - small line showing movement direction
        if self.path_progress < 1.0:
            t2 = min(1.0, self.path_progress + 0.05)
            nx, ny = self._bezier(t2)
            dx, dy = nx - self.x, ny - self.y
            length = math.hypot(dx, dy)
            if length > 0:
                dx, dy = dx / length, dy / length
                end_x = sx + int(dx * scaled_radius * 1.5)
                end_y = sy + int(dy * scaled_radius * 1.5)
                pygame.draw.line(screen, (100, 100, 150), (sx, sy), (end_x, end_y), max(1, int(2 * scale_avg)))


class TrackingScreen:
    """Tracking mode gameplay screen"""
    
    def handle_events(self, event, mouse_pos, game_data):
        """Handle tracking mode events. Returns new state or None."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.mouse.set_visible(True)
            return STATE_PAUSE
        return None
    
    def update(self, current_time, dt, mouse_pos, game_data, settings):
        """Update tracking mode logic. Returns STATE_GAME_OVER if time's up, else None."""
        elapsed_time = current_time - game_data['game_start_time']
        game_duration = game_data['game_duration']
        
        if elapsed_time >= game_duration:
            # Game over
            total_time = game_data['tracking_total_time']
            on_time = game_data['tracking_on_target_time']
            accuracy = (on_time / total_time * 100) if total_time > 0 else 0.0
            records = game_data['records']
            record_key = "TRACKING"
            if record_key not in records:
                records[record_key] = 0.0
            if accuracy > records[record_key]:
                records[record_key] = accuracy
                from utils import save_records
                save_records(records)
            pygame.mouse.set_visible(True)
            return STATE_GAME_OVER
        
        # Initialize tracking target if needed
        if game_data.get('tracking_target') is None:
            game_data['tracking_target'] = TrackingTarget()
            game_data['tracking_last_check'] = current_time
        
        target = game_data['tracking_target']
        
        # 3-phase speed progression (equal time segments)
        progress = min(1.0, elapsed_time / game_duration)
        if progress < 1 / 3:
            phase = 0
        elif progress < 2 / 3:
            phase = 1
        else:
            phase = 2
        speed_mult = TRACKING_PHASE_SPEEDS[phase]
        game_data['_tracking_phase'] = phase  # Store for HUD display
        
        # Radius stays constant (no shrinking — keep it fair)
        target.radius = TRACKING_TARGET_RADIUS
        
        # Update target movement
        target.update(dt, speed_mult)
        
        # Check if crosshair is on target
        is_on = target.check_on_target(mouse_pos)
        
        # Accumulate tracking time at intervals
        if current_time - game_data['tracking_last_check'] >= TRACKING_CHECK_INTERVAL:
            check_dt = current_time - game_data['tracking_last_check']
            game_data['tracking_total_time'] += check_dt
            if is_on:
                game_data['tracking_on_target_time'] += check_dt
                # Score: points per second on target, slightly higher in later phases
                score_rate = TRACKING_SCORE_PER_SECOND * (1 + phase * 0.25)
                game_data['tracking_score_accum'] += score_rate * (check_dt / 1000.0)
                game_data['score'] = int(game_data['tracking_score_accum'])
            game_data['tracking_last_check'] = current_time
        
        return None
    
    def draw(self, screen, fonts, mouse_pos, current_time, game_data, settings, scale_x=1.0, scale_y=1.0):
        """Draw the tracking mode screen"""
        font_title, font_large, font, font_small = fonts
        
        actual_width = int(BASE_WIDTH * scale_x)
        actual_height = int(BASE_HEIGHT * scale_y)
        center_x = int(BASE_WIDTH // 2 * scale_x)
        
        score = game_data['score']
        game_start_time = game_data['game_start_time']
        game_duration = game_data['game_duration']
        
        # Draw tracking target
        target = game_data.get('tracking_target')
        if target:
            target.draw(screen, scale_x, scale_y)
        
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
        total_time = game_data['tracking_total_time']
        on_time = game_data['tracking_on_target_time']
        accuracy = (on_time / total_time * 100) if total_time > 0 else 0
        phase = game_data.get('_tracking_phase', 0)
        phase_labels = ["PHASE 1 — Slow", "PHASE 2 — Medium", "PHASE 3 — Fast"]
        
        elapsed_time = current_time - game_start_time
        remaining_time = max(0, (game_duration - elapsed_time) // 1000)
        timer_color = UI_COLOR if remaining_time > 10 else MISS_EFFECT_COLOR
        timer_text = font_large.render(str(remaining_time), True, timer_color)
        screen.blit(timer_text, timer_text.get_rect(center=(center_x, int(30 * scale_y))))
        
        score_text = font.render(f"SCORE: {score}", True, SCORE_COLOR)
        screen.blit(score_text, (actual_width - int(200 * scale_x), int(15 * scale_y)))
        
        # Mode label — placed below timer with clear gap
        mode_text = font_small.render("TRACKING MODE", True, ACCENT_COLOR)
        screen.blit(mode_text, mode_text.get_rect(center=(center_x, int(78 * scale_y))))
        
        # On-target indicator bar (below score on right)
        bar_w = int(200 * scale_x)
        bar_h = int(12 * scale_y)
        bar_x = actual_width - int(220 * scale_x)
        bar_y = int(65 * scale_y)
        
        # Bar background
        pygame.draw.rect(screen, (40, 40, 60), (bar_x, bar_y, bar_w, bar_h))
        # Filled portion
        fill_w = int(bar_w * accuracy / 100)
        bar_color = TRACKING_HIT_COLOR if accuracy >= 70 else ACCENT_COLOR if accuracy >= 40 else MISS_EFFECT_COLOR
        if fill_w > 0:
            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_w, bar_h))
        pygame.draw.rect(screen, UI_COLOR, (bar_x, bar_y, bar_w, bar_h), 1)
        
        # Stats on left
        phase_color = SCORE_COLOR if phase == 0 else ACCENT_COLOR if phase == 1 else MISS_EFFECT_COLOR
        stats = [
            (phase_labels[phase], phase_color),
            (f"ACCURACY: {accuracy:.1f}%", ACCENT_COLOR),
            (f"SCORE: {score}", SCORE_COLOR),
        ]
        y_offset = int(20 * scale_y)
        line_h = int(28 * scale_y)
        for i, (stat, color) in enumerate(stats):
            text_surface = font_small.render(stat, True, color)
            screen.blit(text_surface, (int(20 * scale_x), y_offset + i * line_h))
        
        # On-target real-time indicator
        if target and target.on_target:
            on_text = font_small.render("ON TARGET", True, TRACKING_HIT_COLOR)
        else:
            on_text = font_small.render("OFF TARGET", True, TRACKING_MISS_COLOR)
        screen.blit(on_text, (int(20 * scale_x), y_offset + len(stats) * line_h))
        
        esc_text = font_small.render("Press ESC to pause", True, (100, 100, 100))
        screen.blit(esc_text, (actual_width - int(200 * scale_x), actual_height - int(30 * scale_y)))
