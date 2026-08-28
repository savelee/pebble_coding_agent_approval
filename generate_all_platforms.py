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

"""Generate screenshots for all Pebble platforms: Aplite, Basalt, Chalk, Diorite, Emery, Flint, Gabbro."""

import os
from PIL import Image, ImageDraw


def generate_color_rectangular(w: int, h: int, status: str = "READY") -> Image.Image:
    """Generate color split-screen for Basalt, Flint, Gabbro."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    header_h = int(h * 0.11)
    usable_h = h - header_h
    half_h = usable_h // 2

    # Status Bar
    draw.rectangle([0, 0, w, header_h], fill=(0, 0, 0, 255))
    draw.text((w // 2 - len(status) * 4, 3), status, fill=(255, 215, 0, 255))

    # Top Green
    top_y = header_h
    draw.rectangle([0, top_y, w, top_y + half_h], fill=(0, 135, 90, 255))
    top_cx = w // 2
    top_cy = top_y + half_h // 2 - int(h * 0.04)
    btn_r = int(w * 0.11)
    draw.ellipse([top_cx - btn_r, top_cy - btn_r, top_cx + btn_r, top_cy + btn_r], fill=(0, 168, 107, 255), outline=(255, 255, 255, 255), width=2)
    chk_s = int(btn_r * 0.45)
    draw.line([(top_cx - chk_s, top_cy), (top_cx - chk_s // 3, top_cy + chk_s), (top_cx + chk_s, top_cy - chk_s * 2 // 3)], fill=(255, 255, 255, 255), width=max(2, w // 60))
    draw.text((w // 2 - 40, top_y + half_h - 16), "CONFIRM [UP]", fill=(255, 255, 255, 255))

    # Bottom Red
    bot_y = header_h + half_h
    draw.rectangle([0, bot_y, w, h], fill=(217, 56, 30, 255))
    bot_cx = w // 2
    bot_cy = bot_y + half_h // 2 - int(h * 0.04)
    draw.ellipse([bot_cx - btn_r, bot_cy - btn_r, bot_cx + btn_r, bot_cy + btn_r], fill=(178, 34, 34, 255), outline=(255, 255, 255, 255), width=2)
    draw.line([(bot_cx - chk_s, bot_cy - chk_s), (bot_cx + chk_s, bot_cy + chk_s)], fill=(255, 255, 255, 255), width=max(2, w // 60))
    draw.line([(bot_cx - chk_s, bot_cy + chk_s), (bot_cx + chk_s, bot_cy - chk_s)], fill=(255, 255, 255, 255), width=max(2, w // 60))
    draw.text((w // 2 - 56, bot_y + half_h - 16), "DISAPPROVE [DOWN]", fill=(255, 255, 255, 255))

    draw.line([(0, bot_y), (w, bot_y)], fill=(0, 0, 0, 255), width=2)
    return img


def generate_bw_rectangular(w: int, h: int, status: str = "READY") -> Image.Image:
    """Generate monochrome 1-bit split-screen for Aplite and Diorite."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    header_h = int(h * 0.11)
    usable_h = h - header_h
    half_h = usable_h // 2

    # Status Bar
    draw.rectangle([0, 0, w, header_h], fill=(0, 0, 0, 255))
    draw.text((w // 2 - len(status) * 4, 3), status, fill=(255, 255, 255, 255))

    # Top Half: White Background (Confirm)
    top_y = header_h
    draw.rectangle([0, top_y, w, top_y + half_h], fill=(255, 255, 255, 255))
    top_cx = w // 2
    top_cy = top_y + half_h // 2 - int(h * 0.04)
    btn_r = int(w * 0.11)
    draw.ellipse([top_cx - btn_r, top_cy - btn_r, top_cx + btn_r, top_cy + btn_r], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2)
    chk_s = int(btn_r * 0.45)
    draw.line([(top_cx - chk_s, top_cy), (top_cx - chk_s // 3, top_cy + chk_s), (top_cx + chk_s, top_cy - chk_s * 2 // 3)], fill=(0, 0, 0, 255), width=2)
    draw.text((w // 2 - 40, top_y + half_h - 16), "CONFIRM [UP]", fill=(0, 0, 0, 255))

    # Bottom Half: Black Background (Disapprove)
    bot_y = header_h + half_h
    draw.rectangle([0, bot_y, w, h], fill=(0, 0, 0, 255))
    bot_cx = w // 2
    bot_cy = bot_y + half_h // 2 - int(h * 0.04)
    draw.ellipse([bot_cx - btn_r, bot_cy - btn_r, bot_cx + btn_r, bot_cy + btn_r], fill=(0, 0, 0, 255), outline=(255, 255, 255, 255), width=2)
    draw.line([(bot_cx - chk_s, bot_cy - chk_s), (bot_cx + chk_s, bot_cy + chk_s)], fill=(255, 255, 255, 255), width=2)
    draw.line([(bot_cx - chk_s, bot_cy + chk_s), (bot_cx + chk_s, bot_cy - chk_s)], fill=(255, 255, 255, 255), width=2)
    draw.text((w // 2 - 56, bot_y + half_h - 16), "DISAPPROVE [DOWN]", fill=(255, 255, 255, 255))

    draw.line([(0, bot_y), (w, bot_y)], fill=(0, 0, 0, 255), width=2)
    return img


def generate_chalk_round(size: int = 180, status: str = "READY") -> Image.Image:
    """Generate circular Pebble Time Round (Chalk) screenshot."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx = size // 2
    cy = size // 2
    r = size // 2

    # Draw Round Face
    # 1. Top Half: Green
    draw.pieslice([0, 0, size - 1, size - 1], start=180, end=360, fill=(0, 135, 90, 255))
    # 2. Bottom Half: Red
    draw.pieslice([0, 0, size - 1, size - 1], start=0, end=180, fill=(217, 56, 30, 255))

    # Center Divider Line
    draw.line([(0, cy), (size, cy)], fill=(0, 0, 0, 255), width=3)

    # Center Status Header Pill
    pill_w = 64
    pill_h = 18
    draw.rectangle([cx - pill_w // 2, cy - pill_h // 2, cx + pill_w // 2, cy + pill_h // 2], fill=(0, 0, 0, 255))
    draw.ellipse([cx - pill_w // 2 - 8, cy - pill_h // 2, cx - pill_w // 2 + 8, cy + pill_h // 2], fill=(0, 0, 0, 255))
    draw.ellipse([cx + pill_w // 2 - 8, cy - pill_h // 2, cx + pill_w // 2 + 8, cy + pill_h // 2], fill=(0, 0, 0, 255))
    draw.text((cx - 16, cy - 6), status, fill=(255, 215, 0, 255))

    # Top Confirm Button (Green)
    top_cy = cy - 40
    btn_r = 16
    draw.ellipse([cx - btn_r, top_cy - btn_r, cx + btn_r, top_cy + btn_r], fill=(0, 168, 107, 255), outline=(255, 255, 255, 255), width=2)
    draw.line([(cx - 6, top_cy), (cx - 2, top_cy + 6), (cx + 6, top_cy - 5)], fill=(255, 255, 255, 255), width=2)
    draw.text((cx - 36, top_cy + 20), "CONFIRM [UP]", fill=(255, 255, 255, 255))

    # Bottom Disapprove Button (Red)
    bot_cy = cy + 40
    draw.ellipse([cx - btn_r, bot_cy - btn_r, cx + btn_r, bot_cy + btn_r], fill=(178, 34, 34, 255), outline=(255, 255, 255, 255), width=2)
    draw.line([(cx - 5, bot_cy - 5), (cx + 5, bot_cy + 5)], fill=(255, 255, 255, 255), width=2)
    draw.line([(cx - 5, bot_cy + 5), (cx + 5, bot_cy - 5)], fill=(255, 255, 255, 255), width=2)
    draw.text((cx - 50, bot_cy - 28), "DISAPPROVE [DOWN]", fill=(255, 255, 255, 255))

    # Outer round border
    draw.ellipse([0, 0, size - 1, size - 1], outline=(0, 0, 0, 255), width=2)
    return img


def main():
    out_dir = "store_assets"
    os.makedirs(out_dir, exist_ok=True)

    # 1. Aplite: 144x168 (B&W Classic)
    aplite = generate_bw_rectangular(144, 168)
    aplite.save(os.path.join(out_dir, "screenshot_aplite_144x168.png"), format="PNG")
    print("Saved store_assets/screenshot_aplite_144x168.png (144x168)")

    # 2. Basalt: 144x168 and 155x168 (Pebble Time)
    basalt_144 = generate_color_rectangular(144, 168)
    basalt_144.save(os.path.join(out_dir, "screenshot_basalt_144x168.png"), format="PNG")
    print("Saved store_assets/screenshot_basalt_144x168.png (144x168)")

    basalt_155 = generate_color_rectangular(155, 168)
    basalt_155.save(os.path.join(out_dir, "screenshot_basalt_155x168.png"), format="PNG")
    print("Saved store_assets/screenshot_basalt_155x168.png (155x168)")

    # 3. Chalk: 180x180 (Round Pebble Time Round)
    chalk = generate_chalk_round(180)
    chalk.save(os.path.join(out_dir, "screenshot_chalk_180x180.png"), format="PNG")
    print("Saved store_assets/screenshot_chalk_180x180.png (180x180 Round)")

    # 4. Diorite: 144x168 (Pebble 2 Monochrome)
    diorite = generate_bw_rectangular(144, 168)
    diorite.save(os.path.join(out_dir, "screenshot_diorite_144x168.png"), format="PNG")
    print("Saved store_assets/screenshot_diorite_144x168.png (144x168)")

    # 5. Flint: 144x168 (Color Prototype)
    flint = generate_color_rectangular(144, 168)
    flint.save(os.path.join(out_dir, "screenshot_flint_144x168.png"), format="PNG")
    print("Saved store_assets/screenshot_flint_144x168.png (144x168)")

    # 6. Gabbro: 260x260 (High-res Prototype)
    gabbro = generate_color_rectangular(260, 260)
    gabbro.save(os.path.join(out_dir, "screenshot_gabbro_260x260.png"), format="PNG")
    print("Saved store_assets/screenshot_gabbro_260x260.png (260x260)")

    print("\n✨ All platform screenshots generated for Aplite, Basalt, Chalk, Diorite, Flint, Gabbro!")


if __name__ == "__main__":
    main()
