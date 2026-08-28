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

"""CLI tool to send notifications from terminal or AI agents to Pebble listener."""

import argparse
import json
import sys
import urllib.error
import urllib.request

from listener.config import settings


def send_notification(
    message: str,
    title: str = "Antigravity",
    host: str = "127.0.0.1",
    port: int = 5000,
) -> bool:
    """Send notification payload to the local listener endpoint.

    Args:
        message: Notification message text.
        title: Notification title (defaults to 'Antigravity').
        host: Target listener host.
        port: Target listener port.

    Returns:
        True if successfully sent, False otherwise.
    """
    url = f"http://{host}:{port}/api/notify"
    payload = json.dumps({"title": title, "body": message}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            if 200 <= resp.status < 300:
                print(f"✓ Notification dispatched to Pebble: '{title}' - '{message}'")
                return True
            else:
                print(f"✗ Listener returned status: {resp.status}", file=sys.stderr)
                return False
    except Exception as err:
        print(f"✗ Failed to connect to listener at {url}: {err}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Send agent notifications to Pebble watch via local listener.",
    )
    parser.add_argument(
        "message",
        nargs="?",
        default=None,
        help="Notification message text (or read from stdin).",
    )
    parser.add_argument(
        "--title",
        "-t",
        default="Antigravity",
        help="Notification title (default: Antigravity).",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Listener host (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=settings.port,
        help=f"Listener port (default: {settings.port}).",
    )

    args = parser.parse_args()

    if args.message:
        msg = args.message
    elif not sys.stdin.isatty():
        msg = sys.stdin.read().strip()
    else:
        print(
            "Usage: python -m listener.notify 'Message' or pipe via stdin",
            file=sys.stderr,
        )
        sys.exit(1)

    if not msg:
        print("Error: Empty notification message.", file=sys.stderr)
        sys.exit(1)

    success = send_notification(
        message=msg,
        title=args.title,
        host=args.host,
        port=args.port,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
