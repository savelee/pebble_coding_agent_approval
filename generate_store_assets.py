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

"""Generate high-polish Rebble App Store assets using official Antigravity brand logo."""

import os
from PIL import Image, ImageDraw, ImageFilter


def create_green_checkmark_badge(size: int) -> Image.Image:
    """Create a high-quality green approve badge with sharp white checkmark."""
    badge = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)

    # Outer border for contrast
    cx = size // 2
    cy = size // 2
    r = size // 2 - 1

    # Shadow/Border
    draw.ellipse([0, 0, size - 1, size - 1], fill=(11, 16, 33, 255))
    # Emerald green circle
    draw.ellipse([2, 2, size - 3, size - 3], fill=(0, 230, 118, 255), outline=(255, 255, 255, 255), width=max(1, size // 24))

    # White Checkmark
    chk_sz = int(r * 0.5)
    th = max(2, size // 14)
    p1 = (cx - chk_sz, cy)
    p2 = (cx - chk_sz // 3, cy + chk_sz)
    p3 = (cx + chk_sz, cy - chk_sz * 2 // 3)
    draw.line([p1, p2], fill=(255, 255, 255, 255), width=th, joint="curve")
    draw.line([p2, p3], fill=(255, 255, 255, 255), width=th, joint="curve")
    return badge


def generate_app_icon_with_official_logo(official_logo_path: str, size: int) -> Image.Image:
    """Compose squircle app icon with official Antigravity logo and green approve badge."""
    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)

    # 1. Dark Navy Squircle Background
    radius = size // 4
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=(11, 16, 33, 255), outline=(30, 41, 59, 255), width=max(1, size // 64))

    # 2. Ambient glow behind logo
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_r = int(size * 0.45)
    glow_draw.ellipse([size // 2 - glow_r, size // 2 - glow_r, size // 2 + glow_r, size // 2 + glow_r], fill=(0, 240, 255, 45))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=size // 16))
    icon.paste(glow, (0, 0), glow)

    # 3. Resize and paste official Antigravity Logo
    logo = Image.open(official_logo_path).convert("RGBA")
    logo_size = int(size * 0.72)
    logo_resized = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    logo_x = (size - logo_size) // 2
    logo_y = (size - logo_size) // 2 - (size // 20)
    icon.paste(logo_resized, (logo_x, logo_y), logo_resized)

    # 4. Paste Green Approve Checkmark Badge in bottom-right corner
    badge_size = int(size * 0.38)
    badge = create_green_checkmark_badge(badge_size)
    badge_x = size - badge_size - max(2, size // 32)
    badge_y = size - badge_size - max(2, size // 32)
    icon.paste(badge, (badge_x, badge_y), badge)

    return icon


def generate_banner_720x320(official_logo_path: str) -> Image.Image:
    """Generate 720x320 banner with high-res official Antigravity logo, typography, and Pebble mockup."""
    w, h = 720, 320
    banner = Image.new("RGBA", (w, h), (11, 16, 33, 255))
    draw = ImageDraw.Draw(banner)

    # Left ambient cyan glow
    glow1 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g1_draw = ImageDraw.Draw(glow1)
    g1_draw.ellipse([20, 40, 300, 320], fill=(0, 240, 255, 35))
    g1_draw.ellipse([450, 40, 710, 300], fill=(0, 230, 118, 30))
    glow1 = glow1.filter(ImageFilter.GaussianBlur(radius=30))
    banner.paste(glow1, (0, 0), glow1)

    # 1. Official Antigravity Logo on Left
    logo = Image.open(official_logo_path).convert("RGBA")
    logo_resized = logo.resize((190, 190), Image.Resampling.LANCZOS)
    banner.paste(logo_resized, (50, 65), logo_resized)

    # Green Approve Badge overlaid on the Antigravity Logo
    badge = create_green_checkmark_badge(64)
    banner.paste(badge, (180, 190), badge)

    # 2. Pebble Time 2 Watch Mockup on Right
    pw, ph = 120, 148
    px, py = 540, 86
    draw.rounded_rectangle([px - 10, py - 10, px + pw + 10, py + ph + 10], radius=18, fill=(20, 24, 34, 255), outline=(51, 65, 85, 255), width=2)

    # Pebble Watch Screen
    header_h = 16
    draw.rectangle([px, py, px + pw, py + header_h], fill=(0, 0, 0, 255))
    draw.text((px + 40, py + 2), "READY", fill=(255, 215, 0, 255))

    # Split green / red screen
    half_h = (ph - header_h) // 2
    # Green Confirm
    draw.rectangle([px, py + header_h, px + pw, py + header_h + half_h], fill=(0, 135, 90, 255))
    draw.ellipse([px + pw // 2 - 14, py + header_h + half_h // 2 - 14, px + pw // 2 + 14, py + header_h + half_h // 2 + 14], fill=(0, 168, 107, 255), outline=(255, 255, 255, 255), width=1)
    draw.line([(px + pw // 2 - 6, py + header_h + half_h // 2), (px + pw // 2 - 2, py + header_h + half_h // 2 + 5), (px + pw // 2 + 6, py + header_h + half_h // 2 - 4)], fill=(255, 255, 255, 255), width=2)

    # Red Disapprove
    draw.rectangle([px, py + header_h + half_h, px + pw, py + ph], fill=(217, 56, 30, 255))
    draw.ellipse([px + pw // 2 - 14, py + header_h + half_h + half_h // 2 - 14, px + pw // 2 + 14, py + header_h + half_h + half_h // 2 + 14], fill=(178, 34, 34, 255), outline=(255, 255, 255, 255), width=1)
    draw.line([(px + pw // 2 - 5, py + header_h + half_h + half_h // 2 - 5), (px + pw // 2 + 5, py + header_h + half_h + half_h // 2 + 5)], fill=(255, 255, 255, 255), width=2)
    draw.line([(px + pw // 2 - 5, py + header_h + half_h + half_h // 2 + 5), (px + pw // 2 + 5, py + header_h + half_h + half_h // 2 - 5)], fill=(255, 255, 255, 255), width=2)

    # Divider line
    draw.line([(px, py + header_h + half_h), (px + pw, py + header_h + half_h)], fill=(0, 0, 0, 255), width=2)

    # 3. Typography
    # Title
    draw.text((260, 85), "ANTIGRAVITY", fill=(0, 240, 255, 255))
    draw.text((260, 115), "WRIST APPROVALS", fill=(255, 255, 255, 255))
    draw.text((260, 160), "ONE-CLICK PEBBLE TIME 2 ACTIONS", fill=(0, 230, 118, 255))
    draw.text((260, 185), "CONFIRM OR REJECT CODING AGENT PROMPTS", fill=(148, 163, 184, 255))
    draw.text((260, 215), "BY @SAVELEE • GITHUB.COM/SAVELEE", fill=(99, 102, 241, 255))

    return banner


def generate_screenshot_180x180() -> Image.Image:
    """Generate 180x180 exact screenshot of the real Pebble watch app layout."""
    size = 180
    img = Image.new("RGBA", (size, size), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    header_h = 22
    usable_h = size - header_h
    half_h = usable_h // 2

    # Top Status Bar
    draw.rectangle([0, 0, size, header_h], fill=(0, 0, 0, 255))
    draw.text((size // 2 - 20, 4), "READY", fill=(255, 215, 0, 255))

    # Top Half: Kelly Green
    top_y = header_h
    draw.rectangle([0, top_y, size, top_y + half_h], fill=(0, 135, 90, 255))
    top_cx = size // 2
    top_cy = top_y + half_h // 2 - 8
    draw.ellipse([top_cx - 20, top_cy - 20, top_cx + 20, top_cy + 20], fill=(0, 168, 107, 255), outline=(255, 255, 255, 255), width=2)
    draw.line([(top_cx - 8, top_cy), (top_cx - 2, top_cy + 8), (top_cx + 8, top_cy - 6)], fill=(255, 255, 255, 255), width=3)
    draw.text((size // 2 - 42, top_y + half_h - 16), "CONFIRM [UP]", fill=(255, 255, 255, 255))

    # Bottom Half: Crimson Red
    bot_y = header_h + half_h
    draw.rectangle([0, bot_y, size, size], fill=(217, 56, 30, 255))
    bot_cx = size // 2
    bot_cy = bot_y + half_h // 2 - 8
    draw.ellipse([bot_cx - 20, bot_cy - 20, bot_cx + 20, bot_cy + 20], fill=(178, 34, 34, 255), outline=(255, 255, 255, 255), width=2)
    draw.line([(bot_cx - 7, bot_cy - 7), (bot_cx + 7, bot_cy + 7)], fill=(255, 255, 255, 255), width=3)
    draw.line([(bot_cx - 7, bot_cy + 7), (bot_cx + 7, bot_cy - 7)], fill=(255, 255, 255, 255), width=3)
    draw.text((size // 2 - 58, bot_y + half_h - 16), "DISAPPROVE [DOWN]", fill=(255, 255, 255, 255))

    # Divider line
    draw.line([(0, bot_y), (size, bot_y)], fill=(0, 0, 0, 255), width=2)
    return img


def generate_watch_splash_logo(official_logo_path: str, out_path: str) -> None:
    """Generate 64x64 PNG of official Antigravity logo optimized for Pebble watch display."""
    logo = Image.open(official_logo_path).convert("RGBA")
    logo_watch = logo.resize((60, 60), Image.Resampling.LANCZOS)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    logo_watch.save(out_path, format="PNG")
    print(f"Generated watch logo resource: {out_path}")


def main():
    official_logo_path = "/tmp/antigravity_official.png"
    if not os.path.exists(official_logo_path):
        raise FileNotFoundError(f"Missing {official_logo_path}. Download first.")

    out_dir = "store_assets"
    os.makedirs(out_dir, exist_ok=True)

    # Save copy of official high-res logo in store_assets
    logo_official = Image.open(official_logo_path)
    logo_official.save(os.path.join(out_dir, "antigravity-icon__full-color.png"), format="PNG")

    # 1. 144x144 App Icon with official Antigravity logo + Green Approve Checkmark
    icon_144 = generate_app_icon_with_official_logo(official_logo_path, 144)
    icon_144.save(os.path.join(out_dir, "icon_144x144.png"), format="PNG")
    print("Generated store_assets/icon_144x144.png (144x144)")

    # 2. 48x48 App Icon
    icon_48 = generate_app_icon_with_official_logo(official_logo_path, 48)
    icon_48.save(os.path.join(out_dir, "icon_48x48.png"), format="PNG")
    print("Generated store_assets/icon_48x48.png (48x48)")

    # 3. 720x320 Store Header Banner
    banner = generate_banner_720x320(official_logo_path)
    banner.save(os.path.join(out_dir, "banner_720x320.png"), format="PNG")
    print("Generated store_assets/banner_720x320.png (720x320)")

    # 4. 180x180 Real App Screenshot
    screenshot = generate_screenshot_180x180()
    screenshot.save(os.path.join(out_dir, "screenshot_180x180.png"), format="PNG")
    print("Generated store_assets/screenshot_180x180.png (180x180)")

    # 5. 28x28 Pebble Watch Menu Icon
    menu_icon = generate_app_icon_with_official_logo(official_logo_path, 28)
    menu_icon_path = "pebble_app/resources/images/app_icon.png"
    os.makedirs(os.path.dirname(menu_icon_path), exist_ok=True)
    menu_icon.save(menu_icon_path, format="PNG")
    print(f"Generated {menu_icon_path} (28x28)")

    # 6. Watch Splash Screen Logo resource (60x60)
    generate_watch_splash_logo(official_logo_path, "pebble_app/resources/images/antigravity_logo_watch.png")

    print("\n✨ All store assets and watch resources updated with official Antigravity full-color branding!")


if __name__ == "__main__":
    main()
