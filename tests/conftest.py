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

"""Pytest fixtures for Pebble Agent Approvals listener tests."""

from unittest.mock import MagicMock

import pytest

from listener.app import create_app
from listener.services.keystroke_service import KeystrokeService


@pytest.fixture
def mock_keystroke_service():
    """Fixture providing a mocked KeystrokeService."""
    service = MagicMock(spec=KeystrokeService)
    service.send_keystrokes.return_value = True
    return service


@pytest.fixture
def test_client(mock_keystroke_service):
    """Fixture providing a Flask test client with injected mock service."""
    app = create_app(keystroke_service=mock_keystroke_service)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
