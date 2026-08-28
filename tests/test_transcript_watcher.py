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

"""Unit tests for TranscriptWatcher service."""

import json
import os
import tempfile
import time

from listener.services.transcript_watcher import (
    TranscriptWatcher,
    clean_markdown_text,
)


def test_clean_markdown_text():
    """Verify markdown strip utility removes links, bullets, and headers."""
    assert clean_markdown_text("### Header Title") == "Header Title"
    assert (
        clean_markdown_text("* [Makefile](file:///path) updated") == "Makefile updated"
    )
    assert clean_markdown_text("**bold text** and `code`") == "bold text and code"


def test_transcript_watcher_summary_extraction():
    """Verify questions and prose results take priority over header titles."""
    watcher = TranscriptWatcher()

    assert watcher.extract_summary("") is None
    assert watcher.extract_summary("   \n  \n") is None

    # Question takes priority
    response_with_question = (
        "### Proposed Enhancement for Version 1.3\n"
        "Would you like me to update the project [Makefile](file:///) "
        "to add a unified make start target?"
    )
    extracted = watcher.extract_summary(response_with_question)
    assert extracted.startswith("Would you like me to update the project Makefile")

    # Prose result takes priority over headers
    response_with_result = (
        "Understood! We will keep the desktop listener lean and headless.\n"
        "## Flow Verified\n* Checked"
    )
    extracted_result = watcher.extract_summary(response_with_result)
    assert (
        extracted_result
        == "Understood! We will keep the desktop listener lean and headless."
    )

    # Header extraction fallback when only headers exist
    header_text = "# Initializing Test Suite\n"
    assert watcher.extract_summary(header_text) == "Initializing Test Suite"


def test_transcript_watcher_file_polling():
    """Verify watcher detects new lines appended to transcript.jsonl."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        log_dir = os.path.join(tmp_dir, "conv-123", ".system_generated", "logs")
        os.makedirs(log_dir, exist_ok=True)
        transcript_file = os.path.join(log_dir, "transcript.jsonl")

        # Initial seed
        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(json.dumps({"step_index": 0, "source": "SYSTEM"}) + "\n")

        notifications_received = []

        def on_notif(title, body):
            notifications_received.append((title, body))

        watcher = TranscriptWatcher(
            base_dir=tmp_dir, on_notification=on_notif, poll_interval=0.1
        )

        # Check latest file discovery
        assert watcher.find_latest_transcript() == transcript_file

        # Append agent response
        record = {
            "step_index": 1,
            "source": "MODEL",
            "type": "PLANNER_RESPONSE",
            "content": "# Test Agent Answer\nReady for approval.",
        }
        with open(transcript_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        watcher.check_for_updates()

        assert len(notifications_received) == 1
        assert notifications_received[0][0] == "Antigravity"
        assert notifications_received[0][1] == "Ready for approval."


def test_transcript_watcher_start_stop():
    """Verify thread lifecycle start and stop."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        watcher = TranscriptWatcher(base_dir=tmp_dir, poll_interval=0.05)
        watcher.start()
        assert watcher._running is True
        time.sleep(0.1)
        watcher.stop()
        assert watcher._running is False
