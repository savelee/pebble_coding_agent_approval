# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generate high-polish Antigravity-branded Rebble App Store assets."""

import math
import os
import struct
import zlib
from typing import Tuple


class Canvas:
    """High-quality 32-bit RGBA canvas with anti-aliasing and shape rendering."""

    def __init__(self, width: int, height: int, bg_color: Tuple[int, int, int, int] = (11, 16, 33, 255)):
        self.width = width
        self.height = height
        self.pixels = bytearray(width * height * 4)
        for i in range(0, len(self.pixels), 4):
            self.pixels[i:i + 4] = bytes(bg_color)

    def set_pixel(self, x: int, y: int, color: Tuple[int, int, int, int]):
        if 0 <= x < self.width and 0 <= y < self.height:
            idx = (y * self.width + x) * 4
            src_a = color[3] / 255.0
            if src_a == 1.0:
                self.pixels[idx:idx + 4] = bytes(color)
            elif src_a > 0.0:
                dst_r = self.pixels[idx]
                dst_g = self.pixels[idx + 1]
                dst_b = self.pixels[idx + 2]
                dst_a = self.pixels[idx + 3] / 255.0
                out_a = src_a + dst_a * (1.0 - src_a)
                out_r = int((color[0] * src_a + dst_r * dst_a * (1.0 - src_a)) / out_a)
                out_g = int((color[1] * src_a + dst_g * dst_a * (1.0 - src_a)) / out_a)
                out_b = int((color[2] * src_a + dst_b * dst_a * (1.0 - src_a)) / out_a)
                self.pixels[idx] = out_r
                self.pixels[idx + 1] = out_g
                self.pixels[idx + 2] = out_b
                self.pixels[idx + 3] = int(out_a * 255)

    def fill_rect(self, x: int, y: int, w: int, h: int, color: Tuple[int, int, int, int]):
        for cy in range(max(0, y), min(y + h, self.height)):
            for cx in range(max(0, x), min(x + w, self.width)):
                self.set_pixel(cx, cy, color)

    def fill_rounded_rect(self, x: int, y: int, w: int, h: int, r: int, color: Tuple[int, int, int, int]):
        for cy in range(max(0, y), min(y + h, self.height)):
            for cx in range(max(0, x), min(x + w, self.width)):
                # Check corners
                in_corner = False
                if cx < x + r and cy < y + r:
                    if (cx - (x + r)) ** 2 + (cy - (y + r)) ** 2 > r * r:
                        continue
                elif cx > x + w - r and cy < y + r:
                    if (cx - (x + w - r)) ** 2 + (cy - (y + r)) ** 2 > r * r:
                        continue
                elif cx < x + r and cy > y + h - r:
                    if (cx - (x + r)) ** 2 + (cy - (y + h - r)) ** 2 > r * r:
                        continue
                elif cx > x + w - r and cy > y + h - r:
                    if (cx - (x + w - r)) ** 2 + (cy - (y + h - r)) ** 2 > r * r:
                        continue
                self.set_pixel(cx, cy, color)

    def fill_circle(self, cx: int, cy: int, radius: int, color: Tuple[int, int, int, int]):
        r_sq = radius * radius
        for y in range(cy - radius, cy + radius + 1):
            for x in range(cx - radius, cx + radius + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r_sq:
                    self.set_pixel(x, y, color)

    def draw_circle(self, cx: int, cy: int, radius: int, color: Tuple[int, int, int, int], width: int = 1):
        r_min_sq = (radius - width) ** 2
        r_max_sq = radius ** 2
        for y in range(cy - radius, cy + radius + 1):
            for x in range(cx - radius, cx + radius + 1):
                d_sq = (x - cx) ** 2 + (y - cy) ** 2
                if r_min_sq <= d_sq <= r_max_sq:
                    self.set_pixel(x, y, color)

    def draw_line(self, x0: int, y0: int, x1: int, y1: int, color: Tuple[int, int, int, int], thickness: int = 1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            for tx in range(-thickness // 2, thickness // 2 + 1):
                for ty in range(-thickness // 2, thickness // 2 + 1):
                    self.set_pixel(x0 + tx, y0 + ty, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def draw_text(self, text: str, x: int, y: int, color: Tuple[int, int, int, int], scale: int = 1):
        font_map = {
            'A': ["01110", "10001", "11111", "10001", "10001"],
            'B': ["11110", "10001", "11110", "10001", "11110"],
            'C': ["01111", "10000", "10000", "10000", "01111"],
            'D': ["11110", "10001", "10001", "10001", "11110"],
            'E': ["11111", "10000", "11110", "10000", "11111"],
            'F': ["11111", "10000", "11110", "10000", "10000"],
            'G': ["01111", "10000", "10011", "10001", "01111"],
            'H': ["10001", "10001", "11111", "10001", "10001"],
            'I': ["11111", "00100", "00100", "00100", "11111"],
            'J': ["00001", "00001", "00001", "10001", "01110"],
            'K': ["10001", "10010", "11100", "10010", "10001"],
            'L': ["10000", "10000", "10000", "10000", "11111"],
            'M': ["10001", "11011", "10101", "10001", "10001"],
            'N': ["10001", "11001", "10101", "10011", "10001"],
            'O': ["01110", "10001", "10001", "10001", "01110"],
            'P': ["11110", "10001", "11110", "10000", "10000"],
            'Q': ["01110", "10001", "10101", "10011", "01111"],
            'R': ["11110", "10001", "11110", "10010", "10001"],
            'S': ["01111", "10000", "01110", "00001", "11110"],
            'T': ["11111", "00100", "00100", "00100", "00100"],
            'U': ["10001", "10001", "10001", "10001", "01110"],
            'V': ["10001", "10001", "10001", "01010", "00100"],
            'W': ["10001", "10001", "10101", "11011", "10001"],
            'X': ["10001", "01010", "00100", "01010", "10001"],
            'Y': ["10001", "01010", "00100", "00100", "00100"],
            'Z': ["11111", "00010", "00100", "01000", "11111"],
            '0': ["01110", "10011", "10101", "11001", "01110"],
            '1': ["00100", "01100", "00100", "00100", "01110"],
            '2': ["01110", "10001", "00110", "01000", "11111"],
            '3': ["11110", "00001", "01110", "00001", "11110"],
            '4': ["10001", "10001", "11111", "00001", "00001"],
            '5': ["11111", "10000", "11110", "00001", "11110"],
            '6': ["01110", "10000", "11110", "10001", "01110"],
            '7': ["11111", "00001", "00010", "00100", "00100"],
            '8': ["01110", "10001", "01110", "10001", "01110"],
            '9': ["01110", "10001", "01111", "00001", "01110"],
            '[': ["011", "010", "010", "010", "011"],
            ']': ["110", "010", "010", "010", "110"],
            '.': ["0", "0", "0", "0", "1"],
            '!': ["1", "1", "1", "0", "1"],
            '-': ["000", "000", "111", "000", "000"],
            ' ': ["000", "000", "000", "000", "000"],
            '@': ["01110", "10001", "10111", "10000", "01111"],
            '/': ["00001", "00010", "00100", "01000", "10000"],
            ':': ["0", "1", "0", "1", "0"],
        }
        cx = x
        for char in text.upper():
            glyph = font_map.get(char, font_map[' '])
            g_w = len(glyph[0])
            for r, row in enumerate(glyph):
                for c, val in enumerate(row):
                    if val == '1':
                        self.fill_rect(cx + c * scale, y + r * scale, scale, scale, color)
            cx += (g_w + 1) * scale

    def save(self, filepath: str):
        raw_data = bytearray()
        for y in range(self.height):
            raw_data.append(0)
            raw_data.extend(self.pixels[y * self.width * 4:(y + 1) * self.width * 4])

        def chunk(chunk_type: bytes, data: bytes) -> bytes:
            length = struct.pack(">I", len(data))
            crc = struct.pack(">I", zlib.crc32(chunk_type + data) & 0xffffffff)
            return length + chunk_type + data + crc

        png = b"\x89PNG\r\n\x1a\n"
        ihdr = struct.pack(">IIBBBBB", self.width, self.height, 8, 6, 0, 0, 0)
        png += chunk(b"IHDR", ihdr)
        compressed = zlib.compress(bytes(raw_data), 9)
        png += chunk(b"IDAT", compressed)
        png += chunk(b"IEND", b"")

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(png)
        print(f"Generated {filepath} ({self.width}x{self.height})")


def draw_antigravity_logo(canvas: Canvas, cx: int, cy: int, radius: int):
    """Draw the futuristic glowing Antigravity Delta / Orbital Prism emblem."""
    # Outer ambient glow
    for dr in range(radius + 15, radius - 5, -2):
        alpha = int(max(0, (radius + 15 - dr) * 4))
        canvas.draw_circle(cx, cy, dr, (0, 240, 255, alpha), 2)

    # 3-Axis Orbital Delta Prism Loops
    # Indigo, Cyan, and Violet overlapping curves
    points_cyan = []
    points_indigo = []
    points_violet = []

    num_pts = 60
    for i in range(num_pts):
        angle = 2 * math.pi * i / num_pts
        # Trifolium / Trefoil knot projection
        r_mod = radius * (0.8 + 0.25 * math.cos(3 * angle))
        px = cx + int(r_mod * math.cos(angle))
        py = cy + int(r_mod * math.sin(angle))

        if i < num_pts // 3:
            points_cyan.append((px, py))
        elif i < 2 * num_pts // 3:
            points_indigo.append((px, py))
        else:
            points_violet.append((px, py))

    # Render glowing orbital tracks
    all_pts = points_cyan + points_indigo + points_violet
    for i in range(len(all_pts)):
        p1 = all_pts[i]
        p2 = all_pts[(i + 1) % len(all_pts)]
        if i < len(all_pts) // 3:
            color = (0, 240, 255, 255)  # Neon Cyan
        elif i < 2 * len(all_pts) // 3:
            color = (99, 102, 241, 255)  # Electric Indigo
        else:
            color = (168, 85, 247, 255)  # Violet
        canvas.draw_line(p1[0], p1[1], p2[0], p2[1], color, max(2, radius // 12))

    # Center Energy Core
    core_r = max(4, radius // 4)
    canvas.fill_circle(cx, cy, core_r + 2, (0, 240, 255, 120))
    canvas.fill_circle(cx, cy, core_r, (255, 255, 255, 255))


def generate_app_icon(size: int) -> Canvas:
    """Generate Antigravity logo with a vibrant Green Checkmark Approve Button on top."""
    canvas = Canvas(size, size, (0, 0, 0, 0))
    cx = size // 2
    cy = size // 2
    r = size // 2 - 2

    # Rounded Squircle App Badge
    canvas.fill_rounded_rect(2, 2, size - 4, size - 4, size // 4, (11, 16, 33, 255))
    canvas.draw_circle(cx, cy, r, (30, 41, 59, 255), 2)

    # 1. Antigravity Core Emblem in Center-Background
    draw_antigravity_logo(canvas, cx, cy - size // 14, int(size * 0.38))

    # 2. Glowing Green Checkmark Approve Button in Foreground (Bottom Right / Center)
    btn_r = int(size * 0.26)
    btn_cx = size - btn_r - max(4, size // 16)
    btn_cy = size - btn_r - max(4, size // 16)

    # Outer glow & border
    canvas.fill_circle(btn_cx, btn_cy, btn_r + 2, (11, 16, 33, 255))
    canvas.fill_circle(btn_cx, btn_cy, btn_r, (0, 230, 118, 255))  # Vivid Emerald
    canvas.draw_circle(btn_cx, btn_cy, btn_r, (255, 255, 255, 255), max(1, size // 48))

    # Sharp White Checkmark
    chk_sz = int(btn_r * 0.52)
    th = max(2, size // 36)
    p1 = (btn_cx - chk_sz, btn_cy)
    p2 = (btn_cx - chk_sz // 3, btn_cy + chk_sz)
    p3 = (btn_cx + chk_sz, btn_cy - chk_sz * 2 // 3)
    canvas.draw_line(p1[0], p1[1], p2[0], p2[1], (255, 255, 255, 255), th)
    canvas.draw_line(p2[0], p2[1], p3[0], p3[1], (255, 255, 255, 255), th)

    return canvas


def generate_screenshot_180x180() -> Canvas:
    """Generate 180x180 exact screenshot of the real Pebble watch app layout."""
    size = 180
    canvas = Canvas(size, size, (0, 0, 0, 255))
    header_h = 20
    usable_h = size - header_h
    half_h = usable_h // 2

    # Top Status Bar
    canvas.fill_rect(0, 0, size, header_h, (0, 0, 0, 255))
    status = "READY"
    tw = len(status) * 12
    canvas.draw_text(status, (size - tw) // 2, 4, (255, 215, 0, 255), 2)

    # Top Half: Emerald Kelly Green (CONFIRM [UP])
    top_y = header_h
    canvas.fill_rect(0, top_y, size, half_h, (0, 135, 90, 255))
    top_cx = size // 2
    top_cy = top_y + half_h // 2 - 8
    btn_r = 18
    canvas.fill_circle(top_cx, top_cy, btn_r, (0, 168, 107, 255))
    canvas.draw_circle(top_cx, top_cy, btn_r, (255, 255, 255, 255), 2)
    # White checkmark
    canvas.draw_line(top_cx - 8, top_cy, top_cx - 2, top_cy + 8, (255, 255, 255, 255), 3)
    canvas.draw_line(top_cx - 2, top_cy + 8, top_cx + 8, top_cy - 6, (255, 255, 255, 255), 3)

    label_up = "CONFIRM [UP]"
    lu_w = len(label_up) * 6
    canvas.draw_text(label_up, (size - lu_w) // 2, top_y + half_h - 14, (255, 255, 255, 255), 1)

    # Bottom Half: Crimson Red (DISAPPROVE [DOWN])
    bot_y = header_h + half_h
    canvas.fill_rect(0, bot_y, size, half_h, (217, 56, 30, 255))
    bot_cx = size // 2
    bot_cy = bot_y + half_h // 2 - 8
    canvas.fill_circle(bot_cx, bot_cy, btn_r, (178, 34, 34, 255))
    canvas.draw_circle(bot_cx, bot_cy, btn_r, (255, 255, 255, 255), 2)
    # White Cross
    canvas.draw_line(bot_cx - 7, bot_cy - 7, bot_cx + 7, bot_cy + 7, (255, 255, 255, 255), 3)
    canvas.draw_line(bot_cx - 7, bot_cy + 7, bot_cx + 7, bot_cy - 7, (255, 255, 255, 255), 3)

    label_down = "DISAPPROVE [DOWN]"
    ld_w = len(label_down) * 6
    canvas.draw_text(label_down, (size - ld_w) // 2, bot_y + half_h - 14, (255, 255, 255, 255), 1)

    # Divider
    canvas.draw_line(0, bot_y, size, bot_y, (0, 0, 0, 255), 2)
    return canvas


def generate_banner_720x320() -> Canvas:
    """Generate 720x320 banner featuring Antigravity logo, watch screen, and developer aesthetic."""
    w, h = 720, 320
    canvas = Canvas(w, h, (11, 16, 33, 255))

    # Ambient cyber glows
    for y in range(h):
        for x in range(w):
            d1 = (x - 140) ** 2 + (y - 160) ** 2
            d2 = (x - 560) ** 2 + (y - 160) ** 2
            if d1 < 180 ** 2:
                intensity = int((1.0 - (d1 / (180 ** 2))) * 45)
                canvas.set_pixel(x, y, (0, 240, 255, intensity))
            if d2 < 180 ** 2:
                intensity = int((1.0 - (d2 / (180 ** 2))) * 45)
                canvas.set_pixel(x, y, (0, 230, 118, intensity))

    # Left Side: High-tech Antigravity Emblem
    draw_antigravity_logo(canvas, 150, 160, 85)

    # Glowing Approve Checkmark on Emblem
    canvas.fill_circle(195, 215, 28, (11, 16, 33, 255))
    canvas.fill_circle(195, 215, 24, (0, 230, 118, 255))
    canvas.draw_circle(195, 215, 24, (255, 255, 255, 255), 2)
    canvas.draw_line(184, 215, 191, 223, (255, 255, 255, 255), 3)
    canvas.draw_line(191, 223, 207, 207, (255, 255, 255, 255), 3)

    # Right Side: Realistic Pebble Time 2 Watch Mockup
    pw = 116
    ph = 144
    px = 530
    py = 88

    # Pebble bezel & strap hints
    canvas.fill_rounded_rect(px - 14, py - 14, pw + 28, ph + 28, 22, (20, 24, 34, 255))
    canvas.draw_circle(px + pw // 2, py + ph // 2, pw // 2 + 16, (45, 55, 72, 255), 2)

    # Pebble screen inside mockup
    canvas.fill_rect(px, py, pw, 14, (0, 0, 0, 255))
    canvas.draw_text("READY", px + 36, py + 3, (255, 215, 0, 255), 1)

    # Split screen (Green / Red)
    half_mock = (ph - 14) // 2
    canvas.fill_rect(px, py + 14, pw, half_mock, (0, 135, 90, 255))
    canvas.fill_circle(px + pw // 2, py + 14 + half_mock // 2, 13, (0, 168, 107, 255))
    canvas.draw_circle(px + pw // 2, py + 14 + half_mock // 2, 13, (255, 255, 255, 255), 1)
    canvas.draw_line(px + pw // 2 - 5, py + 14 + half_mock // 2, px + pw // 2 - 1, py + 14 + half_mock // 2 + 5, (255, 255, 255, 255), 2)
    canvas.draw_line(px + pw // 2 - 1, py + 14 + half_mock // 2 + 5, px + pw // 2 + 5, py + 14 + half_mock // 2 - 4, (255, 255, 255, 255), 2)

    canvas.fill_rect(px, py + 14 + half_mock, pw, half_mock, (217, 56, 30, 255))
    canvas.fill_circle(px + pw // 2, py + 14 + half_mock + half_mock // 2, 13, (178, 34, 34, 255))
    canvas.draw_circle(px + pw // 2, py + 14 + half_mock + half_mock // 2, 13, (255, 255, 255, 255), 1)
    canvas.draw_line(px + pw // 2 - 4, py + 14 + half_mock + half_mock // 2 - 4, px + pw // 2 + 4, py + 14 + half_mock + half_mock // 2 + 4, (255, 255, 255, 255), 2)
    canvas.draw_line(px + pw // 2 - 4, py + 14 + half_mock + half_mock // 2 + 4, px + pw // 2 + 4, py + 14 + half_mock + half_mock // 2 - 4, (255, 255, 255, 255), 2)

    canvas.draw_line(px, py + 14 + half_mock, px + pw, py + 14 + half_mock, (0, 0, 0, 255), 2)

    # Center Typography
    title = "ANTIGRAVITY"
    canvas.draw_text(title, 265, 95, (0, 240, 255, 255), 3)

    subtitle = "WRIST APPROVALS"
    canvas.draw_text(subtitle, 265, 130, (255, 255, 255, 255), 3)

    desc = "ONE-CLICK PEBBLE TIME 2 ACTIONS"
    canvas.draw_text(desc, 265, 170, (0, 230, 118, 255), 1)

    desc2 = "APPROVE / REJECT AI CODING PROMPTS"
    canvas.draw_text(desc2, 265, 190, (148, 163, 184, 255), 1)

    tag = "BY @SAVELEE - GITHUB.COM/SAVELEE"
    canvas.draw_text(tag, 265, 225, (99, 102, 241, 255), 1)

    return canvas


def main():
    out_dir = "store_assets"
    os.makedirs(out_dir, exist_ok=True)

    # 1. Exact 180x180 screenshot of real app
    s_180 = generate_screenshot_180x180()
    s_180.save(os.path.join(out_dir, "screenshot_180x180.png"))

    # 2. Exact 720x320 Banner with Antigravity logo
    banner = generate_banner_720x320()
    banner.save(os.path.join(out_dir, "banner_720x320.png"))

    # 3. Exact 144x144 App Icon (Antigravity logo + Green Checkmark)
    icon_144 = generate_app_icon(144)
    icon_144.save(os.path.join(out_dir, "icon_144x144.png"))

    # 4. Exact 48x48 App Icon (Antigravity logo + Green Checkmark)
    icon_48 = generate_app_icon(48)
    icon_48.save(os.path.join(out_dir, "icon_48x48.png"))

    print("\n✨ All requested store assets generated with Antigravity branding!")


if __name__ == "__main__":
    main()
