"""
Screens package for Aim Trainer
Each screen is a separate module with handle_events, update, and draw functions
"""

from .menu import MenuScreen
from .instruction import InstructionScreen
from .settings_screen import SettingsScreen
from .difficulty import DifficultyScreen
from .countdown import CountdownScreen
from .playing import PlayingScreen
from .game_over import GameOverScreen
from .pause import PauseScreen
from .mode_select import ModeSelectScreen
from .tracking import TrackingScreen

__all__ = [
    'MenuScreen', 'InstructionScreen', 'SettingsScreen',
    'DifficultyScreen', 'CountdownScreen', 'PlayingScreen',
    'GameOverScreen', 'PauseScreen', 'ModeSelectScreen', 'TrackingScreen'
]
