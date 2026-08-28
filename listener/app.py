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

"""Flask application serving HTTP endpoints for Pebble Agent Approvals."""

import logging
from typing import Any, Dict, List, Optional

from flask import Flask, jsonify, request

from listener.config import settings
from listener.services.keystroke_service import KeystrokeService
from listener.services.notification_service import NotificationService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_app(
    keystroke_service: Optional[KeystrokeService] = None,
    notification_service: Optional[NotificationService] = None,
) -> Flask:
    """Create and configure the Flask listener application.

    Args:
        keystroke_service: Optional injected KeystrokeService instance.
        notification_service: Optional injected NotificationService instance.

    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)
    service = keystroke_service or KeystrokeService(target_app=settings.target_app)
    notif_service = notification_service or NotificationService()
    notifications_queue: List[Dict[str, Any]] = []

    @app.route("/healthz", methods=["GET"])
    def health_check():
        """Health check endpoint to verify listener availability.

        Returns:
            JSON response with service status.
        """
        return (
            jsonify(
                {
                    "status": "ok",
                    "service": "pebble-approvals-listener",
                    "target_app": settings.target_app,
                }
            ),
            200,
        )

    @app.route("/api/action", methods=["POST"])
    def handle_action():
        """Handle incoming button action triggered from Pebble smartwatch.

        Expected JSON payload:
            {"action": "confirm"} or {"action": "disapprove"}
            Optional: {"text": "custom text", "target_app": "Antigravity", "delay": 2.0}

        Returns:
            JSON response containing dispatch status and injected text.
        """
        data = request.get_json(silent=True)
        if not data:
            return (
                jsonify(
                    {
                        "error": "Invalid or missing JSON payload.",
                        "status": "error",
                    }
                ),
                400,
            )

        action = data.get("action")
        custom_text = data.get("text")
        target_app_override = data.get("target_app")
        delay_override = float(data.get("delay", 0.0))

        if custom_text:
            text_to_send = custom_text
        elif action == "confirm":
            text_to_send = settings.confirm_text
        elif action == "disapprove":
            text_to_send = settings.disapprove_text
        else:
            return (
                jsonify(
                    {
                        "error": (
                            f"Unsupported action '{action}'. "
                            "Use 'confirm' or 'disapprove'."
                        ),
                        "status": "error",
                    }
                ),
                400,
            )

        success = service.send_keystrokes(
            text=text_to_send,
            auto_enter=settings.auto_enter,
            target_app=target_app_override,
            delay_seconds=delay_override,
        )

        if not success:
            return (
                jsonify(
                    {
                        "error": "Failed to dispatch keystrokes to active window.",
                        "status": "failure",
                        "text_sent": text_to_send,
                    }
                ),
                500,
            )

        return (
            jsonify(
                {
                    "status": "success",
                    "action": action,
                    "text_sent": text_to_send,
                }
            ),
            200,
        )

    @app.route("/api/notify", methods=["POST"])
    def handle_notify():
        """Stage or dispatch notification message for Pebble and system.

        Expected JSON payload:
            {"title": "...", "body": "..."} or {"message": "...", "title": "..."}

        Returns:
            JSON response acknowledging notification enqueue and broadcast.
        """
        data = request.get_json(silent=True)
        if not data:
            return (
                jsonify(
                    {
                        "error": "Missing JSON payload.",
                        "status": "error",
                    }
                ),
                400,
            )

        body = data.get("body") or data.get("message")
        title = data.get("title", "Antigravity")

        if not body:
            return (
                jsonify(
                    {
                        "error": "Notification must include 'body' or 'message'.",
                        "status": "error",
                    }
                ),
                400,
            )

        payload = {"title": title, "body": body}
        notifications_queue.append(payload)

        # Trigger native OS notification (forwards to connected Bluetooth devices)
        notif_service.show_system_notification(title=title, body=body)

        logger.info(
            "Dispatched notification: %s - %s",
            title,
            body,
        )
        return (
            jsonify(
                {
                    "status": "enqueued",
                    "title": title,
                    "body": body,
                    "total_pending": len(notifications_queue),
                }
            ),
            200,
        )

    @app.route("/api/notifications", methods=["GET"])
    def get_notifications():
        """Retrieve and drain pending notifications for Pebble client.

        Returns:
            JSON list of queued notification messages.
        """
        pending = list(notifications_queue)
        notifications_queue.clear()
        return jsonify({"notifications": pending}), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host=settings.host,
        port=settings.port,
        debug=settings.debug,
    )
