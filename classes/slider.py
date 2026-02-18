"""
Slider class for Aim Trainer settings
"""

import pygame
import math
import sys
sys.path.append('..')
from config import UI_COLOR, TARGET_PRIMARY, ACCENT_COLOR, WHITE


class Slider:
    """Slider control for settings"""
    
    def __init__(self, x, y, width, min_val, max_val, initial_val, label):
        self.x = x
        self.y = y
        self.width = width
        self.height = 10
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        self.handle_radius = 12
        self.selected = False
        self.input_text = ""
        self.input_mode = False
        
    def get_handle_x(self):
        """Calculate handle position based on value"""
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        return self.x + int(ratio * self.width)
    
    def draw(self, screen, font, scale_x=1.0, scale_y=1.0):
        """Draw the slider with scaling"""
        # Scale positions and sizes
        sx, sy = int(self.x * scale_x), int(self.y * scale_y)
        sw = int(self.width * scale_x)
        sh = int(self.height * scale_y)
        handle_r = int(self.handle_radius * (scale_x + scale_y) / 2)
        
        # Draw label
        label_text = font.render(self.label, True, UI_COLOR)
        screen.blit(label_text, (sx, sy - int(30 * scale_y)))
        
        # Draw track
        track_rect = pygame.Rect(sx, sy, sw, sh)
        pygame.draw.rect(screen, (50, 50, 70), track_rect)
        pygame.draw.rect(screen, UI_COLOR, track_rect, max(1, int(2 * (scale_x + scale_y) / 2)))
        
        # Draw filled portion
        filled_width = int((self.value - self.min_val) / (self.max_val - self.min_val) * sw)
        if filled_width > 0:
            filled_rect = pygame.Rect(sx, sy, filled_width, sh)
            pygame.draw.rect(screen, ACCENT_COLOR, filled_rect)
        
        # Draw handle
        handle_x = sx + int((self.value - self.min_val) / (self.max_val - self.min_val) * sw)
        handle_color = TARGET_PRIMARY if self.dragging else UI_COLOR
        pygame.draw.circle(screen, handle_color, (handle_x, sy + sh // 2), handle_r)
        pygame.draw.circle(screen, WHITE, (handle_x, sy + sh // 2), handle_r, max(1, int(2 * (scale_x + scale_y) / 2)))
        
        # Draw value (with input box if in input mode)
        if self.input_mode and self.selected:
            value_text = self.input_text + "_"
            box_color = (100, 150, 200)
        else:
            if self.max_val <= 2:
                value_text = f"{self.value:.3f}"
            elif self.max_val == 1:
                value_text = f"{int(self.value * 100)}%"
            else:
                value_text = f"{int(self.value)}"
            box_color = (80, 80, 100) if self.selected else (50, 50, 70)
        
        # Draw value box background
        value_surface = font.render(value_text, True, WHITE)
        value_rect = value_surface.get_rect(topleft=(sx + sw + int(20 * scale_x), sy - int(5 * scale_y)))
        value_box = value_rect.inflate(int(10 * scale_x), int(6 * scale_y))
        pygame.draw.rect(screen, box_color, value_box)
        pygame.draw.rect(screen, UI_COLOR if self.selected else (100, 100, 120), value_box, max(1, int(2 * (scale_x + scale_y) / 2)))
        screen.blit(value_surface, value_rect)
    
    def handle_event(self, event, mouse_pos):
        """Handle mouse and keyboard events for slider"""
        handle_x = self.get_handle_x()
        handle_y = self.y + self.height // 2
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if clicking on value box to enter input mode
            value_box_x = self.x + self.width + 20
            value_box_width = 80
            value_box_rect = pygame.Rect(value_box_x - 5, self.y - 10, value_box_width, 25)
            
            if value_box_rect.collidepoint(mouse_pos):
                self.selected = True
                self.input_mode = True
                self.input_text = ""
                return True
            
            # Check if clicking on handle
            dist = math.hypot(mouse_pos[0] - handle_x, mouse_pos[1] - handle_y)
            if dist <= self.handle_radius:
                self.dragging = True
                self.selected = True
                self.input_mode = False
                return True
            else:
                self.selected = False
                self.input_mode = False
       
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                return True
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Update value based on mouse position
                relative_x = mouse_pos[0] - self.x
                relative_x = max(0, min(self.width, relative_x))
                ratio = relative_x / self.width
                self.value = self.min_val + ratio * (self.max_val - self.min_val)
                return True
        
        elif event.type == pygame.KEYDOWN and self.input_mode and self.selected:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Apply the input value
                try:
                    new_value = float(self.input_text) if self.input_text else self.value
                    self.set_value(new_value)
                except ValueError:
                    pass  # Keep old value if invalid
                self.input_mode = False
                self.input_text = ""
                return True
            elif event.key == pygame.K_ESCAPE:
                # Cancel input
                self.input_mode = False
                self.input_text = ""
                self.selected = False
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
                return True
            elif event.unicode in '0123456789.':
                # Only allow one decimal point
                if event.unicode == '.' and '.' in self.input_text:
                    return True
                # Limit input length
                if len(self.input_text) < 8:
                    self.input_text += event.unicode
                return True
        
        return False
    
    def get_value(self):
        """Get current slider value"""
        return self.value
    
    def set_value(self, value):
        """Set slider value"""
        self.value = max(self.min_val, min(self.max_val, value))
