/*
 * Copyright 2026 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#pragma once

#include <pebble.h>

#if __has_include("message_keys.auto.h")
#include "message_keys.auto.h"
#endif

#ifndef MESSAGE_KEY_ACTION
#define MESSAGE_KEY_ACTION 0
#endif

#ifndef MESSAGE_KEY_STATUS
#define MESSAGE_KEY_STATUS 1
#endif

#ifndef MESSAGE_KEY_HOST
#define MESSAGE_KEY_HOST 2
#endif

#ifndef MESSAGE_KEY_PORT
#define MESSAGE_KEY_PORT 3
#endif

#define ACTION_CONFIRM 0
#define ACTION_DISAPPROVE 1

/**
 * Initialize and push the main UI window to the window stack.
 */
void ui_init(void);

/**
 * Deinitialize and destroy UI window resources.
 */
void ui_deinit(void);

/**
 * Update the status text displayed in the UI.
 *
 * @param status_msg Null-terminated string indicating current action status.
 */
void ui_set_status(const char *status_msg);
