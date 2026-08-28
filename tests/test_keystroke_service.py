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

"""Unit tests for KeystrokeService."""

from unittest.mock import patch

import pytest

from listener.services.keystroke_service import KeystrokeService


def test_execute_command():
    """Verify _execute_command executes subprocess correctly."""
    service = KeystrokeService()
    code, stdout, stderr = service._execute_command(["echo", "hello"])
    assert code == 0
    assert "hello" in stdout


def test_send_keystrokes_empty_text_raises_value_error():
    """Verify ValueError is raised if input text is empty."""
    service = KeystrokeService()
    with pytest.raises(ValueError, match="cannot be empty"):
        service.send_keystrokes("")


def test_send_keystrokes_darwin_with_target_app():
    """Verify AppleScript activates target application before typing."""
    service = KeystrokeService(target_app="Antigravity")
    service.os_type = "Darwin"

    with patch.object(service, "_execute_command") as mock_exec:
        mock_exec.return_value = (0, "", "")
        result = service.send_keystrokes(
            "i confirm",
            auto_enter=True,
            delay_seconds=0.01,
        )

        assert result is True
        mock_exec.assert_called_once()
        args = mock_exec.call_args[0][0]
        assert args[0] == "osascript"
        assert 'tell application "Antigravity" to activate' in args[2]
        assert 'keystroke "i confirm"' in args[2]
        assert "key code 36" in args[2]


def test_send_keystrokes_darwin_without_target_app():
    """Verify AppleScript without target application."""
    service = KeystrokeService(target_app=None)
    service.os_type = "Darwin"

    with patch.object(service, "_execute_command") as mock_exec:
        mock_exec.return_value = (0, "", "")
        result = service.send_keystrokes(
            "i confirm",
            auto_enter=False,
        )

        assert result is True
        mock_exec.assert_called_once()
        args = mock_exec.call_args[0][0]
        assert "activate" not in args[2]


def test_send_keystrokes_darwin_failure():
    """Verify return False when AppleScript command fails."""
    service = KeystrokeService()
    service.os_type = "Darwin"

    with patch.object(service, "_execute_command") as mock_exec:
        mock_exec.return_value = (1, "", "osascript error")
        result = service.send_keystrokes("i confirm", auto_enter=False)

        assert result is False
        mock_exec.assert_called_once()


def test_send_keystrokes_linux_success():
    """Verify xdotool command execution on Linux."""
    service = KeystrokeService()
    service.os_type = "Linux"

    with patch.object(service, "_execute_command") as mock_exec:
        mock_exec.return_value = (0, "", "")
        result = service.send_keystrokes("i disapprove", auto_enter=True)

        assert result is True
        assert mock_exec.call_count == 2
        mock_exec.assert_any_call(["xdotool", "type", "i disapprove"])
        mock_exec.assert_any_call(["xdotool", "key", "Return"])


def test_send_keystrokes_linux_failure():
    """Verify return False when Linux xdotool command fails."""
    service = KeystrokeService()
    service.os_type = "Linux"

    with patch.object(service, "_execute_command") as mock_exec:
        mock_exec.return_value = (1, "", "xdotool error")
        result = service.send_keystrokes("i disapprove", auto_enter=False)

        assert result is False
        mock_exec.assert_called_once_with(["xdotool", "type", "i disapprove"])


def test_send_keystrokes_unsupported_platform():
    """Verify return False on unsupported platform."""
    service = KeystrokeService()
    service.os_type = "FreeBSD"

    result = service.send_keystrokes("test")
    assert result is False
