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

#include "splash.h"
#include "ui.h"
#include <pebble.h>

static void inbox_received_callback(DictionaryIterator *iterator, void *context) {
  // Check for incoming prompt text notification
  Tuple *prompt_tuple = dict_find(iterator, MESSAGE_KEY_PROMPT_TEXT);
  if (prompt_tuple) {
    ui_set_prompt_text(prompt_tuple->value->cstring);
    return;
  }

  // Check for status feedback
  Tuple *status_tuple = dict_find(iterator, MESSAGE_KEY_STATUS);
  if (status_tuple) {
    ui_set_status(status_tuple->value->cstring);
    if (strcmp(status_tuple->value->cstring, "SENT OK") == 0) {
      vibes_short_pulse();
    } else if (strcmp(status_tuple->value->cstring, "NET ERROR") == 0) {
      vibes_double_pulse();
    }
  }
}

static void inbox_dropped_callback(AppMessageResult reason, void *context) {
  APP_LOG(APP_LOG_LEVEL_ERROR, "AppMessage inbox dropped: %d", reason);
  ui_set_status("INBOX ERROR");
}

static void outbox_failed_callback(DictionaryIterator *iterator, AppMessageResult reason, void *context) {
  APP_LOG(APP_LOG_LEVEL_ERROR, "AppMessage outbox failed: %d", reason);
  ui_set_status("SEND FAILED");
  vibes_double_pulse();
}

static void outbox_sent_callback(DictionaryIterator *iterator, void *context) {
  APP_LOG(APP_LOG_LEVEL_INFO, "AppMessage outbox send success.");
}

static void init(void) {
  // Launch with branded splash screen
  splash_init();

  // Register AppMessage callbacks
  app_message_register_inbox_received(inbox_received_callback);
  app_message_register_inbox_dropped(inbox_dropped_callback);
  app_message_register_outbox_failed(outbox_failed_callback);
  app_message_register_outbox_sent(outbox_sent_callback);

  const uint32_t inbox_size = 512;
  const uint32_t outbox_size = 256;
  app_message_open(inbox_size, outbox_size);
}

static void deinit(void) {
  app_message_deregister_callbacks();
  splash_deinit();
  ui_deinit();
}

int main(void) {
  init();
  app_event_loop();
  deinit();
}
