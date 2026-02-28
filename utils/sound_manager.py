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
    """Generate an intense/upbeat background music loop (8 seconds).
    Procedural: kick + hats + pulsing bass + fast arp lead."""
    duration = 8.0
    n = int(SAMPLE_RATE * duration)
    samples = [0.0] * n

    bpm = 150
    beat = 60.0 / bpm              # seconds per beat
    step = beat / 4.0              # 16th-note step
    steps_per_loop = int(duration / step)

    # Minor-ish tense scale (A minor / A aeolian)
    scale = [220.00, 246.94, 261.63, 293.66, 329.63, 349.23, 392.00, 440.00]  # A3..A4

    def soft_clip(x):
        # Simple saturation to avoid harsh clipping
        return max(-1.0, min(1.0, x * 0.8))

    for i in range(n):
        t = i / SAMPLE_RATE

        # ---- Rhythm grid ----
        s = int(t / step) % steps_per_loop          # 16th index
        within = (t % step) / step                  # 0..1 inside step
        beat_idx = int(t / beat) % int(duration / beat)

        out = 0.0

        # ---- Kick (on 1 and 3, plus a few extra for drive) ----
        kick_hit = (s % 16 == 0) or (s % 16 == 8) or (s % 32 == 20)
        if kick_hit:
            # Exponential decay envelope within the step
            env = math.exp(-within * 12.0)
            # Pitch drop for punch: 110 -> 55 Hz
            freq = 110.0 - 55.0 * within
            out += math.sin(2 * math.pi * freq * t) * env * 0.55
            # Add a tiny click transient
            out += (random.random() * 2 - 1) * env * 0.06

        # ---- Hi-hat (noise on every 16th; stronger on offbeats) ----
        hat_env = math.exp(-within * 18.0)
        hat_amp = 0.10 if (s % 4 != 0) else 0.06  # emphasize offbeats
        out += (random.random() * 2 - 1) * hat_env * hat_amp

        # ---- Snare/Clap (on 2 and 4) ----
        snare_hit = (s % 16 == 4) or (s % 16 == 12)
        if snare_hit:
            env = math.exp(-within * 10.0)
            noise = (random.random() * 2 - 1)
            tone = math.sin(2 * math.pi * 200.0 * t)
            out += (0.8 * noise + 0.2 * tone) * env * 0.22

        # ---- Pulsing bass (sidechain-ish duck with kick feel) ----
        # Bass note changes every 2 beats for motion
        bass_note = [220.0, 196.0, 246.94, 174.61]  # A3, G3, B3, F3-ish tension
        bass = bass_note[(beat_idx // 2) % len(bass_note)]

        # Bass gate (8th-note) + subtle wobble
        bass_gate = 0.35 + 0.65 * (1 if (s % 8 < 4) else 0)
        wobble = 0.85 + 0.15 * math.sin(2 * math.pi * 6.0 * t)
        bass_env = bass_gate * wobble

        # Sidechain style duck right after kick
        duck = 1.0 - 0.5 * math.exp(-((t % beat) / beat) * 8.0)
        bass_wave = math.sin(2 * math.pi * bass * t) + 0.35 * math.sin(2 * math.pi * bass * 2 * t)
        out += bass_wave * bass_env * duck * 0.14

        # ---- Fast arp lead (16th notes) ----
        # Pattern picks notes from the scale; jumps add urgency
        arp_pattern = [0, 2, 4, 2, 5, 4, 2, 6]
        note = scale[arp_pattern[s % len(arp_pattern)]]
        lead_env = math.exp(-within * 9.0)
        lead = math.sin(2 * math.pi * note * 2.0 * t)  # octave up
        lead += 0.3 * math.sin(2 * math.pi * note * 4.0 * t)  # shimmer harmonic
        out += lead * lead_env * 0.10

        # ---- Master level + saturation ----
        samples[i] = soft_clip(out)

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
