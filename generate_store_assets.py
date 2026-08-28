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

"""Generate high-polish Rebble App Store assets including exact 200x228 Emery screenshots."""

import os
from PIL import Image, ImageDraw, ImageFilter


def create_green_checkmark_badge(size: int) -> Image.Image:
    """Create a high-quality green approve badge with sharp white checkmark."""
    badge = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)

    cx = size // 2
    cy = size // 2
    r = size // 2 - 1

    # Shadow / Border
    draw.ellipse([0, 0, size - 1, size - 1], fill=(11, 16, 33, 255))
    draw.ellipse([2, 2, size - 3, size - 3], fill=(0, 230, 118, 255), outline=(255, 255, 255, 255), width=max(1, size // 24))

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

    radius = size // 4
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=(11, 16, 33, 255), outline=(30, 41, 59, 255), width=max(1, size // 64))

    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_r = int(size * 0.45)
    glow_draw.ellipse([size // 2 - glow_r, size // 2 - glow_r, size // 2 + glow_r, size // 2 + glow_r], fill=(0, 240, 255, 45))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=size // 16))
    icon.paste(glow, (0, 0), glow)

    logo = Image.open(official_logo_path).convert("RGBA")
    logo_size = int(size * 0.72)
    logo_resized = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    logo_x = (size - logo_size) // 2
    logo_y = (size - logo_size) // 2 - (size // 20)
    icon.paste(logo_resized, (logo_x, logo_y), logo_resized)

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

    glow1 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g1_draw = ImageDraw.Draw(glow1)
    g1_draw.ellipse([20, 40, 300, 320], fill=(0, 240, 255, 35))
    g1_draw.ellipse([450, 40, 710, 300], fill=(0, 230, 118, 30))
    glow1 = glow1.filter(ImageFilter.GaussianBlur(radius=30))
    banner.paste(glow1, (0, 0), glow1)

    logo = Image.open(official_logo_path).convert("RGBA")
    logo_resized = logo.resize((190, 190), Image.Resampling.LANCZOS)
    banner.paste(logo_resized, (50, 65), logo_resized)

    badge = create_green_checkmark_badge(64)
    banner.paste(badge, (180, 190), badge)

    pw, ph = 120, 148
    px, py = 540, 86
    draw.rounded_rectangle([px - 10, py - 10, px + pw + 10, py + ph + 10], radius=18, fill=(20, 24, 34, 255), outline=(51, 65, 85, 255), width=2)

    header_h = 16
    draw.rectangle([px, py, px + pw, py + header_h], fill=(0, 0, 0, 255))
    draw.text((px + 40, py + 2), "READY", fill=(255, 215, 0, 255))

    half_h = (ph - header_h) // 2
    draw.rectangle([px, py + header_h, px + pw, py + header_h + half_h], fill=(0, 135, 90, 255))
    draw.ellipse([px + pw // 2 - 14, py + header_h + half_h // 2 - 14, px + pw // 2 + 14, py + header_h + half_h // 2 + 14], fill=(0, 168, 107, 255), outline=(255, 255, 255, 255), width=1)
    draw.line([(px + pw // 2 - 6, py + header_h + half_h // 2), (px + pw // 2 - 2, py + header_h + half_h // 2 + 5), (px + pw // 2 + 6, py + header_h + half_h // 2 - 4)], fill=(255, 255, 255, 255), width=2)

    draw.rectangle([px, py + header_h + half_h, px + pw, py + ph], fill=(217, 56, 30, 255))
    draw.ellipse([px + pw // 2 - 14, py + header_h + half_h + half_h // 2 - 14, px + pw // 2 + 14, py + header_h + half_h + half_h // 2 + 14], fill=(178, 34, 34, 255), outline=(255, 255, 255, 255), width=1)
    draw.line([(px + pw // 2 - 5, py + header_h + half_h + half_h // 2 - 5), (px + pw // 2 + 5, py + header_h + half_h + half_h // 2 + 5)], fill=(255, 255, 255, 255), width=2)
    draw.line([(px + pw // 2 - 5, py + header_h + half_h + half_h // 2 + 5), (px + pw // 2 + 5, py + header_h + half_h + half_h // 2 - 5)], fill=(255, 255, 255, 255), width=2)

    draw.line([(px, py + header_h + half_h), (px + pw, py + header_h + half_h)], fill=(0, 0, 0, 255), width=2)

    draw.text((260, 85), "ANTIGRAVITY", fill=(0, 240, 255, 255))
    draw.text((260, 115), "WRIST APPROVALS", fill=(255, 255, 255, 255))
    draw.text((260, 160), "ONE-CLICK PEBBLE TIME 2 ACTIONS", fill=(0, 230, 118, 255))
    draw.text((260, 185), "CONFIRM OR REJECT CODING AGENT PROMPTS", fill=(148, 163, 184, 255))
    draw.text((260, 215), "BY @SAVELEE • GITHUB.COM/SAVELEE", fill=(99, 102, 241, 255))

    return banner


def generate_emery_screenshot_200x228(status_text: str = "READY", status_color=(255, 215, 0, 255)) -> Image.Image:
    """Generate exact 200x228 Emery (Pebble Time 2) screenshot."""
    w, h = 200, 228
    img = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    header_h = 24
    usable_h = h - header_h
    half_h = usable_h // 2

    # Top Status Bar
    draw.rectangle([0, 0, w, header_h], fill=(0, 0, 0, 255))
    # Center text
    draw.text((w // 2 - len(status_text) * 4, 5), status_text, fill=status_color)

    # Top Half: Kelly Green
    top_y = header_h
    draw.rectangle([0, top_y, w, top_y + half_h], fill=(0, 135, 90, 255))
    top_cx = w // 2
    top_cy = top_y + half_h // 2 - 10
    btn_r = 22
    draw.ellipse([top_cx - btn_r, top_cy - btn_r, top_cx + btn_r, top_cy + btn_r], fill=(0, 168, 107, 255), outline=(255, 255, 255, 255), width=2)
    # Checkmark
    draw.line([(top_cx - 9, top_cy), (top_cx - 3, top_cy + 9), (top_cx + 9, top_cy - 7)], fill=(255, 255, 255, 255), width=3)
    draw.text((w // 2 - 42, top_y + half_h - 18), "CONFIRM [UP]", fill=(255, 255, 255, 255))

    # Bottom Half: Crimson Red
    bot_y = header_h + half_h
    draw.rectangle([0, bot_y, w, h], fill=(217, 56, 30, 255))
    bot_cx = w // 2
    bot_cy = bot_y + half_h // 2 - 10
    draw.ellipse([bot_cx - btn_r, bot_cy - btn_r, bot_cx + btn_r, bot_cy + btn_r], fill=(178, 34, 34, 255), outline=(255, 255, 255, 255), width=2)
    # Cross
    draw.line([(bot_cx - 8, bot_cy - 8), (bot_cx + 8, bot_cy + 8)], fill=(255, 255, 255, 255), width=3)
    draw.line([(bot_cx - 8, bot_cy + 8), (bot_cx + 8, bot_cy - 8)], fill=(255, 255, 255, 255), width=3)
    draw.text((w // 2 - 58, bot_y + half_h - 18), "DISAPPROVE [DOWN]", fill=(255, 255, 255, 255))

    # Divider line
    draw.line([(0, bot_y), (w, bot_y)], fill=(0, 0, 0, 255), width=2)
    return img


def generate_emery_splash_screenshot_200x228(official_logo_path: str) -> Image.Image:
    """Generate exact 200x228 Emery (Pebble Time 2) splash screen screenshot."""
    w, h = 200, 228
    img = Image.new("RGBA", (w, h), (11, 26, 48, 255))
    draw = ImageDraw.Draw(img)

    # Title
    draw.text((w // 2 - 44, 8), "ANTIGRAVITY", fill=(0, 240, 255, 255))

    # Official Antigravity Logo in center
    logo = Image.open(official_logo_path).convert("RGBA")
    logo_resized = logo.resize((68, 68), Image.Resampling.LANCZOS)
    img.paste(logo_resized, ((w - 68) // 2, 32), logo_resized)

    # Explanation Lines
    lines = [
        "Approve your coding agent",
        "(like Antigravity) from your",
        "wrist, with the Pebble Time 2",
        "app (and web extension)."
    ]
    txt_y = 110
    for line in lines:
        draw.text(((w - len(line) * 6) // 2, txt_y), line, fill=(255, 255, 255, 255))
        txt_y += 18

    # Footer
    draw.text((w // 2 - 60, h - 22), "Press any button to start", fill=(0, 230, 118, 255))
    return img


def main():
    official_logo_path = "/tmp/antigravity_official.png"
    if not os.path.exists(official_logo_path):
        raise FileNotFoundError(f"Missing {official_logo_path}.")

    out_dir = "store_assets"
    os.makedirs(out_dir, exist_ok=True)

    # 1. 200x228 Emery Screenshot (Main Action Ready)
    s_emery_action = generate_emery_screenshot_200x228(status_text="READY", status_color=(255, 215, 0, 255))
    s_emery_action.save(os.path.join(out_dir, "screenshot_emery_200x228.png"), format="PNG")
    print("Generated store_assets/screenshot_emery_200x228.png (200x228)")

    # 2. 200x228 Emery Splash Screen
    s_emery_splash = generate_emery_splash_screenshot_200x228(official_logo_path)
    s_emery_splash.save(os.path.join(out_dir, "screenshot_emery_splash_200x228.png"), format="PNG")
    print("Generated store_assets/screenshot_emery_splash_200x228.png (200x228)")

    # 3. 200x228 Emery Screenshot (Sent Confirmation)
    s_emery_sent = generate_emery_screenshot_200x228(status_text="SENT OK", status_color=(0, 230, 118, 255))
    s_emery_sent.save(os.path.join(out_dir, "screenshot_emery_sent_200x228.png"), format="PNG")
    print("Generated store_assets/screenshot_emery_sent_200x228.png (200x228)")

    # 4. App Icons (144x144, 48x48)
    icon_144 = generate_app_icon_with_official_logo(official_logo_path, 144)
    icon_144.save(os.path.join(out_dir, "icon_144x144.png"), format="PNG")
    print("Generated store_assets/icon_144x144.png (144x144)")

    icon_48 = generate_app_icon_with_official_logo(official_logo_path, 48)
    icon_48.save(os.path.join(out_dir, "icon_48x48.png"), format="PNG")
    print("Generated store_assets/icon_48x48.png (48x48)")

    # 5. 720x320 Store Banner
    banner = generate_banner_720x320(official_logo_path)
    banner.save(os.path.join(out_dir, "banner_720x320.png"), format="PNG")
    print("Generated store_assets/banner_720x320.png (720x320)")

    print("\n✨ All 200x228 Emery screenshots & assets generated successfully!")


if __name__ == "__main__":
    main()
