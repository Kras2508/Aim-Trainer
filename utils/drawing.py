"""
Drawing utilities for Aim Trainer
Contains all rendering and visual effect functions
"""

import pygame
import math
import sys
sys.path.append('..')
from config import *


def draw_crosshair(screen, pos, size=1.0, color=None, thickness=2, gap=5, length=12, outline=True, dot=True, dot_size=2, scale_x=1.0, scale_y=1.0):
    """Draw customizable crosshair like Valorant/CS:GO
    
    Args:
        screen: pygame surface
        pos: (x, y) center position in base coords (800x600)
        size: overall scale multiplier
        color: crosshair color
        thickness: line thickness (1-6)
        gap: center gap size (0-20)
        length: line length (0-30, 0 = dot only)
        outline: draw black outline around crosshair
        dot: draw center dot
        dot_size: center dot size (1-5)
        scale_x, scale_y: coordinate scaling factors
    """
    if color is None:
        color = CROSSHAIR_COLOR
    # Scale position to display coordinates
    x, y = int(pos[0] * scale_x), int(pos[1] * scale_y)
    scale_avg = (scale_x + scale_y) / 2
    
    # Apply size multiplier with scale
    actual_gap = int(gap * size * scale_avg)
    actual_length = int(length * size * scale_avg)
    actual_thickness = max(1, int(thickness * size * scale_avg))
    actual_dot_size = max(1, int(dot_size * size * scale_avg))
    
    # Use rect-based drawing for pixel-perfect centering
    half_t = actual_thickness // 2
    
    def draw_h_rect(surface, col, x1, x2, cy, t):
        """Draw a horizontal rect centered on cy"""
        ht = t // 2
        rect = pygame.Rect(x1, cy - ht, x2 - x1, t)
        pygame.draw.rect(surface, col, rect)
    
    def draw_v_rect(surface, col, cx, y1, y2, t):
        """Draw a vertical rect centered on cx"""
        ht = t // 2
        rect = pygame.Rect(cx - ht, y1, t, y2 - y1)
        pygame.draw.rect(surface, col, rect)
    
    # Draw lines only if length > 0
    if actual_length > 0:
        # Draw outline first (if enabled)
        if outline:
            outline_color = (0, 0, 0)
            ot = actual_thickness + 2
            # Horizontal outlines
            draw_h_rect(screen, outline_color, x - actual_length - actual_gap, x - actual_gap, y, ot)
            draw_h_rect(screen, outline_color, x + actual_gap, x + actual_length + actual_gap, y, ot)
            # Vertical outlines
            draw_v_rect(screen, outline_color, x, y - actual_length - actual_gap, y - actual_gap, ot)
            draw_v_rect(screen, outline_color, x, y + actual_gap, y + actual_length + actual_gap, ot)
        
        # Horizontal lines (as rects for perfect centering)
        draw_h_rect(screen, color, x - actual_length - actual_gap, x - actual_gap, y, actual_thickness)
        draw_h_rect(screen, color, x + actual_gap, x + actual_length + actual_gap, y, actual_thickness)
        
        # Vertical lines (as rects for perfect centering)
        draw_v_rect(screen, color, x, y - actual_length - actual_gap, y - actual_gap, actual_thickness)
        draw_v_rect(screen, color, x, y + actual_gap, y + actual_length + actual_gap, actual_thickness)
    
    # Dot outline (separate from lines)
    if outline and dot:
        pygame.draw.circle(screen, (0, 0, 0), (x, y), actual_dot_size + 1)
    
    # Center dot
    if dot:
        pygame.draw.circle(screen, color, (x, y), actual_dot_size)


def draw_hit_effect(screen, pos, elapsed_time, score_earned=None, scale_x=1.0, scale_y=1.0, combo=0):
    """Draw Aimlab-style hit marker (expanding circle with score and combo)"""
    max_time = 400  # ms
    if elapsed_time > max_time:
        return
    
    progress = elapsed_time / max_time
    scale_avg = (scale_x + scale_y) / 2
    size = int((15 + progress * 25) * scale_avg)
    
    # Scale position
    x, y = int(pos[0] * scale_x), int(pos[1] * scale_y)
    scaled_pos = (x, y)
    
    # Expanding circles
    for i in range(3):
        radius = size + int(i * 8 * scale_avg)
        thickness = max(1, int((3 - i) * scale_avg))
        pygame.draw.circle(screen, HIT_EFFECT_COLOR, scaled_pos, radius, thickness)
    
    # Center checkmark/dot
    dot_size = max(3, int(6 * (1 - progress) * scale_avg))
    pygame.draw.circle(screen, HIT_EFFECT_COLOR, scaled_pos, dot_size)
    
    # Draw score if provided
    if score_earned and elapsed_time < 300:
        font_size = max(16, int(32 * scale_avg))
        font = pygame.font.SysFont(None, font_size)
        score_text = font.render(f"+{score_earned}", True, SCORE_COLOR)
        score_rect = score_text.get_rect(center=(x, y - int((30 + progress * 20) * scale_y)))
        screen.blit(score_text, score_rect)
        
        # Draw combo text if combo >= 2
        if combo >= 2 and elapsed_time < 250:
            combo_font_size = max(14, int(24 * scale_avg))
            combo_font = pygame.font.SysFont(None, combo_font_size)
            combo_color = (
                min(255, 100 + combo * 20),
                max(0, 255 - combo * 15),
                50
            )
            combo_text = combo_font.render(f"x{combo} COMBO!", True, combo_color)
            combo_rect = combo_text.get_rect(center=(x, y - int((50 + progress * 20) * scale_y)))
            screen.blit(combo_text, combo_rect)


