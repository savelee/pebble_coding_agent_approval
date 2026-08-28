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

"""Unit tests for Flask listener HTTP endpoints."""


def test_healthz_endpoint(test_client):
    """Verify health check endpoint returns 200 and status ok."""
    response = test_client.get("/healthz")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "ok"
    assert json_data["service"] == "pebble-approvals-listener"


def test_action_confirm_success(test_client, mock_keystroke_service):
    """Verify confirm action triggers keystroke and returns success."""
    mock_keystroke_service.send_keystrokes.return_value = True
    response = test_client.post("/api/action", json={"action": "confirm"})

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert json_data["action"] == "confirm"
    assert json_data["text_sent"] == "i confirm"
    mock_keystroke_service.send_keystrokes.assert_called_once_with(
        text="i confirm",
        auto_enter=True,
        target_app=None,
        delay_seconds=0.0,
    )


def test_action_disapprove_success(test_client, mock_keystroke_service):
    """Verify disapprove action triggers keystroke and returns success."""
    mock_keystroke_service.send_keystrokes.return_value = True
    response = test_client.post("/api/action", json={"action": "disapprove"})

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert json_data["action"] == "disapprove"
    assert json_data["text_sent"] == "i disapprove"
    mock_keystroke_service.send_keystrokes.assert_called_once_with(
        text="i disapprove",
        auto_enter=True,
        target_app=None,
        delay_seconds=0.0,
    )


def test_action_custom_text(test_client, mock_keystroke_service):
    """Verify custom text and target_app overrides in payload."""
    mock_keystroke_service.send_keystrokes.return_value = True
    response = test_client.post(
        "/api/action",
        json={"text": "proceed now", "target_app": "Cursor", "delay": 1.0},
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert json_data["text_sent"] == "proceed now"
    mock_keystroke_service.send_keystrokes.assert_called_once_with(
        text="proceed now",
        auto_enter=True,
        target_app="Cursor",
        delay_seconds=1.0,
    )


def test_action_invalid_payload(test_client):
    """Verify 400 when body is not JSON."""
    response = test_client.post(
        "/api/action", data="not json", content_type="text/plain"
    )
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["status"] == "error"


def test_action_unknown_action(test_client):
    """Verify 400 when action value is unrecognized."""
    response = test_client.post("/api/action", json={"action": "unknown_cmd"})
    assert response.status_code == 400
    json_data = response.get_json()
    assert "Unsupported action" in json_data["error"]


def test_action_service_failure(test_client, mock_keystroke_service):
    """Verify 500 status when KeystrokeService fails."""
    mock_keystroke_service.send_keystrokes.return_value = False
    response = test_client.post("/api/action", json={"action": "confirm"})

    assert response.status_code == 500
    json_data = response.get_json()
    assert json_data["status"] == "failure"


def test_notify_and_get_notifications(test_client):
    """Verify enqueuing and draining notifications."""
    # Enqueue invalid notification
    bad_res = test_client.post("/api/notify", json={"invalid": "payload"})
    assert bad_res.status_code == 400

    # Enqueue valid notification
    notify_res = test_client.post(
        "/api/notify",
        json={
            "title": "Antigravity Prompt",
            "body": "Agent needs permission.",
        },
    )
    assert notify_res.status_code == 200
    assert notify_res.get_json()["status"] == "enqueued"

    # Drain notifications
    get_res = test_client.get("/api/notifications")
    assert get_res.status_code == 200
    items = get_res.get_json()["notifications"]
    assert len(items) == 1
    assert items[0]["title"] == "Antigravity Prompt"

    # Second drain is empty
    empty_res = test_client.get("/api/notifications")
    assert empty_res.get_json()["notifications"] == []
