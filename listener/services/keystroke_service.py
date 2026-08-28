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

"""Service for dispatching keystrokes to the active OS window."""

import logging
import platform
import subprocess
import time
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class KeystrokeService:
    """Dispatches synthetic keystroke events into the application window."""

    def __init__(self, target_app: Optional[str] = "active") -> None:
        """Initialize KeystrokeService and detect host platform.

        Args:
            target_app: Target app name (e.g. 'Cursor', 'Antigravity', 'active').
        """
        self.os_type = platform.system()
        self.target_app = target_app

    def _execute_command(self, cmd: list[str]) -> Tuple[int, str, str]:
        """Execute a system subprocess command.

        Args:
            cmd: Command arguments list.

        Returns:
            Tuple of (returncode, stdout, stderr).
        """
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode, result.stdout, result.stderr

    def send_keystrokes(
        self,
        text: str,
        auto_enter: bool = True,
        target_app: Optional[str] = None,
        delay_seconds: float = 0.0,
    ) -> bool:
        """Inject keystrokes into the system window.

        Args:
            text: String text to type.
            auto_enter: If True, simulate pressing Return key after typing.
            target_app: Optional application name override to focus before typing.
            delay_seconds: Optional delay before keystroke dispatch.

        Returns:
            True if execution succeeded, False otherwise.

        Raises:
            ValueError: If text is empty or invalid.
        """
        if not text:
            raise ValueError("Text to inject cannot be empty.")

        if delay_seconds > 0:
            time.sleep(delay_seconds)

        app_to_target = target_app if target_app is not None else self.target_app
        logger.info(
            "Injecting keystrokes: '%s' (auto_enter=%s, target_app=%s)",
            text,
            auto_enter,
            app_to_target,
        )

        if self.os_type == "Darwin":
            escaped_text = text.replace("\\", "\\\\").replace('"', '\\"')
            script_lines = []

            # Only activate specific application if not set to active/current/none
            if app_to_target and app_to_target.lower() not in (
                "active",
                "current",
                "none",
                "",
            ):
                # Map shorthand names
                app_name = app_to_target
                if app_name.lower() == "terminal":
                    app_name = "Terminal"
                elif app_name.lower() == "iterm":
                    app_name = "iTerm2"
                elif app_name.lower() == "vscode":
                    app_name = "Visual Studio Code"

                script_lines.append("try")
                script_lines.append(f'    tell application "{app_name}" to activate')
                script_lines.append("on error")
                script_lines.append("    try")
                script_lines.append(
                    f'        tell application "{app_name}.app" to activate'
                )
                script_lines.append("    on error")
                script_lines.append("    end try")
                script_lines.append("end try")
                script_lines.append("delay 0.1")

            script_lines.append(
                f'tell application "System Events" to keystroke "{escaped_text}"'
            )
            if auto_enter:
                script_lines.append('tell application "System Events" to key code 36')

            script = "\n".join(script_lines)
            return_code, _, stderr = self._execute_command(["osascript", "-e", script])
            if return_code != 0:
                logger.error(
                    "Failed to inject keystrokes via AppleScript: %s",
                    stderr,
                )
                return False
            return True

        if self.os_type == "Linux":
            return_code, _, stderr = self._execute_command(["xdotool", "type", text])
            if auto_enter and return_code == 0:
                self._execute_command(["xdotool", "key", "Return"])
            if return_code != 0:
                logger.error(
                    "Failed to inject keystrokes via xdotool: %s",
                    stderr,
                )
                return False
            return True

        logger.warning(
            "Unsupported platform '%s' for automated keystroke injection.",
            self.os_type,
        )
        return False
