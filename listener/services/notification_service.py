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

"""Service for triggering platform-native notifications and managing watch queues."""

import logging
import platform
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)


class NotificationService:
    """Dispatches system notifications across macOS and Linux platforms."""

    def __init__(self, system_platform: Optional[str] = None):
        """Initialize notification service.

        Args:
            system_platform: Optional platform override ('Darwin', 'Linux') for testing.
        """
        self.platform = system_platform or platform.system()

    def show_system_notification(self, title: str, body: str) -> bool:
        """Display a system notification using native OS capabilities.

        On macOS: Uses AppleScript `display notification`.
        On Linux: Uses `notify-send`.

        Args:
            title: Notification title string.
            body: Notification body message string.

        Returns:
            True if notification command succeeded, False otherwise.
        """
        if not title and not body:
            logger.warning("Attempted to show empty notification.")
            return False

        safe_title = (title or "Antigravity").replace('"', '\\"')
        safe_body = (body or "").replace('"', '\\"')

        try:
            if self.platform == "Darwin":
                script = f'display notification "{safe_body}" with title "{safe_title}"'
                subprocess.run(
                    ["osascript", "-e", script],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                logger.info("macOS system notification displayed: %s - %s", title, body)
                return True
            elif self.platform == "Linux":
                subprocess.run(
                    ["notify-send", safe_title, safe_body],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                logger.info("Linux system notification displayed: %s - %s", title, body)
                return True
            else:
                logger.warning(
                    "Unsupported platform for native notification: %s", self.platform
                )
                return False
        except Exception as err:
            logger.error("Failed to display system notification: %s", err)
            return False
