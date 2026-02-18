"""
File management utilities for Aim Trainer
Handles loading and saving of records and settings
"""

import json
import os


def load_records():
    """Load records from file"""
    try:
        if os.path.exists('records.json'):
            with open('records.json', 'r') as f:
                return json.load(f)
    except:
        pass
    return {'EASY': 0.0, 'MEDIUM': 0.0, 'HARD': 0.0}


def save_records(records):
    """Save records to file"""
    try:
        with open('records.json', 'w') as f:
            json.dump(records, f, indent=2)
    except:
        pass


def load_settings():
    """Load settings from file"""
    default_settings = {
        'mouse_sensitivity': 1.0,
        'volume': 0.5,
        'crosshair_size': 1.0,
        'crosshair_color': 'Cyan',
        'crosshair_thickness': 2,
        'crosshair_gap': 5,
        'crosshair_length': 12,
        'crosshair_outline': True,
        'crosshair_dot': True,
        'crosshair_dot_size': 2,
        'game_duration': 60
    }
    try:
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                loaded = json.load(f)
                default_settings.update(loaded)
    except:
        pass
    return default_settings


def save_settings(settings):
    """Save settings to file"""
    try:
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=2)
    except:
        pass
