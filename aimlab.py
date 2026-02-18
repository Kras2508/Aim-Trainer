"""
Aim Trainer - Main Game File
A modern aim training game inspired by Aimlab

Project Structure:
- config.py: Game constants and settings
- classes/: Game object classes (Target, Button, Slider, Particle)
- utils/: Helper functions (drawing, file management, game helpers)
- screens/: Screen modules (menu, settings, playing, etc.)
"""

import pygame
import math
import sys

# Import configuration
from config import *

# Import classes
from classes.particle import create_particles

# Import utilities
from utils import (
    load_records, save_records, load_settings, save_settings,
    draw_decorated_background
)
from utils.sound_manager import SoundManager

# Import screens
from screens import (
    MenuScreen, InstructionScreen, SettingsScreen,
    DifficultyScreen, CountdownScreen, PlayingScreen,
    GameOverScreen, PauseScreen
)


def create_fonts(scale=1.0):
    """Create fonts scaled to current resolution"""
    return (
        pygame.font.SysFont("Arial", max(16, int(80 * scale))),   # font_title
        pygame.font.SysFont("Arial", max(14, int(64 * scale))),   # font_large
        pygame.font.SysFont("Arial", max(12, int(32 * scale))),   # font
        pygame.font.SysFont("Arial", max(10, int(24 * scale))),   # font_small
    )


