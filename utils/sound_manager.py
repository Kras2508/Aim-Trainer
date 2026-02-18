"""
Sound Manager - Procedurally generated game sounds and background music
All sounds are created using math (sine waves, noise) — no external audio files needed.
"""

import pygame
import math
import random
import array


SAMPLE_RATE = 22050


def _make_sound(samples):
    """Convert a list of float samples [-1, 1] to a pygame Sound"""
    # Convert to 16-bit signed integers
    int_samples = array.array('h', [int(max(-32767, min(32767, s * 32767))) for s in samples])
    sound = pygame.mixer.Sound(buffer=int_samples)
    return sound


def create_hit_sound():
    """Short satisfying 'pop' sound when hitting a target"""
    duration = 0.12  # seconds
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = max(0, 1 - t / duration)  # linear decay
        env = env ** 2  # faster decay curve
        # Two harmonics for a richer tone
        wave = (0.6 * math.sin(2 * math.pi * 600 * t) +
                0.3 * math.sin(2 * math.pi * 900 * t) +
                0.1 * math.sin(2 * math.pi * 1200 * t))
        samples.append(wave * env * 0.8)
    return _make_sound(samples)


def create_miss_sound():
    """Low 'thud' sound for missed clicks"""
    duration = 0.1
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = max(0, 1 - t / duration) ** 3
        wave = math.sin(2 * math.pi * 150 * t) * 0.5
        # Add a little noise
        wave += (random.random() * 2 - 1) * 0.15 * env
        samples.append(wave * env * 0.6)
    return _make_sound(samples)


def create_click_sound():
    """Short 'click' for UI button presses"""
    duration = 0.05
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = max(0, 1 - t / duration) ** 4
        wave = math.sin(2 * math.pi * 1000 * t) * 0.5
        wave += math.sin(2 * math.pi * 1500 * t) * 0.3
        samples.append(wave * env * 0.5)
    return _make_sound(samples)


def create_countdown_beep():
    """Beep for countdown (3, 2, 1)"""
    duration = 0.15
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = max(0, 1 - t / duration) ** 1.5
        wave = math.sin(2 * math.pi * 800 * t)
        samples.append(wave * env * 0.4)
    return _make_sound(samples)


def create_countdown_go_beep():
    """Higher pitched beep for 'GO!'"""
    duration = 0.25
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = max(0, 1 - t / duration) ** 1.2
        wave = (0.5 * math.sin(2 * math.pi * 1200 * t) +
                0.3 * math.sin(2 * math.pi * 1800 * t))
        samples.append(wave * env * 0.5)
    return _make_sound(samples)


def create_game_over_sound():
    """Short 'game over' jingle"""
    duration = 0.8
    n = int(SAMPLE_RATE * duration)
    # Descending notes: E5 → C5 → A4
    notes = [(659, 0.0, 0.25), (523, 0.25, 0.5), (440, 0.5, 0.8)]
    samples = [0.0] * n
    for freq, start, end in notes:
        for i in range(n):
            t = i / SAMPLE_RATE
            if start <= t <= end:
                local_t = (t - start) / (end - start)
                env = max(0, 1 - local_t) ** 2
                wave = math.sin(2 * math.pi * freq * t) * env * 0.35
                samples[i] += wave
    return _make_sound(samples)


def generate_bgm_buffer():
    """Generate a short ambient background music loop (8 seconds).
    Uses layered sine waves with chord progressions for a chill vibe."""
    duration = 8.0  # seconds, will loop
    n = int(SAMPLE_RATE * duration)
    samples = [0.0] * n

    # Chord progression: Am → F → C → G (each 2 sec)
    chords = [
        (220, 261.63, 329.63),    # Am: A3, C4, E4
        (174.61, 220, 261.63),    # F:  F3, A3, C4
        (261.63, 329.63, 392),    # C:  C4, E4, G4
        (196, 246.94, 293.66),    # G:  G3, B3, D4
    ]
    chord_len = n // len(chords)

    for ci, chord in enumerate(chords):
        start = ci * chord_len
        end = min(start + chord_len, n)
        for i in range(start, end):
            t = i / SAMPLE_RATE
            # Crossfade envelope for smooth transitions
            local = (i - start) / chord_len
            fade_in = min(1, local * 10) if ci > 0 else min(1, local * 5)
            fade_out = min(1, (1 - local) * 10)
            env = fade_in * fade_out * 0.08  # Keep it quiet

            wave = 0.0
            for freq in chord:
                wave += math.sin(2 * math.pi * freq * t)
                # Add subtle octave below for warmth
                wave += 0.3 * math.sin(2 * math.pi * freq * 0.5 * t)

            # Slow pulsating LFO for movement
            lfo = 0.7 + 0.3 * math.sin(2 * math.pi * 0.5 * t)
            samples[i] += wave * env * lfo

    # Add a soft pad high note
    for i in range(n):
        t = i / SAMPLE_RATE
        pad = 0.02 * math.sin(2 * math.pi * 523.25 * t)  # C5
        pad *= 0.5 + 0.5 * math.sin(2 * math.pi * 0.25 * t)  # slow LFO
        samples[i] += pad

    return _make_sound(samples)


class SoundManager:
    """Manages all game sounds"""

    def __init__(self, volume=0.5):
        self.volume = volume
        self.enabled = True

        try:
            self.hit_sound = create_hit_sound()
            self.miss_sound = create_miss_sound()
            self.click_sound = create_click_sound()
            self.countdown_beep = create_countdown_beep()
            self.countdown_go = create_countdown_go_beep()
            self.game_over_sound = create_game_over_sound()
            self.bgm = generate_bgm_buffer()
        except Exception:
            self.hit_sound = None
            self.miss_sound = None
            self.click_sound = None
            self.countdown_beep = None
            self.countdown_go = None
            self.game_over_sound = None
            self.bgm = None

        self.bgm_playing = False
        self.set_volume(volume)

    def set_volume(self, volume):
        """Set volume for all sound effects"""
        self.volume = volume
        for snd in [self.hit_sound, self.miss_sound, self.click_sound,
                     self.countdown_beep, self.countdown_go, self.game_over_sound]:
            if snd:
                snd.set_volume(volume)
        if self.bgm:
            self.bgm.set_volume(volume * 0.3)  # BGM quieter than SFX

    def play_hit(self):
        if self.enabled and self.hit_sound:
            self.hit_sound.play()

    def play_miss(self):
        if self.enabled and self.miss_sound:
            self.miss_sound.play()

    def play_click(self):
        if self.enabled and self.click_sound:
            self.click_sound.play()

    def play_countdown(self):
        if self.enabled and self.countdown_beep:
            self.countdown_beep.play()

    def play_go(self):
        if self.enabled and self.countdown_go:
            self.countdown_go.play()

    def play_game_over(self):
        if self.enabled and self.game_over_sound:
            self.game_over_sound.play()

    def start_bgm(self):
        """Start looping background music"""
        if self.bgm and not self.bgm_playing:
            self.bgm.play(loops=-1)
            self.bgm_playing = True

    def stop_bgm(self):
        """Stop background music"""
        if self.bgm and self.bgm_playing:
            self.bgm.stop()
            self.bgm_playing = False
