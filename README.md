# 🎯 Aim Trainer — Assignment 1

**Game Programming Course — SEM252**

An **Aimlab-style** aim trainer game built with **Python and Pygame** to practice reflexes, mouse accuracy, and reaction time.

---

## 📋 Table of Contents

- [Game Overview](#-game-overview)
- [How to Run](#️-how-to-run)
- [Controls](#-controls)
- [Game Rules](#-game-rules)
- [Scoring System](#-scoring-system)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Asset Sources](#-asset-sources)

---

## 🎮 Game Overview

**Aim Trainer** is a reaction-time training game with two modes:

- **Classic Mode**: Targets spawn randomly — click them before they vanish
- **Tracking Mode**: A target moves along smooth Bezier curves — keep your crosshair on it

### Core Gameplay Loop (Classic):
1. Targets spawn one at a time at random positions
2. Each target has a **time-to-live (TTL)** before it expires
3. Player clicks to hit targets → earns score based on reaction time
4. Consecutive hits build a **Combo** multiplier (up to 2.0x)
5. Missing a click or letting targets expire counts as a **miss** and resets combo
6. Game runs for **60 seconds** (configurable in settings)
7. Final results show performance metrics and accuracy records

### Core Gameplay Loop (Tracking):
1. A target moves along Bezier curves on screen
2. Player keeps crosshair inside the target radius
3. Speed increases in 3 phases: Slow → Medium → Fast
4. Score accumulates based on time spent on-target
5. Game runs for the configured duration
6. Results show on-target accuracy and time stats

---

## 🖥️ Requirements

- **Python 3.8+**
- **Pygame 2.0+**

Install dependencies:

```bash
pip install pygame
```

---

## ▶️ How to Run

1. Clone or download the project
2. Open terminal in the project directory
3. Run the main file:

```bash
python aimlab.py
```

---

## 🕹 Controls

| Action              | Input            |
| ------------------- | ---------------- |
| Shoot target        | Left Mouse Click |
| Pause game          | ESC              |
| Navigate menus      | Mouse            |
| Adjust settings     | Click sliders    |
| Resume from pause   | Continue button or ESC |

---

## 📖 Game Rules

### Target Mechanics
- **Spawn Position**: Targets spawn at random `(x, y)` where `MARGIN < x < SCREEN_WIDTH - MARGIN` and `MARGIN < y < SCREEN_HEIGHT - MARGIN` to ensure full visibility
- **Target Radius**: Varies based on difficulty progression (starts at 50px, shrinks to 20px)
- **Target Lifetime (TTL)**: Duration before target expires (varies by difficulty: 800ms–3000ms)
- **Hit Detection**: Uses circular collision detection with distance formula: `distance = sqrt((mx - tx)² + (my - ty)²)`
  - If `distance <= radius` → HIT
  - Otherwise → MISS

### Difficulty Progression
The game becomes progressively harder over time:

| Progression | Target Size | Target Lifetime |
|-------------|-------------|-----------------|
| 0–50%       | 50px → 35px | Full TTL → 70% TTL |
| 50–100%     | 35px → 20px | 70% TTL → 70% TTL |

### Difficulty Levels (Classic Mode)

| Difficulty | Max Targets | Target Lifetime | Spawn Delay |
| ---------- | ----------- | --------------- | ----------- |
| **Easy**   | 1           | 2000–3000 ms    | 200 ms      |
| **Medium** | 1           | 1200–2000 ms    | 150 ms      |
| **Hard**   | 1           | 800–1500 ms     | 100 ms      |

> Note: Only 1 target at a time (MVP requirement). Difficulty affects target lifetime only.

### Tracking Mode Phases

| Phase | Label  | Speed Multiplier | Duration        |
|-------|--------|------------------|-----------------|
| 1     | Slow   | 0.2x             | 1/3 of game time |
| 2     | Medium | 0.5x             | 1/3 of game time |
| 3     | Fast   | 1.0x             | 1/3 of game time |

### Performance Metrics
- **Hits**: Successful target clicks
- **Misses**: Missed clicks or timeout expirations
- **Accuracy**: `(Hits / (Hits + Misses)) × 100%`
- **Reaction Time**: Time from target spawn to click (in milliseconds)
- **Average Reaction**: Mean of all reaction times
- **Best Reaction**: Fastest reaction time in the session

---

## 🎯 Scoring System

### Scoring Formula (Classic Mode)
```python
combo_mult = min(2.0, 1.0 + (combo - 1) * 0.1)  # Up to 2.0x
score += int((100 + int(max(0, TTL - reaction_time) / TTL * 50)) * combo_mult)
```

### Breakdown:
- **Base Points**: 100 points per hit
- **Reflex Bonus**: Up to +50 points based on reaction speed
  - Formula: `bonus = (TTL - reaction_time) / TTL × 50`
  - Faster reactions = higher bonus
  - Maximum bonus: 50 points (instant click)
  - Minimum bonus: 0 points (click near timeout)
- **Combo Multiplier**: Consecutive hits increase multiplier by +0.1x (max 2.0x)
  - 1 hit: 1.0x, 2 hits: 1.1x, 3 hits: 1.2x, ... 11+ hits: 2.0x
  - Miss (click miss or timeout) resets combo to 0

### Example:
- Target TTL: 2000ms, Reaction time: 500ms, Combo: 5x (1.4x mult)
- Base: 100
- Bonus: `(2000 - 500) / 2000 × 50 = 37.5` → 37 points
- Combo: `(100 + 37) × 1.4 = 191.8` → **191 points**

---

## 📊 Features

### Core Features (MVP)
- [x] **Main Menu**: Start Game, Instructions, Settings, Exit
- [x] **Mode Selection**: Classic (click targets) and Tracking (follow moving target)
- [x] **Difficulty Selection**: Easy, Medium, Hard
- [x] **Countdown Screen**: 3-2-1 countdown before gameplay
- [x] **Gameplay Screen**: 
  - Real-time target spawning/despawning
  - Circular hit detection
  - Custom crosshair cursor
  - Live HUD (timer, score, hits, misses, accuracy, reaction times, combo)
- [x] **Pause System**: ESC to pause, resume, or access settings mid-game
- [x] **Results Screen**: Final stats with accuracy records
- [x] **Game States**: Menu → Mode Select → Difficulty/Countdown → Playing → Pause/Game Over (9 states)

### Bonus Features
- [x] **Combo System**: Consecutive hits increase score multiplier (up to 2.0x), miss resets
- [x] **Tracking Mode**: A moving target follows smooth Bezier curves; player must keep crosshair on it. 3-phase speed progression (Slow → Medium → Fast). Skips difficulty selection — goes straight to countdown. Score based on time-on-target %.
- [x] **Persistent Records**: Best accuracy saved per difficulty per mode in `records.json`
- [x] **Settings Menu**:
  - Mouse sensitivity adjustment (0.1–2.0x)
  - Game duration (30–120 seconds)
  - Sound volume control
  - Crosshair customization (size, color, thickness, gap, length, dot, outline)
  - Pill-style toggle switches for Outline/Dot options
  - Live crosshair preview panel
  - Scrollable crosshair tab with scrollbar indicator
- [x] **Mouse Lock**: Cursor locked to window during gameplay
- [x] **Window Resize Support**: Virtual screen scaling with smooth rendering
- [x] **Visual Feedback**: Hit/miss effects with floating score text and combo indicators
- [x] **Audio Feedback**: Procedural hit/miss/click/countdown sounds + BGM

### Settings Return Logic
- Settings opened from Menu → returns to Menu
- Settings opened from Pause → returns to Pause (preserves game state)

---

## 📁 Project Structure

```
Ass1/
├── aimlab.py                 # Main game loop, state manager
├── config.py                 # Constants, colors, difficulty settings
├── README.md                 # This file
├── records.json              # Persistent accuracy records
├── settings.json             # User preferences
├── classes/
│   ├── __init__.py
│   ├── button.py             # Button UI class
│   ├── slider.py             # Slider control for settings
│   ├── target.py             # Target spawn/hit/draw logic
│   └── particle.py           # Background particle effects
├── screens/
│   ├── __init__.py
│   ├── menu.py               # Main menu screen
│   ├── mode_select.py        # Game mode selection (Classic/Tracking)
│   ├── instruction.py        # How to play guide
│   ├── settings_screen.py    # Settings with tabs (General/Crosshair)
│   ├── difficulty.py         # Difficulty selection
│   ├── countdown.py          # 3-2-1 countdown
│   ├── playing.py            # Classic gameplay loop (with combo)
│   ├── tracking.py           # Tracking mode gameplay
│   ├── game_over.py          # Results display
│   └── pause.py              # Pause overlay
└── utils/
    ├── __init__.py
    ├── drawing.py            # Drawing utilities (crosshair, effects)
    ├── file_manager.py       # JSON save/load
    ├── game_helpers.py       # Spawn position, collision helpers
    └── sound_manager.py      # Procedural audio generation
```

---

## 🎨 Asset Sources

**All assets are procedurally generated — no external files are used.**

### Graphics
- **Targets**: Drawn using `pygame.draw.circle()` with multi-layered rings and pulsing glow effect
- **Crosshair**: Custom rendering with `pygame.Rect` for pixel-perfect centering
- **UI Elements**: Buttons, sliders, and text rendered with Pygame primitives
- **Effects**: Hit markers (X shape) and miss indicators (red circle) drawn procedurally
- **Background**: Gradient fill with animated particles using trigonometric functions

### Audio
- **Hit Sound**: Generated using a sine wave algorithm:
  ```python
  [int(128 + 127 * sin(2π × 440 × i / 22050)) for i in range(2205)]
  ```
  This creates a 100ms beep at 440Hz (A4 note)

### Fonts
- **System fonts**: Arial (fallback to pygame default)
- Font sizes: 80px (title), 64px (large), 32px (normal), 24px (small)

---

## 🧪 Technical Implementation

### Game Loop Architecture
- **Fixed FPS**: 60 FPS using `pygame.time.Clock()`
- **Virtual Screen**: Fixed 800×600 resolution scaled to display size using `pygame.transform.smoothscale()`
- **State Machine**: 9 states (Menu, Instruction, Settings, Difficulty, Countdown, Playing, Game Over, Pause, Mode Select)
- **Mouse Sensitivity**: Custom cursor with relative mouse movement (`pygame.mouse.get_rel()`) multiplied by sensitivity factor

### Hit Detection Algorithm
```python
distance = math.hypot(mouse_x - target_x, mouse_y - target_y)
is_hit = distance <= target_radius
```

### Spawn Position Algorithm
```python
x = random.randint(MARGIN, SCREEN_WIDTH - MARGIN)
y = random.randint(MARGIN, SCREEN_HEIGHT - MARGIN)
# Validates no overlap with existing targets (80px minimum spacing)
```


---

## Project Team

**Project owner / contacts: Group 11**

**Team:**
- Đỗ Đăng Khoa (Kras2508)
- Nguyễn Minh Hưng
- Nguyễn Phước Quý Bảo
- Nguyễn Nguyên Ngọc

---
