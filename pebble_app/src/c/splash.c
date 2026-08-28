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

static Window *s_splash_window;
static Layer *s_splash_canvas;
static AppTimer *s_splash_timer = NULL;

static void transition_to_main(void *data) {
  s_splash_timer = NULL;
  ui_init();
  if (s_splash_window) {
    window_stack_remove(s_splash_window, true);
  }
}

static void click_handler(ClickRecognizerRef recognizer, void *context) {
  if (s_splash_timer) {
    app_timer_cancel(s_splash_timer);
    s_splash_timer = NULL;
  }
  transition_to_main(NULL);
}

static void splash_click_config_provider(void *context) {
  window_single_click_subscribe(BUTTON_ID_SELECT, click_handler);
  window_single_click_subscribe(BUTTON_ID_UP, click_handler);
  window_single_click_subscribe(BUTTON_ID_DOWN, click_handler);
  window_single_click_subscribe(BUTTON_ID_BACK, click_handler);
}

static void splash_canvas_update_proc(Layer *layer, GContext *ctx) {
  GRect bounds = layer_get_bounds(layer);

  // 1. Background
  graphics_context_set_fill_color(ctx, GColorOxfordBlue);
  graphics_fill_rect(ctx, bounds, 0, GCornerNone);

  // 2. Title Header
  graphics_context_set_text_color(ctx, GColorWhite);
  graphics_draw_text(
      ctx,
      "AGENT APPROVALS",
      fonts_get_system_font(FONT_KEY_GOTHIC_18_BOLD),
      GRect(0, 4, bounds.size.w, 20),
      GTextOverflowModeWordWrap,
      GTextAlignmentCenter,
      NULL);

  // 3. Miniature Watch Layout Screenshot Preview Box
  int card_w = 64;
  int card_h = 74;
  int card_x = (bounds.size.w - card_w) / 2;
  int card_y = 26;

  // Outer bezel frame
  graphics_context_set_fill_color(ctx, GColorBlack);
  graphics_fill_rect(ctx, GRect(card_x - 3, card_y - 3, card_w + 6, card_h + 6), 4, GCornersAll);
  graphics_context_set_stroke_color(ctx, GColorWhite);
  graphics_context_set_stroke_width(ctx, 1);
  graphics_draw_round_rect(ctx, GRect(card_x - 3, card_y - 3, card_w + 6, card_h + 6), 4);

  // Top half of mini preview (Green with Checkmark)
  int mini_half_h = card_h / 2;
  graphics_context_set_fill_color(ctx, GColorKellyGreen);
  graphics_fill_rect(ctx, GRect(card_x, card_y, card_w, mini_half_h), 0, GCornerNone);

  int mini_top_cx = card_x + card_w / 2;
  int mini_top_cy = card_y + mini_half_h / 2;
  graphics_context_set_fill_color(ctx, GColorIslamicGreen);
  graphics_fill_circle(ctx, GPoint(mini_top_cx, mini_top_cy), 11);
  graphics_context_set_stroke_color(ctx, GColorWhite);
  graphics_context_set_stroke_width(ctx, 1);
  graphics_draw_circle(ctx, GPoint(mini_top_cx, mini_top_cy), 11);
  // Checkmark lines
  graphics_draw_line(ctx, GPoint(mini_top_cx - 5, mini_top_cy), GPoint(mini_top_cx - 2, mini_top_cy + 4));
  graphics_draw_line(ctx, GPoint(mini_top_cx - 2, mini_top_cy + 4), GPoint(mini_top_cx + 5, mini_top_cy - 3));

  // Bottom half of mini preview (Red with Cross)
  graphics_context_set_fill_color(ctx, GColorRed);
  graphics_fill_rect(ctx, GRect(card_x, card_y + mini_half_h, card_w, mini_half_h), 0, GCornerNone);

  int mini_bot_cx = card_x + card_w / 2;
  int mini_bot_cy = card_y + mini_half_h + mini_half_h / 2;
  graphics_context_set_fill_color(ctx, GColorDarkCandyAppleRed);
  graphics_fill_circle(ctx, GPoint(mini_bot_cx, mini_bot_cy), 11);
  graphics_context_set_stroke_color(ctx, GColorWhite);
  graphics_context_set_stroke_width(ctx, 1);
  graphics_draw_circle(ctx, GPoint(mini_bot_cx, mini_bot_cy), 11);
  // Cross lines
  graphics_draw_line(ctx, GPoint(mini_bot_cx - 4, mini_bot_cy - 4), GPoint(mini_bot_cx + 4, mini_bot_cy + 4));
  graphics_draw_line(ctx, GPoint(mini_bot_cx - 4, mini_bot_cy + 4), GPoint(mini_bot_cx + 4, mini_bot_cy - 4));

  // Divider line
  graphics_context_set_stroke_color(ctx, GColorBlack);
  graphics_draw_line(ctx, GPoint(card_x, card_y + mini_half_h), GPoint(card_x + card_w, card_y + mini_half_h));

  // 4. Detailed Explanation Text
  graphics_context_set_text_color(ctx, GColorWhite);
  graphics_draw_text(
      ctx,
      "Approve your coding agent (like Antigravity) from your wrist, with the Pebble Time 2 app (and web extension).",
      fonts_get_system_font(FONT_KEY_GOTHIC_14),
      GRect(6, card_y + card_h + 4, bounds.size.w - 12, 54),
      GTextOverflowModeWordWrap,
      GTextAlignmentCenter,
      NULL);

  // 5. Action prompt footer
  graphics_context_set_text_color(ctx, GColorCeleste);
  graphics_draw_text(
      ctx,
      "Press any button to start",
      fonts_get_system_font(FONT_KEY_GOTHIC_14_BOLD),
      GRect(0, bounds.size.h - 18, bounds.size.w, 16),
      GTextOverflowModeWordWrap,
      GTextAlignmentCenter,
      NULL);
}

static void splash_window_load(Window *window) {
  Layer *window_layer = window_get_root_layer(window);
  GRect bounds = layer_get_bounds(window_layer);

  s_splash_canvas = layer_create(bounds);
  layer_set_update_proc(s_splash_canvas, splash_canvas_update_proc);
  layer_add_child(window_layer, s_splash_canvas);

  // Timer for automatic transition after 4000ms (4 seconds)
  s_splash_timer = app_timer_register(4000, transition_to_main, NULL);
}

static void splash_window_unload(Window *window) {
  if (s_splash_timer) {
    app_timer_cancel(s_splash_timer);
    s_splash_timer = NULL;
  }
  layer_destroy(s_splash_canvas);
}

void splash_init(void) {
  if (!s_splash_window) {
    s_splash_window = window_create();
    window_set_click_config_provider(s_splash_window, splash_click_config_provider);
    window_set_window_handlers(
        s_splash_window,
        (WindowHandlers){
            .load = splash_window_load,
            .unload = splash_window_unload,
        });
  }
  window_stack_push(s_splash_window, true);
}

void splash_deinit(void) {
  if (s_splash_window) {
    window_destroy(s_splash_window);
    s_splash_window = NULL;
  }
}
