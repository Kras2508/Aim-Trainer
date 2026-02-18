# 📖 TÀI LIỆU MÔ TẢ CHI TIẾT - AIM TRAINER GAME

## Mục lục
1. [Tổng quan game](#1-tổng-quan-game)
2. [Cấu trúc dự án](#2-cấu-trúc-dự-án)
3. [Các màn hình (Screens)](#3-các-màn-hình-screens)
4. [Hệ thống tính điểm](#4-hệ-thống-tính-điểm)
5. [Hệ thống độ khó](#5-hệ-thống-độ-khó)
6. [Cơ chế gameplay](#6-cơ-chế-gameplay)
7. [Hệ thống cài đặt (Settings)](#7-hệ-thống-cài-đặt-settings)
8. [Hệ thống âm thanh](#8-hệ-thống-âm-thanh)
9. [Hệ thống đồ họa & hiệu ứng](#9-hệ-thống-đồ-họa--hiệu-ứng)
10. [Lưu trữ dữ liệu](#10-lưu-trữ-dữ-liệu)
11. [Kiến trúc kỹ thuật](#11-kiến-trúc-kỹ-thuật)

---

## 1. Tổng quan game

**Aim Trainer** là một game luyện tập ngắm bắn (aim training) lấy cảm hứng từ Aimlab, được xây dựng bằng **Python** và thư viện **Pygame**.

**Mục tiêu**: Người chơi cần click chuột vào các mục tiêu (target) xuất hiện ngẫu nhiên trên màn hình trước khi chúng biến mất. Click càng nhanh và chính xác càng được nhiều điểm.

**Vòng lặp gameplay chính**:
1. Chọn độ khó → Đếm ngược 3-2-1 → Bắt đầu chơi
2. Target xuất hiện ngẫu nhiên trên màn hình
3. Người chơi click chuột trái để bắn target
4. Mỗi target có thời gian tồn tại (TTL) giới hạn — hết thời gian sẽ biến mất và tính là miss
5. Click trúng = Hit (được điểm), click trượt hoặc target hết hạn = Miss
6. Game kết thúc sau thời gian quy định (mặc định 60 giây)
7. Hiển thị kết quả chi tiết

---

## 2. Cấu trúc dự án

```
Ass1/
├── aimlab.py                 # File chính — vòng lặp game, quản lý state
├── config.py                 # Hằng số, màu sắc, cài đặt độ khó
├── records.json              # Lưu kỷ lục accuracy theo từng độ khó
├── settings.json             # Lưu cài đặt người dùng
│
├── classes/                  # Các class đối tượng game
│   ├── target.py             # Lớp Target (mục tiêu bắn)
│   ├── button.py             # Lớp Button (nút bấm UI)
│   ├── slider.py             # Lớp Slider (thanh trượt cài đặt)
│   └── particle.py           # Lớp Particle (hiệu ứng hạt nền)
│
├── screens/                  # Các màn hình
│   ├── menu.py               # Màn hình chính (Menu)
│   ├── instruction.py        # Hướng dẫn chơi
│   ├── settings_screen.py    # Cài đặt (2 tab: General & Crosshair)
│   ├── difficulty.py         # Chọn độ khó
│   ├── countdown.py          # Đếm ngược 3-2-1-GO!
│   ├── playing.py            # Màn hình chơi chính
│   ├── game_over.py          # Hiển thị kết quả
│   └── pause.py              # Tạm dừng game
│
└── utils/                    # Tiện ích
    ├── drawing.py            # Vẽ crosshair, hiệu ứng hit/miss, gradient
    ├── file_manager.py       # Đọc/ghi file JSON (records, settings)
    ├── game_helpers.py       # Tạo vị trí spawn, kích thước target
    └── sound_manager.py      # Quản lý âm thanh (tạo bằng thuật toán)
```

---

## 3. Các màn hình (Screens)

Game sử dụng **State Machine** với 8 trạng thái:

### 3.1. Menu chính (STATE_MENU = 0)
- **File**: `screens/menu.py`
- **Hiển thị**: Tiêu đề "AIM TRAINER", phụ đề "Train Your Reflexes"
- **4 nút bấm**:
  - `START GAME` → Chuyển sang màn chọn độ khó
  - `INSTRUCTIONS` → Xem hướng dẫn chơi
  - `SETTINGS` → Mở cài đặt
  - `QUIT` → Thoát game
- Các nút có hiệu ứng hover (đổi màu khi di chuột lên)

### 3.2. Hướng dẫn chơi (STATE_INSTRUCTION = 1)
- **File**: `screens/instruction.py`
- **Nội dung hiển thị**:
  - Cách chơi: Click vào target trước khi chúng biến mất
  - Thời lượng game (hiển thị giá trị hiện tại từ settings)
  - Target nhỏ dần và nhanh hơn theo thời gian
  - Hệ thống tính điểm: Base 100 + Bonus lên đến 50
  - Điều khiển: Left Click = bắn, ESC = tạm dừng
- **Nút**: `BACK` → Quay lại Menu

### 3.3. Cài đặt (STATE_SETTINGS = 2)
- **File**: `screens/settings_screen.py`
- **Giao diện tab**: 2 tab — General và Crosshair
- **Chi tiết ở mục 7**
- **Nút**: `BACK` (quay lại), `SAVE & APPLY` (lưu cài đặt)
- **Logic quay lại thông minh**: Mở từ Menu → về Menu; Mở từ Pause → về Pause

### 3.4. Chọn độ khó (STATE_DIFFICULTY = 3)
- **File**: `screens/difficulty.py`
- **3 nút chọn**:
  - `EASY` (màu xanh lá)
  - `MEDIUM` (màu vàng cam)
  - `HARD` (màu đỏ)
- **Nút**: `BACK` → Quay lại Menu
- Sau khi chọn → chuyển sang đếm ngược

### 3.5. Đếm ngược (STATE_COUNTDOWN = 4)
- **File**: `screens/countdown.py`
- Hiển thị lần lượt: **3** (đỏ) → **2** (vàng) → **1** (xanh) → **GO!** (xanh lá)
- Mỗi số kéo dài 1 giây (tổng 3 giây)
- Phát âm thanh beep cho mỗi số; âm thanh "GO!" khác biệt
- Hiển thị tên độ khó đã chọn
- Nhấn ESC để hủy và quay lại chọn độ khó
- Con trỏ chuột bị ẩn, chuột bị khóa trong cửa sổ

### 3.6. Màn hình chơi (STATE_PLAYING = 5)
- **File**: `screens/playing.py`
- **Đây là màn hình gameplay chính**, bao gồm:

#### Target (Mục tiêu):
- Xuất hiện ngẫu nhiên trên màn hình
- Có hiệu ứng phát sáng (glow) và nhấp nháy (pulsing)
- Vòng cảnh báo màu cam khi sắp hết hạn (30% cuối thời gian sống)
- Thiết kế nhiều lớp: vòng ngoài phát sáng → vòng chính đỏ → vòng trong hồng → tâm trắng → chấm đỏ

#### HUD (Heads-Up Display):
- **Timer**: Thời gian còn lại (giữa trên), chuyển đỏ khi còn <10 giây
- **Score**: Tổng điểm (góc phải trên)
- **Bảng thống kê trái**:
  - `DIFFICULTY`: Độ khó hiện tại
  - `HITS`: Số lần bắn trúng
  - `MISSES`: Số lần bắn trượt
  - `ACCURACY`: Độ chính xác (%)
  - `AVG`: Thời gian phản xạ trung bình (ms)
  - `BEST`: Thời gian phản xạ nhanh nhất (ms)
- Gợi ý "Press ESC to pause" (góc phải dưới)

#### Hiệu ứng:
- **Hit**: Vòng tròn xanh mở rộng + chữ "+điểm" bay lên (kéo dài 400ms)
- **Miss**: Dấu X đỏ (kéo dài 300ms)

#### Crosshair:
- Con trỏ chuột tùy biến thay vì con trỏ hệ thống
- Kiểu dáng giống Valorant/CS:GO
- Tùy chỉnh đầy đủ (size, color, thickness, gap, length, dot, outline)

### 3.7. Kết quả (STATE_GAME_OVER = 6)
- **File**: `screens/game_over.py`
- **Hiển thị**:
  - Tiêu đề "RESULTS"
  - Tổng điểm (số lớn màu xanh lá)
  - Thống kê chi tiết: Difficulty, Hits, Misses, Accuracy, Avg Reaction, Best Reaction
  - Nếu accuracy cao hơn kỷ lục cũ → hiện **"NEW RECORD!"**
  - Nếu không → hiện kỷ lục hiện tại
- **2 nút**:
  - `PLAY AGAIN` → Quay lại chọn độ khó
  - `MAIN MENU` → Quay lại Menu

### 3.8. Tạm dừng (STATE_PAUSE = 7)
- **File**: `screens/pause.py`
- **Overlay tối** (alpha 180/255) phủ lên màn hình game
- **3 nút**:
  - `CONTINUE` → Tiếp tục chơi
  - `SETTINGS` → Mở cài đặt (nhớ trạng thái game)
  - `QUIT TO MENU` → Bỏ cuộc, về Menu
- Nhấn ESC cũng tiếp tục chơi

---

## 4. Hệ thống tính điểm

### 4.1. Công thức tính điểm

```
Điểm mỗi hit = Base Points + Reflex Bonus
             = 100 + int(max(0, TTL - reaction_time) / TTL × 50)
```

Trong đó:
- **Base Points** = 100 điểm (cố định cho mỗi lần bắn trúng)
- **TTL** = Thời gian sống của target (milliseconds)
- **reaction_time** = Thời gian từ lúc target xuất hiện đến lúc click (milliseconds)
- **Reflex Bonus** = Thưởng thêm dựa trên tốc độ phản xạ (0 → 50 điểm)

### 4.2. Cách tính Reflex Bonus

| Tốc độ phản xạ | Bonus | Giải thích |
|-----------------|-------|------------|
| Click ngay lập tức (0ms) | +50 | `(TTL - 0) / TTL × 50 = 50` |
| Click ở nửa thời gian | +25 | `(TTL - TTL/2) / TTL × 50 = 25` |
| Click sát hết hạn | +0~1 | `(TTL - ~TTL) / TTL × 50 ≈ 0` |
| Target hết hạn (miss) | 0 | Không được điểm |
| Click trượt (miss) | 0 | Không được điểm, tăng miss count |

### 4.3. Ví dụ cụ thể

**Ví dụ 1 — Easy, phản xạ nhanh:**
- Target TTL: 2500ms
- Reaction time: 400ms
- Base: 100
- Bonus: `int(max(0, 2500 - 400) / 2500 × 50)` = `int(2100/2500 × 50)` = `int(42.0)` = **42**
- **Tổng: 142 điểm**

**Ví dụ 2 — Hard, phản xạ trung bình:**
- Target TTL: 1000ms
- Reaction time: 600ms
- Base: 100
- Bonus: `int(max(0, 1000 - 600) / 1000 × 50)` = `int(400/1000 × 50)` = `int(20.0)` = **20**
- **Tổng: 120 điểm**

**Ví dụ 3 — Click chậm:**
- Target TTL: 1500ms
- Reaction time: 1400ms
- Base: 100
- Bonus: `int(max(0, 1500 - 1400) / 1500 × 50)` = `int(100/1500 × 50)` = `int(3.33)` = **3**
- **Tổng: 103 điểm**

### 4.4. Các chỉ số hiệu suất (Performance Metrics)

| Chỉ số | Công thức | Mô tả |
|--------|-----------|-------|
| **Hits** | Đếm số lần click trúng target | Tổng số target bắn trúng |
| **Misses** | Click trượt + Target hết hạn | Tổng số lần thất bại |
| **Accuracy** | `Hits / (Hits + Misses) × 100%` | Độ chính xác tổng thể |
| **Avg Reaction** | `Tổng reaction_time / Số hits` | Thời gian phản xạ trung bình |
| **Best Reaction** | `min(reaction_times)` | Thời gian phản xạ nhanh nhất |
| **Score** | `Σ (100 + bonus)` cho mỗi hit | Tổng điểm tích lũy |

### 4.5. Hệ thống kỷ lục (Records)

- Kỷ lục được lưu theo **Accuracy** (%), không phải Score
- Mỗi độ khó (Easy, Medium, Hard) có kỷ lục riêng
- So sánh: nếu `accuracy hiện tại > record[difficulty]` → cập nhật kỷ lục
- Lưu vào file `records.json`
- Điều kiện: phải có ít nhất 1 click (`total_clicks > 0`)

---

## 5. Hệ thống độ khó

### 5.1. Ba mức độ khó

| Thông số | Easy | Medium | Hard |
|----------|------|--------|------|
| **Max Targets** (đồng thời) | 2 | 3 | 5 |
| **Min Lifetime** (ms) | 2000 | 1200 | 800 |
| **Max Lifetime** (ms) | 3000 | 2000 | 1500 |
| **Spawn Delay** (ms) | 800 | 500 | 300 |

### 5.2. Difficulty Progression (Tăng dần theo thời gian)

Game trở nên khó hơn theo thời gian chơi (`progress = elapsed / duration`):

#### Kích thước Target giảm dần:
- **0% – 50% thời gian**: Target từ 50px giảm xuống 35px (tuyến tính)
- **50% – 100% thời gian**: Target từ 35px giảm xuống 20px (tuyến tính)

```
Nửa đầu:  size = 50 - (50 - 35) × (progress × 2) = 50 - 15 × (progress × 2)
Nửa sau:  size = 35 - (35 - 20) × ((progress - 0.5) × 2) = 35 - 15 × ((progress - 0.5) × 2)
```

#### Thời gian sống Target giảm dần:
- Lifetime giảm tối đa **30%** khi đến cuối game
- `adjusted_min = min_lifetime × (1 - progress × 0.3)`
- `adjusted_max = max_lifetime × (1 - progress × 0.3)`
- Có giới hạn tối thiểu: min = 500ms, max = 800ms (không bao giờ ngắn hơn)

---

## 6. Cơ chế gameplay

### 6.1. Spawn Target
- **Vị trí**: Random trong vùng an toàn (`MARGIN=80` pixel từ mép màn hình)
- **Tránh chồng chéo**: Kiểm tra khoảng cách tối thiểu 80px với target hiện có
- **Tối đa 50 lần thử** tìm vị trí hợp lệ; nếu không tìm được → đặt random
- **Tần suất spawn**: Theo spawn_delay của độ khó, chỉ spawn khi số target sống < max_targets

### 6.2. Hit Detection (Phát hiện va chạm)
- Sử dụng **phát hiện va chạm hình tròn** (circular collision)
- Công thức: `distance = √((mouse_x - target_x)² + (mouse_y - target_y)²)`
- Nếu `distance ≤ target_radius` → **HIT**
- Chỉ phát hiện hit với target đầu tiên trong danh sách (break sau hit đầu)
- Nếu không trúng target nào → **MISS**

### 6.3. Target Expiration
- Mỗi target có `lifetime` (thời gian sống) được random trong khoảng [min, max] của độ khó
- Khi `current_time - spawn_time ≥ lifetime` → target hết hạn → **MISS** (tự động)
- Target hết hạn bị xóa khỏi danh sách

### 6.4. Mouse & Crosshair
- **Trong gameplay**: Con trỏ hệ thống bị ẩn, thay bằng crosshair tùy chỉnh
- **Mouse Lock**: Chuột bị khóa trong cửa sổ game (`pygame.event.set_grab(True)`)
- **Tọa độ ảo**: Game sử dụng hệ tọa độ gốc 800×600, mouse position được scale về hệ tọa độ này
- **Sensitivity**: Di chuyển chuột nhân với hệ số sensitivity (mặc định 1.0x)
  ```python
  custom_cx += rel[0] × scale_x × sensitivity
  custom_cy += rel[1] × scale_y × sensitivity
  ```
- Khi vào gameplay → reset cursor về giữa màn hình
- Khi thoát gameplay → giải phóng chuột

### 6.5. Pause System
- Nhấn **ESC** khi đang chơi → Tạm dừng
- Game state chuyển sang `STATE_PAUSE`
- Thời gian **KHÔNG** bị dừng (sử dụng `pygame.time.get_ticks()`) — nhưng target không bị xử lý khi pause nên không ảnh hưởng
- Từ Pause có thể: Tiếp tục, Mở Settings, Thoát về Menu

---

## 7. Hệ thống cài đặt (Settings)

### 7.1. Tab General

| Cài đặt | Slider Range | Mặc định | Mô tả |
|---------|-------------|----------|-------|
| **Mouse Sensitivity** | 0.1 – 2.0 | 1.0 | Tốc độ di chuyển con trỏ trong game |
| **Volume** | 0.0 – 1.0 | 0.5 | Âm lượng hiệu ứng âm thanh |
| **Game Duration** | 30 – 120 (giây) | 60 | Thời lượng mỗi ván chơi |

### 7.2. Tab Crosshair

| Cài đặt | Range | Mặc định | Mô tả |
|---------|-------|----------|-------|
| **Size** | 0.5 – 2.0 | 1.0 | Hệ số kích thước tổng thể |
| **Thickness** | 1 – 6 | 2 | Độ dày các đường crosshair |
| **Gap** | 0 – 20 | 5 | Khoảng cách từ tâm đến các đường |
| **Length** | 0 – 30 | 12 | Chiều dài các đường (0 = chỉ có chấm) |
| **Dot Size** | 1 – 5 | 2 | Kích thước chấm tâm |
| **Outline** | ON/OFF | ON | Viền đen bao quanh crosshair |
| **Dot** | ON/OFF | ON | Hiện/ẩn chấm tâm |
| **Color** | 6 màu | Cyan | Màu crosshair |

**Màu có sẵn**: Cyan `(0,255,200)`, Green `(100,255,100)`, Red `(255,100,100)`, White `(255,255,255)`, Purple `(200,100,255)`, Yellow `(255,255,100)`

### 7.3. Tính năng slider
- Kéo thả handle để thay đổi giá trị
- Click vào ô giá trị → chế độ nhập số trực tiếp (hỗ trợ bàn phím)
- Enter để áp dụng, ESC để hủy
- Giá trị được clamp trong khoảng [min, max]

### 7.4. Preview Crosshair
- Tab Crosshair có ô **Preview** hiển thị trực tiếp crosshair với các cài đặt hiện tại
- Cập nhật real-time khi thay đổi slider

### 7.5. Scrollable UI
- Tab Crosshair hỗ trợ cuộn (scroll) khi nội dung vượt quá vùng hiển thị
- Cuộn bằng mouse wheel
- Hiển thị thanh scrollbar bên phải
- Content được clip (cắt) để không tràn ra ngoài vùng tabs/buttons

---

## 8. Hệ thống âm thanh

### 8.1. Procedural Audio (Âm thanh tạo bằng thuật toán)
Tất cả âm thanh được **tạo bằng toán học** (sine waves, noise) — **KHÔNG sử dụng file âm thanh bên ngoài**.

| Âm thanh | Thời lượng | Tần số | Mô tả |
|----------|-----------|--------|-------|
| **Hit** | 120ms | 600Hz + 900Hz + 1200Hz | Tiếng "pop" ngắn khi bắn trúng |
| **Miss** | 100ms | 150Hz + noise | Tiếng "thud" trầm khi bắn trượt |
| **Click** | 50ms | 1000Hz + 1500Hz | Tiếng click khi bấm nút UI |
| **Countdown** | 150ms | 800Hz | Tiếng beep cho đếm ngược 3-2-1 |
| **Go** | 250ms | 1200Hz + 1800Hz | Tiếng beep cao hơn cho "GO!" |
| **Game Over** | 800ms | 659→523→440Hz | Giai điệu ngắn xuống dần (E5→C5→A4) |

### 8.2. Background Music (BGM)
- **Vòng lặp 8 giây** chơi liên tục
- Tiến trình hợp âm: **Am → F → C → G** (mỗi hợp âm 2 giây)
- Sử dụng layered sine waves + octave harmony + LFO modulation
- Âm lượng BGM = 30% âm lượng SFX (để không lấn át gameplay)
- Có fade-in/fade-out giữa các hợp âm

### 8.3. Volume Control
- Tất cả SFX dùng chung mức volume từ Settings
- BGM tự động giảm 70% so với SFX
- Có thể điều chỉnh từ 0.0 (tắt) đến 1.0 (max)

---

## 9. Hệ thống đồ họa & hiệu ứng

### 9.1. Background
- **Gradient background**: Chuyển màu từ xanh đậm `(15,20,35)` ↓ tím đậm `(25,15,45)`
- **Grid lines**: Lưới mờ (màu `(30,35,55)`) cách nhau 50px
- **Particles**: 50 hạt sáng chuyển động chậm, wrap around khi ra ngoài màn hình
- **Corner decorations**: 4 góc có hình chữ L hoạt hình, dao động theo sin wave với phase offset khác nhau

### 9.2. Target Design
- **5 lớp đồ họa** (từ ngoài vào):
  1. Vòng ngoài phát sáng (pulsing glow) — 3 vòng neon
  2. Vòng chính — màu đỏ tươi `(255,70,90)` filled
  3. Vòng trong — màu hồng nhạt `(255,120,140)` ở 70% bán kính
  4. Vòng trắng — `(255,255,255)` ở 40% bán kính
  5. Chấm tâm — đỏ `(255,70,90)` ở 15% bán kính
- **Hiệu ứng pulsing**: Vòng ngoài dao động theo `sin(time × 0.01)` (±3px)
- **Cảnh báo hết hạn**: Vòng cam `(255,180,50)` khi target ở 70%+ thời gian sống

### 9.3. Hit Effect
- **3 vòng tròn xanh** mở rộng dần (expanding circles)
- **Chấm tâm** thu nhỏ dần (shrinking dot)
- **Floating score text**: Chữ "+X điểm" bay lên trên (trong 300ms đầu)
- Toàn bộ hiệu ứng kéo dài **400ms**

### 9.4. Miss Effect
- **Dấu X đỏ** từ 2 đường chéo
- Dấu X mở rộng nhẹ theo thời gian
- Kéo dài **300ms**

### 9.5. Crosshair
- Vẽ bằng `pygame.Rect` cho pixel-perfect centering
- 4 đường (trái, phải, trên, dưới) với gap ở giữa
- Viền đen (outline) tùy chọn — dày hơn crosshair 2px
- Chấm tâm (dot) tùy chọn với viền đen riêng
- Nếu length = 0 → chỉ hiện dot (kiểu dot-only crosshair)

### 9.6. Scaling System
- Game thiết kế ở độ phân giải gốc **800×600**
- Hỗ trợ **resize cửa sổ** — tất cả tọa độ được scale theo (scale_x, scale_y)
- Fonts được tạo lại khi resize
- Tất cả đối tượng (target, button, slider, crosshair, effects) đều hỗ trợ scale
- Các độ phân giải preset: 800×600, 1024×768, 1280×720, 1366×768, 1600×900, 1920×1080

---

## 10. Lưu trữ dữ liệu

### 10.1. records.json — Kỷ lục
```json
{
  "EASY": 89.47,
  "MEDIUM": 0,
  "HARD": 69
}
```
- Lưu **accuracy cao nhất** (%) cho mỗi độ khó
- Cập nhật tự động khi kết thúc game nếu vượt kỷ lục
- Tạo mới với giá trị 0.0 nếu file không tồn tại

### 10.2. settings.json — Cài đặt người dùng
```json
{
  "mouse_sensitivity": 1.0,
  "volume": 0.5,
  "crosshair_size": 1.0,
  "crosshair_color": "Cyan",
  "crosshair_thickness": 2,
  "crosshair_gap": 5,
  "crosshair_length": 12,
  "crosshair_outline": true,
  "crosshair_dot": true,
  "crosshair_dot_size": 2,
  "game_duration": 60
}
```
- Lưu khi nhấn `SAVE & APPLY` trong Settings
- Load khi khởi động game, merge với default nếu thiếu key
- Xử lý lỗi: nếu file lỗi/không đọc được → dùng default

---

## 11. Kiến trúc kỹ thuật

### 11.1. Game Loop
```
Khởi tạo → [Vòng lặp chính]
              ├── Tick (60 FPS)
              ├── Xử lý Input (Events)
              ├── Update Logic
              ├── Render (Draw)
              └── Display Flip
```
- **FPS cố định**: 60 FPS sử dụng `pygame.time.Clock()`
- **Delta time**: `dt = clock.tick(FPS)` (không dùng trực tiếp, dùng ticks)
- **Event dispatch**: Mỗi state chuyển event sang screen tương ứng

### 11.2. State Machine Flow
```
MENU ─────────────→ INSTRUCTION ──→ MENU
  │                                   ↑
  ├──→ SETTINGS ──────────────────────┤
  │                                   │
  └──→ DIFFICULTY ──→ COUNTDOWN ──→ PLAYING ──→ GAME OVER
         ↑                  ↑           │           │
         │                  │           ↓           │
         │                  └─── PAUSE ──┤          │
         │                       │       │          │
         │                       ↓       │          │
         │                   SETTINGS    │          │
         │                               │          │
         └───────────────────────────────┘──────────┘
```

### 11.3. Coordinate System
- **Base coordinates**: 800×600 (tham chiếu cố định)
- **Display coordinates**: Kích thước thực của cửa sổ
- **Scale factors**: `scale_x = display_width / 800`, `scale_y = display_height / 600`
- Mouse input: Chuyển từ display coords → base coords để xử lý logic
- Render output: Chuyển từ base coords → display coords để vẽ

### 11.4. Tính năng nổi bật
- **100% Procedural**: Không sử dụng bất kỳ file asset bên ngoài nào (ảnh, âm thanh, font đặc biệt)
- **Resizable Window**: Hỗ trợ thay đổi kích thước cửa sổ real-time
- **Persistent Data**: Settings và Records được lưu/load tự động
- **Modular Architecture**: Chia tách rõ ràng giữa classes, screens, utils
- **Custom Crosshair**: Hệ thống crosshair tùy biến cao, tương tự FPS games

---

*Tài liệu được tạo dựa trên phân tích toàn bộ mã nguồn của dự án Aim Trainer.*
