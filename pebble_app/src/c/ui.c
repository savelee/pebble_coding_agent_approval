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

#include "ui.h"
#include <pebble.h>

static Window *s_main_window;
static Layer *s_canvas_layer;
static TextLayer *s_status_layer;
static char s_status_buffer[32] = "READY";

/**
 * Send action key to PebbleKit JS via AppMessage dictionary.
 *
 * @param action Integer action code (ACTION_CONFIRM or ACTION_DISAPPROVE).
 */
static void send_action(int action) {
  DictionaryIterator *iter;
  AppMessageResult result = app_message_outbox_begin(&iter);
  if (result == APP_MSG_OK) {
    dict_write_int(iter, MESSAGE_KEY_ACTION, &action, sizeof(int), true);
    app_message_outbox_send();
    vibes_short_pulse();
    if (action == ACTION_CONFIRM) {
      ui_set_status("CONFIRMING...");
    } else {
      ui_set_status("DISAPPROVING...");
    }
  } else {
    vibes_double_pulse();
    ui_set_status("OUTBOX BUSY");
  }
}

static void up_click_handler(ClickRecognizerRef recognizer, void *context) {
  send_action(ACTION_CONFIRM);
}

static void down_click_handler(ClickRecognizerRef recognizer, void *context) {
  send_action(ACTION_DISAPPROVE);
}

static void click_config_provider(void *context) {
  window_single_click_subscribe(BUTTON_ID_UP, up_click_handler);
  window_single_click_subscribe(BUTTON_ID_DOWN, down_click_handler);
}

/**
 * Draw a checkmark inside a bounding box.
 */
static void draw_checkmark(GContext *ctx, GPoint center, int radius) {
  graphics_context_set_stroke_width(ctx, 3);
  graphics_context_set_stroke_color(ctx, GColorWhite);

  // Checkmark line segments
  GPoint p1 = GPoint(center.x - radius / 2, center.y);
  GPoint p2 = GPoint(center.x - radius / 6, center.y + radius / 3);
  GPoint p3 = GPoint(center.x + radius / 2, center.y - radius / 3);

  graphics_draw_line(ctx, p1, p2);
  graphics_draw_line(ctx, p2, p3);
}

/**
 * Draw a cross (X) inside a bounding box.
 */
static void draw_cross(GContext *ctx, GPoint center, int radius) {
  graphics_context_set_stroke_width(ctx, 3);
  graphics_context_set_stroke_color(ctx, GColorWhite);

  int offset = radius / 3;
  graphics_draw_line(
      ctx,
      GPoint(center.x - offset, center.y - offset),
      GPoint(center.x + offset, center.y + offset));
  graphics_draw_line(
      ctx,
      GPoint(center.x - offset, center.y + offset),
      GPoint(center.x + offset, center.y - offset));
}

/**
 * Canvas layer update procedure rendering split screen and icons.
 */
