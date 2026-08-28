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

"""Configuration settings for the Pebble Agent Approvals listener service."""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables.

    Attributes:
        host: The IP address or hostname to bind the Flask server.
        port: The TCP port for incoming Pebble HTTP requests.
        confirm_text: Text string to inject when confirmation action is received.
        disapprove_text: Text string to inject when disapproval action is received.
        auto_enter: Whether to append a newline / Return keystroke after typing.
        target_app: Optional target application name to focus before typing.
        debug: Whether to enable debug mode in Flask.
    """

    model_config = SettingsConfigDict(env_prefix="PEBBLE_")

    host: str = "0.0.0.0"
    port: int = 5000
    confirm_text: str = "i confirm"
    disapprove_text: str = "i disapprove"
    auto_enter: bool = True
    target_app: Optional[str] = "Antigravity"
    debug: bool = False


settings = Settings()
