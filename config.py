"""
Configuration file for Aim Trainer
Contains all game constants, colors, and settings
"""

# -----------------------------
# Screen Configuration
# -----------------------------
# Base resolution (reference for scaling)
BASE_WIDTH = 800
BASE_HEIGHT = 600
# Default screen size (can be resized)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# -----------------------------
# Game States
# -----------------------------
STATE_MENU = 0
STATE_INSTRUCTION = 1
STATE_SETTINGS = 2
STATE_DIFFICULTY = 3
STATE_COUNTDOWN = 4
STATE_PLAYING = 5
STATE_GAME_OVER = 6
STATE_PAUSE = 7
STATE_MODE_SELECT = 8

# -----------------------------
# Game Modes
# -----------------------------
MODE_CLASSIC = 'CLASSIC'
MODE_TRACKING = 'TRACKING'

# -----------------------------
# Game Timing
# -----------------------------
GAME_DURATION = 60000  # ms
COUNTDOWN_DURATION = 3000  # 3 seconds countdown

# -----------------------------
# Target Configuration
# -----------------------------
TARGET_SIZE_SMALL = 20
TARGET_SIZE_MEDIUM = 35
TARGET_SIZE_LARGE = 50
TARGET_SIZE_START = 50  # Starting size for progression

# Safe spawn margins
MARGIN = 80

# Target timing (will be overridden by difficulty)
TARGET_MIN_LIFETIME = 1200    # ms
TARGET_MAX_LIFETIME = 2000    # ms
SPAWN_DELAY = 500              # ms between spawns
MAX_TARGETS = 1                # 1 target at a time (MVP)

# -----------------------------
# Difficulty Settings
# -----------------------------
DIFFICULTIES = {
    'EASY': {
        'min_lifetime': 2000,
        'max_lifetime': 3000,
        'spawn_delay': 200,
        'max_targets': 1
    },
    'MEDIUM': {
        'min_lifetime': 1200,
        'max_lifetime': 2000,
        'spawn_delay': 150,
        'max_targets': 1
    },
    'HARD': {
        'min_lifetime': 800,
        'max_lifetime': 1500,
        'spawn_delay': 100,
        'max_targets': 1
    }
}

# -----------------------------
# Colors (Modern Aimlab Style)
# -----------------------------
BACKGROUND_START = (15, 20, 35)        # Dark blue gradient start
BACKGROUND_END = (25, 15, 45)          # Purple gradient end
TARGET_PRIMARY = (255, 70, 90)         # Bright red target
TARGET_SECONDARY = (255, 120, 140)     # Lighter red ring
TARGET_CENTER = (255, 255, 255)        # White center dot
CROSSHAIR_COLOR = (0, 255, 200)        # Cyan crosshair (default)
HIT_EFFECT_COLOR = (100, 255, 150)     # Green hit effect
MISS_EFFECT_COLOR = (255, 80, 80)      # Red miss effect
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
UI_COLOR = (150, 200, 255)             # Blue UI text
ACCENT_COLOR = (255, 180, 50)          # Orange accent
SCORE_COLOR = (100, 255, 150)          # Green for score

# -----------------------------
# Customization Options
# -----------------------------
CROSSHAIR_COLORS = {
    'Cyan': (0, 255, 200),
    'Green': (100, 255, 100),
    'Red': (255, 100, 100),
    'White': (255, 255, 255),
    'Purple': (200, 100, 255),
    'Yellow': (255, 255, 100)
}

RESOLUTIONS = ['800x600', '1024x768', '1280x720', '1366x768', '1600x900', '1920x1080']

# -----------------------------
# Scoring
# -----------------------------
BASE_POINTS = 100
BONUS_CAP = 50

# -----------------------------
# Combo System
# -----------------------------
COMBO_MULTIPLIER_STEP = 0.1    # +0.1x per consecutive hit
COMBO_MULTIPLIER_MAX = 2.0     # Max 2.0x multiplier

# -----------------------------
# Tracking Mode
# -----------------------------
TRACKING_TARGET_RADIUS = 40
TRACKING_SCORE_PER_SECOND = 100   # Points per second on target
TRACKING_CHECK_INTERVAL = 50      # ms between on-target checks
TRACKING_HIT_COLOR = (100, 255, 150)   # Green glow when on target
TRACKING_MISS_COLOR = (255, 80, 80)    # Red glow when off target

# 3-phase speed progression (game time split into 3 equal segments)
TRACKING_PHASE_SPEEDS = [0.2, 0.5, 0.8]   # Speed multiplier per phase