static void canvas_update_proc(Layer *layer, GContext *ctx) {
  GRect bounds = layer_get_bounds(layer);
  int header_height = 22;
  int usable_height = bounds.size.h - header_height;
  int half_height = usable_height / 2;
  int top_start_y = header_height;
  int bottom_start_y = header_height + half_height;

  // 1. Draw Top Half (Kelly Green Confirm)
  GRect top_rect = GRect(0, top_start_y, bounds.size.w, half_height);
  graphics_context_set_fill_color(ctx, GColorKellyGreen);
  graphics_fill_rect(ctx, top_rect, 0, GCornerNone);

  // Circle button for Confirm
  GPoint top_center = GPoint(bounds.size.w / 2, top_start_y + half_height / 2 - 10);
  int circle_radius = 20;
  graphics_context_set_fill_color(ctx, GColorIslamicGreen);
  graphics_fill_circle(ctx, top_center, circle_radius);
  graphics_context_set_stroke_color(ctx, GColorWhite);
  graphics_context_set_stroke_width(ctx, 2);
  graphics_draw_circle(ctx, top_center, circle_radius);
  draw_checkmark(ctx, top_center, circle_radius);

  // Top Label
  graphics_context_set_text_color(ctx, GColorWhite);
  graphics_draw_text(
      ctx,
      "CONFIRM [UP]",
      fonts_get_system_font(FONT_KEY_GOTHIC_14_BOLD),
      GRect(0, top_start_y + half_height - 20, bounds.size.w, 16),
      GTextOverflowModeWordWrap,
      GTextAlignmentCenter,
      NULL);

  // 2. Draw Bottom Half (Red Disapprove)
  GRect bottom_rect = GRect(0, bottom_start_y, bounds.size.w, half_height);
  graphics_context_set_fill_color(ctx, GColorRed);
  graphics_fill_rect(ctx, bottom_rect, 0, GCornerNone);

  // Circle button for Disapprove
  GPoint bottom_center = GPoint(bounds.size.w / 2, bottom_start_y + half_height / 2 - 10);
  graphics_context_set_fill_color(ctx, GColorDarkCandyAppleRed);
  graphics_fill_circle(ctx, bottom_center, circle_radius);
  graphics_context_set_stroke_color(ctx, GColorWhite);
  graphics_context_set_stroke_width(ctx, 2);
  graphics_draw_circle(ctx, bottom_center, circle_radius);
  draw_cross(ctx, bottom_center, circle_radius);

  // Bottom Label
  graphics_draw_text(
      ctx,
      "DISAPPROVE [DOWN]",
      fonts_get_system_font(FONT_KEY_GOTHIC_14_BOLD),
      GRect(0, bottom_start_y + half_height - 20, bounds.size.w, 16),
      GTextOverflowModeWordWrap,
      GTextAlignmentCenter,
      NULL);

  // 3. Middle dividing line
  graphics_context_set_stroke_color(ctx, GColorBlack);
  graphics_context_set_stroke_width(ctx, 2);
  graphics_draw_line(
      ctx,
      GPoint(0, bottom_start_y),
      GPoint(bounds.size.w, bottom_start_y));
}

void ui_set_status(const char *status_msg) {
  if (!status_msg || !s_status_layer) {
    return;
  }
  snprintf(s_status_buffer, sizeof(s_status_buffer), "%s", status_msg);
  text_layer_set_text(s_status_layer, s_status_buffer);
}

static void main_window_load(Window *window) {
  Layer *window_layer = window_get_root_layer(window);
  GRect bounds = layer_get_bounds(window_layer);

  // Create canvas layer for split background & custom graphics
  s_canvas_layer = layer_create(bounds);
  layer_set_update_proc(s_canvas_layer, canvas_update_proc);
  layer_add_child(window_layer, s_canvas_layer);

  // Dedicated Top Status Header Bar (never overlaps button content)
  int header_height = 22;
  s_status_layer = text_layer_create(GRect(0, 0, bounds.size.w, header_height));
  text_layer_set_background_color(s_status_layer, GColorBlack);
  text_layer_set_text_color(s_status_layer, GColorYellow);
  text_layer_set_font(s_status_layer, fonts_get_system_font(FONT_KEY_GOTHIC_14_BOLD));
  text_layer_set_text_alignment(s_status_layer, GTextAlignmentCenter);
  text_layer_set_text(s_status_layer, s_status_buffer);
  layer_add_child(window_layer, text_layer_get_layer(s_status_layer));
}

static void main_window_unload(Window *window) {
  text_layer_destroy(s_status_layer);
  layer_destroy(s_canvas_layer);
}

void ui_init(void) {
  s_main_window = window_create();
  window_set_click_config_provider(s_main_window, click_config_provider);
  window_set_window_handlers(
      s_main_window,
      (WindowHandlers){
          .load = main_window_load,
          .unload = main_window_unload,
      });
  window_stack_push(s_main_window, true);
}

void ui_deinit(void) {
  window_destroy(s_main_window);
}
