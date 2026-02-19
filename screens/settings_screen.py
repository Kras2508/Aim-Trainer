"""
Settings Screen - Tabbed settings with General and Crosshair tabs, scrollable
"""

import pygame
from config import *
from classes import Button, Slider
from utils import draw_crosshair


class SettingsScreen:
    """Settings screen with tab layout: General | Crosshair (scrollable)"""
    
    TAB_GENERAL = 0
    TAB_CROSSHAIR = 1
    
    # Layout constants (in base 800x600 coordinates)
    CONTENT_TOP = 120        # where content area starts (below tabs)
    CONTENT_BOTTOM = 530     # where content area ends (above buttons)
    SCROLL_SPEED = 30        # pixels per scroll tick
    SL_X = 50                # slider x
    SL_W = BASE_WIDTH - 200  # slider width
    SL_SPACING = 80          # spacing between sliders
    
    def __init__(self, settings):
        self.active_tab = self.TAB_GENERAL
        self.scroll_y = 0     # scroll offset for crosshair tab
        self.return_state = STATE_MENU  # where to go back (menu or pause)
        
        # ── General tab sliders (absolute positions, no scroll) ──
        self.sensitivity_slider = Slider(self.SL_X, 160, self.SL_W, 0.1, 2.0,
                                         settings['mouse_sensitivity'], "Mouse Sensitivity")
        self.volume_slider = Slider(self.SL_X, 260, self.SL_W, 0.0, 1.0,
                                    settings['volume'], "Volume")
        self.game_duration_slider = Slider(self.SL_X, 360, self.SL_W, 30, 120,
                                           settings['game_duration'], "Game Duration (sec)")
        
        # ── Crosshair tab sliders (y set dynamically via _apply_scroll) ──
        self.crosshair_size_slider = Slider(self.SL_X, 0, self.SL_W, 0.5, 2.0,
                                            settings['crosshair_size'], "Size")
        self.crosshair_thickness_slider = Slider(self.SL_X, 0, self.SL_W, 1, 6,
                                                  settings.get('crosshair_thickness', 2), "Thickness")
        self.crosshair_gap_slider = Slider(self.SL_X, 0, self.SL_W, 0, 20,
                                           settings.get('crosshair_gap', 5), "Gap")
        self.crosshair_length_slider = Slider(self.SL_X, 0, self.SL_W, 0, 30,
                                              settings.get('crosshair_length', 12), "Length")
        self.crosshair_dot_size_slider = Slider(self.SL_X, 0, self.SL_W, 1, 5,
                                                settings.get('crosshair_dot_size', 2), "Dot Size")
        self.ch_sliders = [
            self.crosshair_size_slider, self.crosshair_thickness_slider,
            self.crosshair_gap_slider, self.crosshair_length_slider,
            self.crosshair_dot_size_slider
        ]
        
        # Content-space Y offsets for crosshair elements (relative to content top)
        # Sliders at 30, 110, 190, 270, 350
        self._ch_slider_offsets = [30 + i * self.SL_SPACING for i in range(5)]
        self._ch_toggle_offset = 30 + 5 * self.SL_SPACING - 20   # 430-20=410
        self._ch_preview_offset = self._ch_toggle_offset           # same row, right side
        self._ch_color_label_offset = self._ch_toggle_offset + 50  # 460
        self._ch_color_boxes_offset = self._ch_color_label_offset + 22  # 482
        self._ch_content_height = self._ch_color_boxes_offset + 40  # 522 total
        
        # Toggles
        self.crosshair_outline = settings.get('crosshair_outline', True)
        self.crosshair_dot = settings.get('crosshair_dot', True)
        self.outline_rect = pygame.Rect(self.SL_X, 0, 190, 30)
        self.dot_rect = pygame.Rect(self.SL_X + 210, 0, 150, 30)
        
        # Color selection
        self.selected_crosshair_color = settings['crosshair_color']
        self.color_boxes = []
        box_size = 30
        box_spacing = 8
        colors_list = list(CROSSHAIR_COLORS.items())
        total_w = len(colors_list) * box_size + (len(colors_list) - 1) * box_spacing
        start_x = (BASE_WIDTH - total_w) // 2
        for i, (color_name, color_value) in enumerate(colors_list):
            bx = start_x + i * (box_size + box_spacing)
            self.color_boxes.append({
                'name': color_name,
                'color': color_value,
                'rect': pygame.Rect(bx, 0, box_size, box_size)
            })
        
        # Tab rects (in base coordinates)
        tab_w = 200
        tab_h = 40
        tab_y = 70
        self.tab_general_rect = pygame.Rect(BASE_WIDTH // 2 - tab_w - 5, tab_y, tab_w, tab_h)
        self.tab_crosshair_rect = pygame.Rect(BASE_WIDTH // 2 + 5, tab_y, tab_w, tab_h)
        
        # Buttons (fixed at bottom, never scroll)
        self.back_button = Button(50, BASE_HEIGHT - 60, 120, 45, "BACK",
                                  (100, 100, 100), (150, 150, 150))
        self.save_button = Button(BASE_WIDTH - 250, BASE_HEIGHT - 60, 200, 45,
                                  "SAVE & APPLY", (50, 150, 50), (80, 200, 80))
        
        # Apply initial scroll positions
        self._apply_scroll()
    
    @property
    def _max_scroll(self):
        """Maximum scroll offset"""
        visible_h = self.CONTENT_BOTTOM - self.CONTENT_TOP
        return max(0, self._ch_content_height - visible_h)
    
    def _apply_scroll(self):
        """Reposition all crosshair-tab elements based on current scroll_y"""
        base = self.CONTENT_TOP - self.scroll_y
        # Sliders
        for slider, offset in zip(self.ch_sliders, self._ch_slider_offsets):
            slider.y = base + offset
        # Toggles
        ty = base + self._ch_toggle_offset
        self.outline_rect.y = ty
        self.dot_rect.y = ty
        # Color boxes
        for box in self.color_boxes:
            box['rect'].y = base + self._ch_color_boxes_offset
    
    def _in_content_area(self, pos):
        """Check if a position is inside the scrollable content area"""
        return self.CONTENT_TOP <= pos[1] <= self.CONTENT_BOTTOM
    
    def handle_events(self, event, mouse_pos, settings, save_settings_func, sound_manager):
        """Handle settings events. Returns new state or None."""
        # Scroll wheel (only for crosshair tab)
        if event.type == pygame.MOUSEWHEEL and self.active_tab == self.TAB_CROSSHAIR:
            self.scroll_y -= event.y * self.SCROLL_SPEED
            self.scroll_y = max(0, min(self._max_scroll, self.scroll_y))
            self._apply_scroll()
            return None
        
        # Slider events - only if mouse is in content area
        in_content = self._in_content_area(mouse_pos)
        if self.active_tab == self.TAB_GENERAL:
            self.sensitivity_slider.handle_event(event, mouse_pos)
            self.volume_slider.handle_event(event, mouse_pos)
            self.game_duration_slider.handle_event(event, mouse_pos)
        else:
            # For dragging, always handle (slider might be dragged outside area)
            any_dragging = any(s.dragging for s in self.ch_sliders)
            if in_content or any_dragging:
                for s in self.ch_sliders:
                    s.handle_event(event, mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Tab clicks (always accessible)
            if self.tab_general_rect.collidepoint(mouse_pos):
                self.active_tab = self.TAB_GENERAL
                return None
            elif self.tab_crosshair_rect.collidepoint(mouse_pos):
                self.active_tab = self.TAB_CROSSHAIR
                self.scroll_y = 0
                self._apply_scroll()
                return None
            
            # Button clicks (always accessible)
            if self.back_button.is_clicked(mouse_pos):
                return self.return_state
            elif self.save_button.is_clicked(mouse_pos):
                return self._save_settings(settings, save_settings_func, sound_manager)
            
            # Crosshair tab clickables (only in content area)
            if self.active_tab == self.TAB_CROSSHAIR and in_content:
                if self.outline_rect.collidepoint(mouse_pos):
                    self.crosshair_outline = not self.crosshair_outline
                elif self.dot_rect.collidepoint(mouse_pos):
                    self.crosshair_dot = not self.crosshair_dot
                for box in self.color_boxes:
                    if box['rect'].collidepoint(mouse_pos):
                        self.selected_crosshair_color = box['name']
        return None
    
    def _save_settings(self, settings, save_settings_func, sound_manager):
        """Save all settings and return to previous screen"""
        settings['mouse_sensitivity'] = self.sensitivity_slider.get_value()
        settings['volume'] = self.volume_slider.get_value()
        settings['game_duration'] = int(self.game_duration_slider.get_value())
        settings['crosshair_size'] = self.crosshair_size_slider.get_value()
        settings['crosshair_thickness'] = int(self.crosshair_thickness_slider.get_value())
        settings['crosshair_gap'] = int(self.crosshair_gap_slider.get_value())
        settings['crosshair_length'] = int(self.crosshair_length_slider.get_value())
        settings['crosshair_dot_size'] = int(self.crosshair_dot_size_slider.get_value())
        settings['crosshair_outline'] = self.crosshair_outline
        settings['crosshair_dot'] = self.crosshair_dot
        settings['crosshair_color'] = self.selected_crosshair_color
        save_settings_func(settings)
        if sound_manager:
            sound_manager.set_volume(settings['volume'])
        return self.return_state
    
    def update(self, mouse_pos):
        """Update button hover states"""
        self.back_button.update(mouse_pos)
        self.save_button.update(mouse_pos)
        pygame.mouse.set_visible(True)
    
    def _draw_tab(self, screen, font, rect, label, is_active):
        """Draw a single tab button"""
        if is_active:
            bg = (50, 60, 100)
            border = ACCENT_COLOR
            text_color = WHITE
        else:
            bg = (30, 35, 55)
            border = (60, 60, 80)
            text_color = (120, 120, 140)
        pygame.draw.rect(screen, bg, rect)
        pygame.draw.rect(screen, border, rect, 2)
        text = font.render(label, True, text_color)
        screen.blit(text, text.get_rect(center=rect.center))
    
    def draw(self, screen, fonts, scale_x=1.0, scale_y=1.0):
        """Draw the settings screen with scaling"""
        font_title, font_large, font, font_small = fonts
        
        actual_width = int(BASE_WIDTH * scale_x)
        actual_height = int(BASE_HEIGHT * scale_y)
        center_x = int(BASE_WIDTH // 2 * scale_x)
        
        # Title
        title = font_large.render("SETTINGS", True, UI_COLOR)
        screen.blit(title, title.get_rect(center=(center_x, int(35 * scale_y))))
        
        # Scale and draw tabs
        scaled_general_rect = pygame.Rect(
            int(self.tab_general_rect.x * scale_x),
            int(self.tab_general_rect.y * scale_y),
            int(self.tab_general_rect.width * scale_x),
            int(self.tab_general_rect.height * scale_y)
        )
        scaled_crosshair_rect = pygame.Rect(
            int(self.tab_crosshair_rect.x * scale_x),
            int(self.tab_crosshair_rect.y * scale_y),
            int(self.tab_crosshair_rect.width * scale_x),
            int(self.tab_crosshair_rect.height * scale_y)
        )
        self._draw_tab(screen, font, scaled_general_rect, "GENERAL",
                       self.active_tab == self.TAB_GENERAL)
        self._draw_tab(screen, font, scaled_crosshair_rect, "CROSSHAIR",
                       self.active_tab == self.TAB_CROSSHAIR)
        
        # Content area separator
        sep_y = int(115 * scale_y)
        pygame.draw.line(screen, (50, 60, 100), (int(30 * scale_x), sep_y), (actual_width - int(30 * scale_x), sep_y), 1)
        
        # Clip to content area so scrolled items don't bleed into tabs/buttons
        content_top = int(self.CONTENT_TOP * scale_y)
        content_bottom = int(self.CONTENT_BOTTOM * scale_y)
        content_rect = pygame.Rect(0, content_top, actual_width, content_bottom - content_top)
        screen.set_clip(content_rect)
        
        if self.active_tab == self.TAB_GENERAL:
            self._draw_general_tab(screen, font, font_small, scale_x, scale_y)
        else:
            self._draw_crosshair_tab(screen, font, font_small, scale_x, scale_y)
        
        # Remove clip
        screen.set_clip(None)
        
        # Scrollbar indicator (crosshair tab only)
        if self.active_tab == self.TAB_CROSSHAIR and self._max_scroll > 0:
            self._draw_scrollbar(screen, scale_x, scale_y)
        
        # Bottom buttons (always drawn, never clipped)
        self.back_button.draw(screen, font_small, scale_x, scale_y)
        self.save_button.draw(screen, font_small, scale_x, scale_y)
    
    def _draw_scrollbar(self, screen, scale_x=1.0, scale_y=1.0):
        """Draw a thin scrollbar on the right edge"""
        actual_width = int(BASE_WIDTH * scale_x)
        bar_x = actual_width - int(8 * scale_x)
        bar_h = int((self.CONTENT_BOTTOM - self.CONTENT_TOP) * scale_y)
        bar_top = int(self.CONTENT_TOP * scale_y)
        bar_w = max(3, int(5 * scale_x))
        
        # Track
        pygame.draw.rect(screen, (40, 40, 60),
                         (bar_x, bar_top, bar_w, bar_h))
        
        # Thumb
        visible_ratio = bar_h / (self._ch_content_height * scale_y)
        thumb_h = max(int(20 * scale_y), int(bar_h * visible_ratio))
        scroll_ratio = self.scroll_y / self._max_scroll if self._max_scroll > 0 else 0
        thumb_y = bar_top + int(scroll_ratio * (bar_h - thumb_h))
        pygame.draw.rect(screen, (100, 110, 140),
                         (bar_x, thumb_y, bar_w, thumb_h))
    
    def _draw_general_tab(self, screen, font, font_small, scale_x=1.0, scale_y=1.0):
        """Draw General tab content"""
        self.sensitivity_slider.draw(screen, font_small, scale_x, scale_y)
        self.volume_slider.draw(screen, font_small, scale_x, scale_y)
        self.game_duration_slider.draw(screen, font_small, scale_x, scale_y)
        
        tips = [
            "Mouse Sensitivity: affects cursor speed in-game",
            "Volume: game sound effects volume",
            "Duration: how long each round lasts",
        ]
        y = int(430 * scale_y)
        line_h = int(24 * scale_y)
        for tip in tips:
            text = font_small.render(tip, True, (80, 90, 110))
            screen.blit(text, (int(50 * scale_x), y))
            y += line_h
    
    def _draw_crosshair_tab(self, screen, font, font_small, scale_x=1.0, scale_y=1.0):
        """Draw Crosshair tab content (positions already set by _apply_scroll)"""
        actual_width = int(BASE_WIDTH * scale_x)
        
        # Sliders
        for s in self.ch_sliders:
            s.draw(screen, font_small, scale_x, scale_y)
        
        # Toggle buttons (scale positions)
        outline_scaled = pygame.Rect(
            int(self.outline_rect.x * scale_x),
            int(self.outline_rect.y * scale_y),
            int(self.outline_rect.width * scale_x),
            int(self.outline_rect.height * scale_y)
        )
        dot_scaled = pygame.Rect(
            int(self.dot_rect.x * scale_x),
            int(self.dot_rect.y * scale_y),
            int(self.dot_rect.width * scale_x),
            int(self.dot_rect.height * scale_y)
        )
        
        # ── Toggle switches: "Label:" text + separate ON/OFF pill ──
        for rect_scaled, is_on, label_text_str in [
            (outline_scaled, self.crosshair_outline, "Outline:"),
            (dot_scaled, self.crosshair_dot, "Dot:"),
        ]:
            # Draw label text on the left
            lbl_surface = font_small.render(label_text_str, True, UI_COLOR)
            screen.blit(lbl_surface, lbl_surface.get_rect(midleft=(rect_scaled.left, rect_scaled.centery)))
            
            # Draw ON/OFF pill switch to the right of label
            lbl_w = lbl_surface.get_width() + int(10 * scale_x)
            pill_w = int(44 * scale_x)
            pill_h = int(24 * scale_y)
            pill_x = rect_scaled.left + lbl_w
            pill_y = rect_scaled.centery - pill_h // 2
            pill_rect = pygame.Rect(pill_x, pill_y, pill_w, pill_h)
            pill_r = pill_h // 2
            
            # Pill background
            bg_color = (40, 130, 75) if is_on else (70, 55, 70)
            pygame.draw.rect(screen, bg_color, pill_rect, border_radius=pill_r)
            border_col = (80, 200, 120) if is_on else (100, 85, 110)
            pygame.draw.rect(screen, border_col, pill_rect, max(1, int(2 * min(scale_x, scale_y))), border_radius=pill_r)
            
            # Sliding circle
            circle_r = max(3, pill_h // 2 - max(2, int(3 * scale_y)))
            if is_on:
                cx = pill_rect.right - circle_r - max(2, int(4 * scale_x))
                cc = (180, 255, 200)
            else:
                cx = pill_rect.left + circle_r + max(2, int(4 * scale_x))
                cc = (140, 130, 150)
            pygame.draw.circle(screen, cc, (cx, pill_rect.centery), circle_r)
        
        # ── Preview (right side, label above box with gap) ──
        preview_w = int(140 * scale_x)
        preview_h = int(70 * scale_y)
        preview_x = actual_width - preview_w - int(30 * scale_x)
        preview_label = font_small.render("Preview:", True, UI_COLOR)
        preview_label_y = outline_scaled.top
        screen.blit(preview_label, (preview_x, preview_label_y))
        preview_box_y = preview_label_y + preview_label.get_height() + int(6 * scale_y)
        preview_bg = pygame.Rect(preview_x, preview_box_y, preview_w, preview_h)
        pygame.draw.rect(screen, (20, 22, 38), preview_bg, border_radius=max(1, int(6 * min(scale_x, scale_y))))
        pygame.draw.rect(screen, (70, 75, 100), preview_bg, max(1, int(2 * min(scale_x, scale_y))), border_radius=max(1, int(6 * min(scale_x, scale_y))))
        preview_color = CROSSHAIR_COLORS.get(self.selected_crosshair_color, CROSSHAIR_COLOR)
        # Preview crosshair needs base coords for centering
        draw_crosshair(screen, (preview_bg.centerx / scale_x, preview_bg.centery / scale_y),
                       self.crosshair_size_slider.get_value(),
                       preview_color,
                       int(self.crosshair_thickness_slider.get_value()),
                       int(self.crosshair_gap_slider.get_value()),
                       int(self.crosshair_length_slider.get_value()),
                       self.crosshair_outline,
                       self.crosshair_dot,
                       int(self.crosshair_dot_size_slider.get_value()),
                       scale_x, scale_y)
        
        # Color selection
        color_y = int((self.CONTENT_TOP + self._ch_color_label_offset - self.scroll_y) * scale_y)
        color_label = font_small.render("Color:", True, UI_COLOR)
        screen.blit(color_label, color_label.get_rect(center=(actual_width // 2, color_y)))
        for box in self.color_boxes:
            scaled_box = pygame.Rect(
                int(box['rect'].x * scale_x),
                int(box['rect'].y * scale_y),
                int(box['rect'].width * scale_x),
                int(box['rect'].height * scale_y)
            )
            pygame.draw.rect(screen, box['color'], scaled_box)
            border_w = max(1, int(3 * (scale_x + scale_y) / 2)) if box['name'] == self.selected_crosshair_color else 1
            border_c = WHITE if box['name'] == self.selected_crosshair_color else (80, 80, 80)
            pygame.draw.rect(screen, border_c, scaled_box, border_w)
