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

"""Unit tests for notify CLI tool."""

from unittest.mock import MagicMock, patch

import pytest

from listener.notify import main, send_notification


def test_send_notification_success():
    """Verify send_notification with successful HTTP response."""
    with patch("urllib.request.urlopen") as mock_open:
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__.return_value = mock_resp
        mock_open.return_value = mock_resp

        success = send_notification("Hello Antigravity", title="Agent")
        assert success is True


def test_send_notification_http_error():
    """Verify send_notification when HTTP status is not 2xx."""
    with patch("urllib.request.urlopen") as mock_open:
        mock_resp = MagicMock()
        mock_resp.status = 500
        mock_resp.__enter__.return_value = mock_resp
        mock_open.return_value = mock_resp

        success = send_notification("Failed message")
        assert success is False


def test_send_notification_network_exception():
    """Verify send_notification handles network failure."""
    with patch("urllib.request.urlopen", side_effect=Exception("Connection refused")):
        success = send_notification("Failed message")
        assert success is False


def test_notify_cli_with_args():
    """Verify CLI execution with positional arguments."""
    with patch("listener.notify.send_notification", return_value=True):
        with patch("sys.argv", ["notify.py", "Test message", "--title", "CLI"]):
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 0
