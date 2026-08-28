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

"""Generate a 28x28 menu icon PNG for Pebble application."""

import os
import struct
import zlib


def create_app_icon_png(target_path: str) -> None:
    width = 28
    height = 28

    # 28x28 RGBA image buffer
    # Draw a rounded badge with green checkmark (top) and red cross (bottom)
    pixels = bytearray(width * height * 4)

    for y in range(height):
        for x in range(width):
            idx = (y * width + x) * 4
            dx = x - 13.5
            dy = y - 13.5
            dist = (dx * dx + dy * dy) ** 0.5

            if dist > 13.5:
                # Transparent outside circle
                pixels[idx:idx + 4] = b"\x00\x00\x00\x00"
            elif dist > 12.0:
                # Border
                pixels[idx:idx + 4] = b"\x0b\x1a\x30\xff"  # Dark navy
            elif y < 14:
                # Top half: Kelly green
                # Draw checkmark in white
                is_check = (
                    (x == 8 and y == 7) or
                    (x == 9 and y == 8) or
                    (x == 10 and y == 9) or
                    (x == 11 and y == 8) or
                    (x == 12 and y == 7) or
                    (x == 13 and y == 6) or
                    (x == 14 and y == 5) or
                    (x == 15 and y == 4)
                )
                if is_check:
                    pixels[idx:idx + 4] = b"\xff\xff\xff\xff"
                else:
                    pixels[idx:idx + 4] = b"\x00\x87\x5a\xff"
            else:
                # Bottom half: Red
                # Draw cross in white
                is_cross = (
                    (abs(x - 14) == abs(y - 20) and 9 <= x <= 19) or
                    (abs(x - 14) == abs(20 - y) and 9 <= x <= 19)
                )
                if is_cross:
                    pixels[idx:idx + 4] = b"\xff\xff\xff\xff"
                else:
                    pixels[idx:idx + 4] = b"\xd9\x38\x1e\xff"

    # Encode raw scanlines for PNG (each line prefixed with filter byte 0)
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)  # Filter type None
        raw_data.extend(pixels[y * width * 4:(y + 1) * width * 4])

    def chunk(chunk_type: bytes, data: bytes) -> bytes:
        length = struct.pack(">I", len(data))
        crc = struct.pack(">I", zlib.crc32(chunk_type + data) & 0xffffffff)
        return length + chunk_type + data + crc

    # PNG Signature
    png = b"\x89PNG\r\n\x1a\n"
    # IHDR
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    png += chunk(b"IHDR", ihdr)
    # IDAT
    compressed = zlib.compress(bytes(raw_data), 9)
    png += chunk(b"IDAT", compressed)
    # IEND
    png += chunk(b"IEND", b"")

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "wb") as f:
        f.write(png)
    print(f"Generated {target_path} successfully.")


if __name__ == "__main__":
    create_app_icon_png("pebble_app/resources/images/app_icon.png")
