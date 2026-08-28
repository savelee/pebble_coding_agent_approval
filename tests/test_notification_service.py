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

"""Unit tests for NotificationService."""

from unittest.mock import patch

from listener.services.notification_service import NotificationService


def test_notification_service_empty():
    """Verify empty notification returns False."""
    svc = NotificationService(system_platform="Darwin")
    assert svc.show_system_notification("", "") is False


def test_notification_service_darwin_success():
    """Verify macOS osascript execution."""
    svc = NotificationService(system_platform="Darwin")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        success = svc.show_system_notification("Antigravity", "Task complete!")
        assert success is True
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "osascript" in args
        assert "Task complete!" in args[2]


def test_notification_service_linux_success():
    """Verify Linux notify-send execution."""
    svc = NotificationService(system_platform="Linux")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        success = svc.show_system_notification("Antigravity", "Build passed")
        assert success is True
        mock_run.assert_called_once_with(
            ["notify-send", "Antigravity", "Build passed"],
            check=True,
            capture_output=True,
            text=True,
        )


def test_notification_service_unsupported():
    """Verify unsupported platform returns False."""
    svc = NotificationService(system_platform="Windows")
    assert svc.show_system_notification("Title", "Body") is False


def test_notification_service_subprocess_error():
    """Verify subprocess error handling."""
    svc = NotificationService(system_platform="Darwin")
    with patch("subprocess.run", side_effect=Exception("Execution failed")):
        assert svc.show_system_notification("Title", "Body") is False