def main():
    """Main game function"""
    pygame.init()
    pygame.mixer.init()

    # Display setup - resizable window
    display_width, display_height = SCREEN_WIDTH, SCREEN_HEIGHT
    display = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
    pygame.display.set_caption("Aim Trainer - Aimlab Style")
    clock = pygame.time.Clock()

    # Calculate scale factor based on display size
    scale_x = display_width / BASE_WIDTH
    scale_y = display_height / BASE_HEIGHT
    scale = min(scale_x, scale_y)  # Uniform scale to maintain aspect ratio

    # Virtual screen at native resolution (no scaling blur)
    screen = pygame.Surface((display_width, display_height))

    # Fonts tuple: (title, large, normal, small) - scaled to resolution
    fonts = create_fonts(scale)

    # Load data
    records = load_records()
    settings = load_settings()
    particles = create_particles(50)

    # Sound manager (all sounds procedurally generated)
    sound_manager = SoundManager(settings['volume'])
    sound_manager.start_bgm()

    # Initialize all screens with scale info
    screen_info = {'scale_x': scale_x, 'scale_y': scale_y, 'scale': scale}
    menu_screen = MenuScreen()
    instruction_screen = InstructionScreen()
    settings_screen = SettingsScreen(settings)
    difficulty_screen = DifficultyScreen()
    countdown_screen = CountdownScreen()
    playing_screen = PlayingScreen()
    game_over_screen = GameOverScreen()
    pause_screen = PauseScreen()

    # Game state
    game_state = STATE_MENU
    selected_difficulty = 'MEDIUM'
    game_duration = settings['game_duration'] * 1000

    # Game data dictionary (shared between screens)
    game_data = {
        'targets': [],
        'hits': 0,
        'misses': 0,
        'score': 0,
        'hit_effects': [],
        'miss_effects': [],
        'reaction_times': [],
        'game_start_time': 0,
        'countdown_start_time': 0,
        'last_spawn_time': 0,
        'current_target_size': TARGET_SIZE_START,
        'game_duration': game_duration,
        'selected_difficulty': selected_difficulty,
        'records': records,
        'sound_manager': sound_manager,
        'current_time': 0,
    }

    def reset_game():
        """Reset game data for a new round"""
        game_data['targets'] = []
        game_data['hits'] = 0
        game_data['misses'] = 0
        game_data['score'] = 0
        game_data['hit_effects'] = []
        game_data['miss_effects'] = []
        game_data['reaction_times'] = []
        game_data['last_spawn_time'] = 0
        game_data['current_target_size'] = TARGET_SIZE_START
        game_data['game_duration'] = settings['game_duration'] * 1000
        now = pygame.time.get_ticks()
        game_data['game_start_time'] = now
        game_data['countdown_start_time'] = now

    # Custom cursor position for sensitivity (in base coords 800x600)
    custom_cx = BASE_WIDTH // 2
    custom_cy = BASE_HEIGHT // 2
    prev_game_state = None

    # ─── Main Loop ───────────────────────────────────────────────
    running = True
    while running:
        dt = clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        game_data['current_time'] = current_time

        # Scale mouse position to base coordinate system (800x600)
        raw_mouse = pygame.mouse.get_pos()
        sx = BASE_WIDTH / display_width
        sy = BASE_HEIGHT / display_height

        # Use sensitivity-based cursor during gameplay
        in_gameplay = game_state in (STATE_PLAYING, STATE_COUNTDOWN)
        if in_gameplay:
            rel = pygame.mouse.get_rel()
            sens = settings.get('mouse_sensitivity', 1.0)
            custom_cx += rel[0] * sx * sens
            custom_cy += rel[1] * sy * sens
            # Clamp to base screen
            custom_cx = max(0, min(BASE_WIDTH, custom_cx))
            custom_cy = max(0, min(BASE_HEIGHT, custom_cy))
            mouse_pos = (int(custom_cx), int(custom_cy))
        else:
            mouse_pos = (int(raw_mouse[0] * sx), int(raw_mouse[1] * sy))

        # When entering gameplay, reset cursor to center and consume pending rel
        if in_gameplay and prev_game_state not in (STATE_PLAYING, STATE_COUNTDOWN):
            custom_cx = BASE_WIDTH // 2
            custom_cy = BASE_HEIGHT // 2
            pygame.mouse.get_rel()  # consume stale delta
            pygame.event.set_grab(True)  # lock mouse inside window
        elif not in_gameplay and prev_game_state in (STATE_PLAYING, STATE_COUNTDOWN):
            pygame.event.set_grab(False)  # release mouse
        prev_game_state = game_state

        # ─── Event handling ──────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.VIDEORESIZE:
                display_width, display_height = event.w, event.h
                display = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
                # Recreate screen at native resolution
                screen = pygame.Surface((display_width, display_height))
                # Recalculate scale and recreate fonts
                scale_x = display_width / BASE_WIDTH
                scale_y = display_height / BASE_HEIGHT
                scale = min(scale_x, scale_y)
                fonts = create_fonts(scale)
                screen_info = {'scale_x': scale_x, 'scale_y': scale_y, 'scale': scale}
                continue

            # Dispatch event to current screen
            if game_state == STATE_MENU:
                result = menu_screen.handle_events(event, mouse_pos)
                if result == 'QUIT':
                    running = False
                elif result is not None:
                    sound_manager.play_click()
                    game_state = result

            elif game_state == STATE_INSTRUCTION:
                result = instruction_screen.handle_events(event, mouse_pos)
                if result is not None:
                    sound_manager.play_click()
                    game_state = result

            elif game_state == STATE_SETTINGS:
                result = settings_screen.handle_events(event, mouse_pos, settings, save_settings, sound_manager)
                if result is not None:
                    sound_manager.play_click()
                    game_state = result
                    settings_screen.return_state = STATE_MENU  # reset for next time

            elif game_state == STATE_DIFFICULTY:
                result = difficulty_screen.handle_events(event, mouse_pos)
                if result is not None:
                    sound_manager.play_click()
                    new_state, difficulty = result
                    if difficulty is not None:
                        selected_difficulty = difficulty
                        game_data['selected_difficulty'] = selected_difficulty
                        reset_game()
                        pygame.mouse.set_visible(False)
                    game_state = new_state

            elif game_state == STATE_COUNTDOWN:
                result = countdown_screen.handle_events(event)
                if result is not None:
                    game_state = result

            elif game_state == STATE_PLAYING:
                result = playing_screen.handle_events(event, mouse_pos, game_data)
                if result is not None:
                    if result == STATE_PAUSE:
                        # Warp OS mouse to match custom cursor pos on unpause
                        pygame.mouse.set_pos(int(custom_cx / sx), int(custom_cy / sy))
                    game_state = result

            elif game_state == STATE_GAME_OVER:
                result = game_over_screen.handle_events(event, mouse_pos)
                if result is not None:
                    sound_manager.play_click()
                    game_state = result

            elif game_state == STATE_PAUSE:
                result = pause_screen.handle_events(event, mouse_pos)
                if result is not None:
                    sound_manager.play_click()
                    if result == STATE_SETTINGS:
                        settings_screen.return_state = STATE_PAUSE
                    game_state = result

        # ─── Update ─────────────────────────────────────────────
        if game_state == STATE_MENU:
            menu_screen.update(mouse_pos)
        elif game_state == STATE_INSTRUCTION:
            instruction_screen.update(mouse_pos)
        elif game_state == STATE_SETTINGS:
            settings_screen.update(mouse_pos)
        elif game_state == STATE_DIFFICULTY:
            difficulty_screen.update(mouse_pos)
        elif game_state == STATE_COUNTDOWN:
            if countdown_screen.update(current_time, game_data['countdown_start_time'], sound_manager):
                sound_manager.play_go()
                game_state = STATE_PLAYING
                game_data['game_start_time'] = current_time
        elif game_state == STATE_PLAYING:
            result = playing_screen.update(current_time, game_data, settings)
            if result is not None:
                if result == STATE_GAME_OVER:
                    sound_manager.play_game_over()
                game_state = result
        elif game_state == STATE_GAME_OVER:
            game_over_screen.update(mouse_pos)
        elif game_state == STATE_PAUSE:
            pause_screen.update(mouse_pos)

        # ─── Draw ───────────────────────────────────────────────
        draw_decorated_background(screen, particles, current_time, scale_x, scale_y)

        if game_state == STATE_MENU:
            menu_screen.draw(screen, fonts, scale_x, scale_y)
        elif game_state == STATE_INSTRUCTION:
            instruction_screen.draw(screen, fonts, settings['game_duration'], scale_x, scale_y)
        elif game_state == STATE_SETTINGS:
            settings_screen.draw(screen, fonts, scale_x, scale_y)
        elif game_state == STATE_DIFFICULTY:
            difficulty_screen.draw(screen, fonts, scale_x, scale_y)
        elif game_state == STATE_COUNTDOWN:
            countdown_screen.draw(screen, fonts, current_time, game_data['countdown_start_time'], selected_difficulty, scale_x, scale_y)
        elif game_state == STATE_PLAYING:
            playing_screen.draw(screen, fonts, mouse_pos, current_time, game_data, settings, scale_x, scale_y)
        elif game_state == STATE_GAME_OVER:
            game_over_screen.draw(screen, fonts, game_data, scale_x, scale_y)
        elif game_state == STATE_PAUSE:
            pause_screen.draw(screen, fonts, scale_x, scale_y)

        # ─── Present (native resolution - no scaling needed) ────
        display.blit(screen, (0, 0))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
