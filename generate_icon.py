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

"""Generate exact 25x25 menu icon for Pebble OS compatibility."""

import os
from PIL import Image, ImageDraw


def create_25x25_menu_icon(official_logo_path: str = "/tmp/antigravity_official.png", target_path: str = "pebble_app/resources/images/app_icon.png"):
    size = 25
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Dark squircle badge
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=5, fill=(11, 16, 33, 255), outline=(30, 41, 59, 255), width=1)

    # 2. Official logo if available
    if os.path.exists(official_logo_path):
        logo = Image.open(official_logo_path).convert("RGBA")
        logo_resized = logo.resize((18, 18), Image.Resampling.LANCZOS)
        img.paste(logo_resized, (3, 3), logo_resized)
    else:
        # Fallback Antigravity cyber dot
        draw.ellipse([5, 5, 19, 19], fill=(0, 240, 255, 255))

    # 3. Green checkmark approve badge in corner
    badge_r = 5
    bx, by = 18, 18
    draw.ellipse([bx - badge_r, by - badge_r, bx + badge_r, by + badge_r], fill=(0, 230, 118, 255), outline=(255, 255, 255, 255), width=1)
    draw.line([(bx - 2, by), (bx - 1, by + 2), (bx + 2, by - 2)], fill=(255, 255, 255, 255), width=1)

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    img.save(target_path, format="PNG", optimize=True)
    print(f"✓ Saved {target_path} (exact size: {img.size[0]}x{img.size[1]} px)")


if __name__ == "__main__":
    create_25x25_menu_icon()
