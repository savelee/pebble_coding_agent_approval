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

"""Configuration settings for Pebble Agent Approvals listener."""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = False
    target_app: Optional[str] = "active"
    confirm_text: str = "i confirm"
    disapprove_text: str = "i disapprove"
    auto_enter: bool = True

    model_config = SettingsConfigDict(
        env_prefix="PEBBLE_",
        case_sensitive=False,
    )


settings = Settings()
