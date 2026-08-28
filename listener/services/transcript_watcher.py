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

"""Background watcher for conversation transcripts to stream agent responses."""

import glob
import json
import logging
import os
import re
import threading
import time
from typing import Callable, Optional

logger = logging.getLogger(__name__)


def clean_markdown_text(text: str) -> str:
    """Remove markdown links, bold, code ticks, and special formatting."""
    # Convert [label](url) -> label
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    # Remove markdown headers and list bullets
    text = re.sub(r"^[\#\*\-\>\s]+", "", text)
    # Remove bold, italics, inline code ticks
    text = re.sub(r"[\*\_`]", "", text)
    return text.strip()


class TranscriptWatcher:
    """Monitors active Antigravity transcript logs and notifies on agent updates."""

    def __init__(
        self,
        base_dir: Optional[str] = None,
        on_notification: Optional[Callable[[str, str], None]] = None,
        poll_interval: float = 1.5,
    ) -> None:
        """Initialize transcript watcher.

        Args:
            base_dir: Custom base directory for transcripts (defaults to Antigravity).
            on_notification: Callback function receiving (title, body).
            poll_interval: Polling frequency in seconds.
        """
        self.base_dir = base_dir or os.path.expanduser("~/.gemini/antigravity/brain")
        self.on_notification = on_notification
        self.poll_interval = poll_interval
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._last_file: Optional[str] = None
        self._last_position: int = 0

    def find_latest_transcript(self) -> Optional[str]:
        """Find the most recently modified transcript.jsonl log file.

        Returns:
            Absolute filepath string or None if no transcript exists.
        """
        pattern = os.path.join(
            self.base_dir, "*", ".system_generated", "logs", "transcript.jsonl"
        )
        files = glob.glob(pattern)
        if not files:
            return None
        return max(files, key=os.path.getmtime)

    def extract_summary(self, content: str) -> Optional[str]:
        """Extract a clean, concise summary prioritizing questions and actions.

        Args:
            content: Raw string content from planner response.

        Returns:
            Concise summary string or None if content is not notify-worthy.
        """
        if not content:
            return None

        lines = [line.strip() for line in content.splitlines() if line.strip()]
        if not lines:
            return None

        # Priority 1: Direct questions asking for user input or approval
        for line in lines:
            if "?" in line and len(line) > 10 and not line.startswith("### FAQ"):
                cleaned = clean_markdown_text(line)
                if len(cleaned) > 10:
                    return cleaned[:180]

        # Priority 2: Confirmation / action prompts
        for line in lines:
            lower = line.lower()
            if (
                "confirm" in lower
                or "approve" in lower
                or "disapprove" in lower
                or "proceed" in lower
            ):
                if not line.startswith("1.") and not line.startswith("*"):
                    cleaned = clean_markdown_text(line)
                    if len(cleaned) > 10:
                        return cleaned[:180]

        # Priority 3: First meaningful header
        for line in lines:
            if line.startswith("#"):
                cleaned = clean_markdown_text(line)
                if cleaned:
                    return cleaned[:180]

        # Priority 4: First non-empty prose line
        for line in lines:
            cleaned = clean_markdown_text(line)
            if len(cleaned) > 8:
                return cleaned[:180]

        return None

    def check_for_updates(self) -> None:
        """Poll the active transcript file for new agent response steps."""
        latest_file = self.find_latest_transcript()
        if not latest_file:
            return

        if latest_file != self._last_file:
            self._last_file = latest_file
            try:
                size = os.path.getsize(latest_file)
                self._last_position = max(0, size - 2048)
            except OSError:
                self._last_position = 0

        try:
            with open(latest_file, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(self._last_position)
                new_lines = f.readlines()
                self._last_position = f.tell()

            for line in new_lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    if (
                        record.get("source") == "MODEL"
                        and record.get("type") == "PLANNER_RESPONSE"
                    ):
                        content = record.get("content")
                        if content:
                            summary = self.extract_summary(content)
                            if summary and self.on_notification:
                                logger.info(
                                    "Transcript watcher detected response: %s",
                                    summary,
                                )
                                self.on_notification("Antigravity", summary)
                except Exception as parse_err:
                    logger.debug("Skipping unparseable transcript line: %s", parse_err)
        except Exception as err:
            logger.debug("Error reading transcript file: %s", err)

    def _loop(self) -> None:
        while self._running:
            self.check_for_updates()
            time.sleep(self.poll_interval)

    def start(self) -> None:
        """Start the background watcher thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info("TranscriptWatcher started monitoring in background.")

    def stop(self) -> None:
        """Stop the background watcher thread."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
            self._thread = None
