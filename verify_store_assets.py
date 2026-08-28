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

"""Verify and optimize all store asset PNGs for Rebble Developer Portal compatibility."""

import os
from PIL import Image


def fix_and_verify_store_assets():
    store_dir = "store_assets"
    files = {
        "banner_720x320.png": ("RGB", (720, 320)),
        "icon_144x144.png": ("RGBA", (144, 144)),
        "icon_48x48.png": ("RGBA", (48, 48)),
        "screenshot_emery_200x228.png": ("RGB", (200, 228)),
        "screenshot_emery_splash_200x228.png": ("RGB", (200, 228)),
        "screenshot_emery_sent_200x228.png": ("RGB", (200, 228)),
        "screenshot_aplite_144x168.png": ("RGB", (144, 168)),
        "screenshot_basalt_144x168.png": ("RGB", (144, 168)),
        "screenshot_chalk_180x180.png": ("RGBA", (180, 180)),
        "screenshot_diorite_144x168.png": ("RGB", (144, 168)),
        "screenshot_flint_144x168.png": ("RGB", (144, 168)),
        "screenshot_gabbro_260x260.png": ("RGB", (260, 260)),
    }

    for filename, (mode, (exp_w, exp_h)) in files.items():
        path = os.path.join(store_dir, filename)
        if not os.path.exists(path):
            print(f"Warning: Missing {path}")
            continue

        img = Image.open(path)
        if img.size != (exp_w, exp_h):
            print(f"Resizing {filename} from {img.size} to ({exp_w}, {exp_h})")
            img = img.resize((exp_w, exp_h), Image.Resampling.LANCZOS)

        if mode == "RGB" and img.mode != "RGB":
            # Flatten to RGB on dark background
            bg = Image.new("RGB", img.size, (11, 16, 33))
            if img.mode == "RGBA":
                bg.paste(img, (0, 0), img)
            else:
                bg.paste(img, (0, 0))
            img = bg
        elif mode == "RGBA" and img.mode != "RGBA":
            img = img.convert("RGBA")

        # Save with clean standard PNG chunks
        img.save(path, format="PNG", optimize=True)
        print(f"✓ Verified & Saved: {filename} [{img.mode}, {img.size[0]}x{img.size[1]} px, {os.path.getsize(path)} bytes]")


if __name__ == "__main__":
    fix_and_verify_store_assets()