def draw_miss_effect(screen, pos, elapsed_time, scale_x=1.0, scale_y=1.0):
    """Draw miss effect (X marker)"""
    max_time = 300
    if elapsed_time > max_time:
        return
    
    progress = elapsed_time / max_time
    scale_avg = (scale_x + scale_y) / 2
    size = int((15 + progress * 10) * scale_avg)
    
    # Scale position
    x, y = int(pos[0] * scale_x), int(pos[1] * scale_y)
    
    # Draw X marker
    thickness = max(2, int(3 * scale_avg))
    pygame.draw.line(screen, MISS_EFFECT_COLOR, (x - size, y - size), (x + size, y + size), thickness)
    pygame.draw.line(screen, MISS_EFFECT_COLOR, (x + size, y - size), (x - size, y + size), thickness)


def draw_gradient_background(screen, scale_x=1.0, scale_y=1.0):
    """Draw vertical gradient background"""
    actual_width = int(BASE_WIDTH * scale_x)
    actual_height = int(BASE_HEIGHT * scale_y)
    for y in range(actual_height):
        progress = y / actual_height
        r = int(BACKGROUND_START[0] + (BACKGROUND_END[0] - BACKGROUND_START[0]) * progress)
        g = int(BACKGROUND_START[1] + (BACKGROUND_END[1] - BACKGROUND_START[1]) * progress)
        b = int(BACKGROUND_START[2] + (BACKGROUND_END[2] - BACKGROUND_START[2]) * progress)
        pygame.draw.line(screen, (r, g, b), (0, y), (actual_width, y))


def draw_decorated_background(screen, particles, current_time, scale_x=1.0, scale_y=1.0):
    """Draw gradient background with particles and geometric decorations"""
    actual_width = int(BASE_WIDTH * scale_x)
    actual_height = int(BASE_HEIGHT * scale_y)
    scale_avg = (scale_x + scale_y) / 2
    
    # Draw gradient
    draw_gradient_background(screen, scale_x, scale_y)
    
    # Draw grid lines (subtle)
    grid_color = (30, 35, 55)
    grid_spacing = int(50 * scale_avg)
    for x in range(0, actual_width, grid_spacing):
        pygame.draw.line(screen, grid_color, (x, 0), (x, actual_height), 1)
    for y in range(0, actual_height, grid_spacing):
        pygame.draw.line(screen, grid_color, (0, y), (actual_width, y), 1)
    
    # Update and draw particles (scaled)
    for particle in particles:
        particle.update()
        particle.draw(screen, scale_x, scale_y)
    
    # Draw corner decorations (animated) - sử dụng aaline cho animation mượt hơn
    anim_time = current_time * 0.002
    corner_color = (50, 60, 100)
    corner_margin = int(20 * scale_avg)
    corner_len = int(40 * scale_avg)
    corner_anim = int(5 * scale_avg)
    
    # Top left
    tl_offset = corner_margin + corner_anim * math.sin(anim_time)
    pygame.draw.aaline(screen, corner_color, (corner_margin, tl_offset), (corner_margin, tl_offset + corner_len))
    pygame.draw.aaline(screen, corner_color, (corner_margin, tl_offset), (corner_margin + corner_len, tl_offset))
    
    # Top right - phase offset 90 độ
    tr_offset = corner_margin + corner_anim * math.sin(anim_time + math.pi / 2)
    pygame.draw.aaline(screen, corner_color, (actual_width - corner_margin, tr_offset), (actual_width - corner_margin, tr_offset + corner_len))
    pygame.draw.aaline(screen, corner_color, (actual_width - corner_margin - corner_len, tr_offset), (actual_width - corner_margin, tr_offset))
    
    # Bottom left - phase offset 180 độ
    bl_offset = corner_margin + corner_anim * math.sin(anim_time + math.pi)
    pygame.draw.aaline(screen, corner_color, (corner_margin, actual_height - bl_offset - corner_len), (corner_margin, actual_height - bl_offset))
    pygame.draw.aaline(screen, corner_color, (corner_margin, actual_height - bl_offset), (corner_margin + corner_len, actual_height - bl_offset))
    
    # Bottom right - phase offset 270 độ
    br_offset = corner_margin + corner_anim * math.sin(anim_time + 3 * math.pi / 2)
    pygame.draw.aaline(screen, corner_color, (actual_width - corner_margin, actual_height - br_offset - corner_len), (actual_width - corner_margin, actual_height - br_offset))
    pygame.draw.aaline(screen, corner_color, (actual_width - corner_margin - corner_len, actual_height - br_offset), (actual_width - corner_margin, actual_height - br_offset))
