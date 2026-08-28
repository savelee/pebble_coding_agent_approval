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

"""Generate all submission image assets for Rebble App Store."""

import math
import os
import struct
import zlib
from typing import List, Tuple


class ImageBuffer:
    """Simple RGBA image rasterizer without external dependencies."""

    def __init__(self, width: int, height: int, bg_color: Tuple[int, int, int, int] = (0, 0, 0, 0)):
        self.width = width
        self.height = height
        self.pixels = bytearray(width * height * 4)
        for i in range(0, len(self.pixels), 4):
            self.pixels[i:i + 4] = bytes(bg_color)

    def set_pixel(self, x: int, y: int, color: Tuple[int, int, int, int]):
        if 0 <= x < self.width and 0 <= y < self.height:
            idx = (y * self.width + x) * 4
            # Alpha blending
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
        for cy in range(y, min(y + h, self.height)):
            for cx in range(x, min(x + w, self.width)):
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

    def draw_simple_text(self, text: str, x: int, y: int, color: Tuple[int, int, int, int], scale: int = 1):
        """Simple 5x7 bitmap font renderer for clean labels."""
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

    def save_png(self, filepath: str):
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
        print(f"Saved {filepath} ({self.width}x{self.height})")


def generate_action_screen(width: int, height: int, status_text: str = "READY", status_color=(255, 215, 0, 255)) -> ImageBuffer:
    img = ImageBuffer(width, height)
    header_h = int(height * 0.1)
    usable_h = height - header_h
    half_h = usable_h // 2
    top_y = header_h
    bot_y = header_h + half_h

    # Top Status Bar
    img.fill_rect(0, 0, width, header_h, (0, 0, 0, 255))
    scale = 2 if width >= 200 else 1
    text_w = len(status_text) * (6 * scale)
    img.draw_simple_text(status_text, (width - text_w) // 2, (header_h - 5 * scale) // 2, status_color, scale)

    # Top Half (Kelly Green)
    img.fill_rect(0, top_y, width, half_h, (0, 135, 90, 255))
    top_cx = width // 2
    top_cy = top_y + half_h // 2 - int(height * 0.04)
    radius = int(width * 0.11)
    img.fill_circle(top_cx, top_cy, radius, (0, 168, 107, 255))
    img.draw_circle(top_cx, top_cy, radius, (255, 255, 255, 255), 2)
    # Checkmark
    chk_scale = int(radius * 0.45)
    img.draw_line(top_cx - chk_scale, top_cy, top_cx - chk_scale // 3, top_cy + chk_scale, (255, 255, 255, 255), 3)
    img.draw_line(top_cx - chk_scale // 3, top_cy + chk_scale, top_cx + chk_scale, top_cy - chk_scale * 2 // 3, (255, 255, 255, 255), 3)

    label_scale = 2 if width >= 200 else 1
    top_label = "CONFIRM [UP]"
    tl_w = len(top_label) * (6 * label_scale)
    img.draw_simple_text(top_label, (width - tl_w) // 2, top_y + half_h - 7 * label_scale - 4, (255, 255, 255, 255), label_scale)

    # Bottom Half (Red)
    img.fill_rect(0, bot_y, width, half_h, (217, 56, 30, 255))
    bot_cx = width // 2
    bot_cy = bot_y + half_h // 2 - int(height * 0.04)
    img.fill_circle(bot_cx, bot_cy, radius, (178, 34, 34, 255))
    img.draw_circle(bot_cx, bot_cy, radius, (255, 255, 255, 255), 2)
    # Cross
    cr_scale = int(radius * 0.45)
    img.draw_line(bot_cx - cr_scale, bot_cy - cr_scale, bot_cx + cr_scale, bot_cy + cr_scale, (255, 255, 255, 255), 3)
    img.draw_line(bot_cx - cr_scale, bot_cy + cr_scale, bot_cx + cr_scale, bot_cy - cr_scale, (255, 255, 255, 255), 3)

    bot_label = "DISAPPROVE [DOWN]"
    bl_w = len(bot_label) * (6 * label_scale)
    img.draw_simple_text(bot_label, (width - bl_w) // 2, bot_y + half_h - 7 * label_scale - 4, (255, 255, 255, 255), label_scale)

    # Divider line
    img.draw_line(0, bot_y, width, bot_y, (0, 0, 0, 255), 2)
    return img


def generate_splash_screen(width: int, height: int) -> ImageBuffer:
    img = ImageBuffer(width, height, (11, 26, 48, 255))

    # Header
    scale = 2 if width >= 200 else 1
    title = "AGENT APPROVALS"
    t_w = len(title) * (6 * scale)
    img.draw_simple_text(title, (width - t_w) // 2, 10, (255, 255, 255, 255), scale)

    # Center mini layout preview box
    card_w = int(width * 0.35)
    card_h = int(height * 0.38)
    card_x = (width - card_w) // 2
    card_y = int(height * 0.16)

    # Bezel
    img.fill_rect(card_x - 3, card_y - 3, card_w + 6, card_h + 6, (0, 0, 0, 255))
    img.draw_circle(card_x + card_w // 2, card_y + card_h // 2, card_w // 2 + 4, (255, 255, 255, 255), 1)

    # Mini top green
    m_half = card_h // 2
    img.fill_rect(card_x, card_y, card_w, m_half, (0, 135, 90, 255))
    img.fill_circle(card_x + card_w // 2, card_y + m_half // 2, 9, (0, 168, 107, 255))
    img.draw_circle(card_x + card_w // 2, card_y + m_half // 2, 9, (255, 255, 255, 255), 1)

    # Mini bot red
    img.fill_rect(card_x, card_y + m_half, card_w, m_half, (217, 56, 30, 255))
    img.fill_circle(card_x + card_w // 2, card_y + m_half + m_half // 2, 9, (178, 34, 34, 255))
    img.draw_circle(card_x + card_w // 2, card_y + m_half + m_half // 2, 9, (255, 255, 255, 255), 1)

    # Explanation lines
    lines = [
        "APPROVE YOUR CODING AGENT",
        "(LIKE ANTIGRAVITY)",
        "FROM YOUR WRIST!"
    ]
    txt_y = card_y + card_h + 12
    for line in lines:
        lw = len(line) * 6
        img.draw_simple_text(line, (width - lw) // 2, txt_y, (200, 220, 240, 255), 1)
        txt_y += 10

    # Footer
    foot = "PRESS ANY BUTTON"
    fw = len(foot) * 6
    img.draw_simple_text(foot, (width - fw) // 2, height - 16, (0, 230, 118, 255), 1)
    return img


def generate_banner() -> ImageBuffer:
    width = 720
    height = 320
    img = ImageBuffer(width, height, (11, 26, 48, 255))

    # Background ambient glows
    for y in range(height):
        for x in range(width):
            gx1 = (x - 180) ** 2 + (y - 160) ** 2
            gx2 = (x - 540) ** 2 + (y - 160) ** 2
            if gx1 < 160 ** 2:
                intensity = int((1.0 - (gx1 / (160 ** 2))) * 40)
                img.set_pixel(x, y, (0, 135, 90, intensity))
            if gx2 < 160 ** 2:
                intensity = int((1.0 - (gx2 / (160 ** 2))) * 40)
                img.set_pixel(x, y, (217, 56, 30, intensity))

    # Center Pebble watch chassis graphic (Emery 200x228 frame)
    watch_w = 140
    watch_h = 160
    wx = (width - watch_w) // 2
    wy = 40

    # Watch frame
    img.fill_rect(wx - 6, wy - 6, watch_w + 12, watch_h + 12, (20, 20, 22, 255))
    img.draw_circle(wx + watch_w // 2, wy + watch_h // 2, watch_w // 2 + 10, (60, 64, 67, 255), 2)

    # Top half (Green Confirm)
    wh_half = watch_h // 2
    img.fill_rect(wx, wy, watch_w, wh_half, (0, 135, 90, 255))
    img.fill_circle(wx + watch_w // 2, wy + wh_half // 2, 20, (0, 168, 107, 255))
    img.draw_circle(wx + watch_w // 2, wy + wh_half // 2, 20, (255, 255, 255, 255), 2)
    img.draw_line(wx + watch_w // 2 - 8, wy + wh_half // 2, wx + watch_w // 2 - 2, wy + wh_half // 2 + 8, (255, 255, 255, 255), 3)
    img.draw_line(wx + watch_w // 2 - 2, wy + wh_half // 2 + 8, wx + watch_w // 2 + 8, wy + wh_half // 2 - 6, (255, 255, 255, 255), 3)

    # Bottom half (Red Disapprove)
    img.fill_rect(wx, wy + wh_half, watch_w, wh_half, (217, 56, 30, 255))
    img.fill_circle(wx + watch_w // 2, wy + wh_half + wh_half // 2, 20, (178, 34, 34, 255))
    img.draw_circle(wx + watch_w // 2, wy + wh_half + wh_half // 2, 20, (255, 255, 255, 255), 2)
    img.draw_line(wx + watch_w // 2 - 7, wy + wh_half + wh_half // 2 - 7, wx + watch_w // 2 + 7, wy + wh_half + wh_half // 2 + 7, (255, 255, 255, 255), 3)
    img.draw_line(wx + watch_w // 2 - 7, wy + wh_half + wh_half // 2 + 7, wx + watch_w // 2 + 7, wy + wh_half + wh_half // 2 - 7, (255, 255, 255, 255), 3)

    # Text Banner
    title = "AGENT APPROVALS"
    tw = len(title) * (6 * 3)
    img.draw_simple_text(title, (width - tw) // 2, 220, (255, 255, 255, 255), 3)

    subtitle = "ONE-CLICK CODING AGENT APPROVALS FOR PEBBLE TIME 2"
    sw = len(subtitle) * (6 * 1)
    img.draw_simple_text(subtitle, (width - sw) // 2, 255, (0, 230, 118, 255), 1)

    sub2 = "GOOGLE ANTIGRAVITY - CURSOR - CLAUDE CODE"
    s2w = len(sub2) * 6
    img.draw_simple_text(sub2, (width - s2w) // 2, 275, (180, 200, 220, 255), 1)

    by = "BY @SAVELEE"
    byw = len(by) * 6
    img.draw_simple_text(by, (width - byw) // 2, 295, (100, 140, 180, 255), 1)

    return img


def generate_large_icon(size: int = 144) -> ImageBuffer:
    img = ImageBuffer(size, size, (0, 0, 0, 0))
    cx = size // 2
    cy = size // 2
    radius = size // 2 - 4

    # Rounded outer badge
    img.fill_circle(cx, cy, radius, (11, 26, 48, 255))
    img.draw_circle(cx, cy, radius, (0, 230, 118, 255), 4)

    # Top green half circle
    sub_r = int(radius * 0.4)
    img.fill_circle(cx - sub_r // 2, cy - 4, sub_r, (0, 135, 90, 255))
    img.draw_circle(cx - sub_r // 2, cy - 4, sub_r, (255, 255, 255, 255), 2)
    img.draw_line(cx - sub_r // 2 - 8, cy - 4, cx - sub_r // 2 - 2, cy + 4, (255, 255, 255, 255), 3)
    img.draw_line(cx - sub_r // 2 - 2, cy + 4, cx - sub_r // 2 + 8, cy - 10, (255, 255, 255, 255), 3)

    # Bottom red half circle
    img.fill_circle(cx + sub_r // 2, cy + 4, sub_r, (217, 56, 30, 255))
    img.draw_circle(cx + sub_r // 2, cy + 4, sub_r, (255, 255, 255, 255), 2)
    img.draw_line(cx + sub_r // 2 - 7, cy + 4 - 7, cx + sub_r // 2 + 7, cy + 4 + 7, (255, 255, 255, 255), 3)
    img.draw_line(cx + sub_r // 2 - 7, cy + 4 + 7, cx + sub_r // 2 + 7, cy + 4 - 7, (255, 255, 255, 255), 3)

    return img


def main():
    out_dir = "store_assets"
    os.makedirs(out_dir, exist_ok=True)

    # 1. Store Banner (720x320)
    banner = generate_banner()
    banner.save_png(os.path.join(out_dir, "banner_720x320.png"))

    # 2. Large Appstore Icon (144x144 & 80x80)
    icon_144 = generate_large_icon(144)
    icon_144.save_png(os.path.join(out_dir, "icon_large_144x144.png"))

    icon_80 = generate_large_icon(80)
    icon_80.save_png(os.path.join(out_dir, "icon_80x80.png"))

    # 3. Pebble Time 2 (Emery: 200x228) Screenshots
    # Screenshot 1: Main Action Screen
    s1 = generate_action_screen(200, 228, status_text="READY", status_color=(255, 215, 0, 255))
    s1.save_png(os.path.join(out_dir, "screenshot_1_action_emery.png"))

    # Screenshot 2: Splash / Info Screen
    s2 = generate_splash_screen(200, 228)
    s2.save_png(os.path.join(out_dir, "screenshot_2_splash_emery.png"))

    # Screenshot 3: Action Confirmed / SENT OK
    s3 = generate_action_screen(200, 228, status_text="SENT OK", status_color=(0, 230, 118, 255))
    s3.save_png(os.path.join(out_dir, "screenshot_3_sent_emery.png"))

    # 4. Pebble Time / Pebble Time Steel (Basalt: 144x168) Screenshots
    b1 = generate_action_screen(144, 168, status_text="READY", status_color=(255, 215, 0, 255))
    b1.save_png(os.path.join(out_dir, "screenshot_4_action_basalt.png"))

    b2 = generate_splash_screen(144, 168)
    b2.save_png(os.path.join(out_dir, "screenshot_5_splash_basalt.png"))

    print("\nAll store submission image resources generated successfully in 'store_assets/' directory!")


if __name__ == "__main__":
    main()
