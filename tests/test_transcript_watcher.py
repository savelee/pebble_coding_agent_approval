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

from listener.services.transcript_watcher import TranscriptWatcher


def test_transcript_watcher_summary_extraction():
    """Verify clean 1-line summary extraction from various markdown agent texts."""
    watcher = TranscriptWatcher()

    assert watcher.extract_summary("") is None
    assert watcher.extract_summary("   \n  \n") is None

    # Header extraction
    header_text = "# Proposal for Pebble Agent Approvals\nSome details here."
    assert watcher.extract_summary(header_text) == "Proposal for Pebble Agent Approvals"

    # Confirmation / question phrase extraction
    question_text = (
        "Analysis complete.\nDo you want to confirm this implementation plan?"
    )
    assert "confirm" in watcher.extract_summary(question_text).lower()

    # Generic first line
    prose_text = "All 25 unit tests have passed successfully!"
    assert (
        watcher.extract_summary(prose_text)
        == "All 25 unit tests have passed successfully!"
    )


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
        assert notifications_received[0][1] == "Test Agent Answer"


def test_transcript_watcher_start_stop():
    """Verify thread lifecycle start and stop."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        watcher = TranscriptWatcher(base_dir=tmp_dir, poll_interval=0.05)
        watcher.start()
        assert watcher._running is True
        time.sleep(0.1)
        watcher.stop()
        assert watcher._running is False
