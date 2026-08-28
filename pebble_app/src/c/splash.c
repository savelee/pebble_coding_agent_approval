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
static bool s_has_transitioned = false;

static void transition_to_main(void *data) {
  if (s_has_transitioned) {
    return;
  }
  s_has_transitioned = true;
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
}

static void splash_canvas_update_proc(Layer *layer, GContext *ctx) {
  GRect bounds = layer_get_bounds(layer);

  // Background
  graphics_context_set_fill_color(ctx, GColorOxfordBlue);
  graphics_fill_rect(ctx, bounds, 0, GCornerNone);

  // Center Badge
  int center_x = bounds.size.w / 2;
  int center_y = bounds.size.h / 2 - 20;

  // Outer ring
  graphics_context_set_stroke_color(ctx, GColorCeleste);
  graphics_context_set_stroke_width(ctx, 2);
  graphics_draw_circle(ctx, GPoint(center_x, center_y), 28);

  // Dual color inner icons (Green check on left, Red cross on right)
  graphics_context_set_fill_color(ctx, GColorKellyGreen);
  graphics_fill_circle(ctx, GPoint(center_x - 10, center_y), 12);
  graphics_context_set_fill_color(ctx, GColorRed);
  graphics_fill_circle(ctx, GPoint(center_x + 10, center_y), 12);

  graphics_context_set_stroke_color(ctx, GColorWhite);
  graphics_context_set_stroke_width(ctx, 2);
  // Checkmark in green circle
  graphics_draw_line(
      ctx,
      GPoint(center_x - 14, center_y),
      GPoint(center_x - 11, center_y + 4));
  graphics_draw_line(
      ctx,
      GPoint(center_x - 11, center_y + 4),
      GPoint(center_x - 6, center_y - 3));

  // Cross in red circle
  graphics_draw_line(
      ctx,
      GPoint(center_x + 7, center_y - 3),
      GPoint(center_x + 13, center_y + 3));
  graphics_draw_line(
      ctx,
      GPoint(center_x + 7, center_y + 3),
      GPoint(center_x + 13, center_y - 3));

  // Title
  graphics_context_set_text_color(ctx, GColorWhite);
  graphics_draw_text(
      ctx,
      "AGENT APPROVALS",
      fonts_get_system_font(FONT_KEY_GOTHIC_18_BOLD),
      GRect(0, center_y + 34, bounds.size.w, 22),
      GTextOverflowModeWordWrap,
      GTextAlignmentCenter,
      NULL);

  // Subtitle
  graphics_context_set_text_color(ctx, GColorLightGray);
  graphics_draw_text(
      ctx,
      "Antigravity & Jetski",
      fonts_get_system_font(FONT_KEY_GOTHIC_14),
      GRect(0, center_y + 56, bounds.size.w, 18),
      GTextOverflowModeWordWrap,
      GTextAlignmentCenter,
      NULL);

  // Author / GitHub footer
  graphics_context_set_text_color(ctx, GColorCeleste);
  graphics_draw_text(
      ctx,
      "github.com/savelee",
      fonts_get_system_font(FONT_KEY_GOTHIC_14_BOLD),
      GRect(0, bounds.size.h - 22, bounds.size.w, 18),
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

  // Timer for automatic transition after 1500ms
  s_splash_timer = app_timer_register(1500, transition_to_main, NULL);
}

static void splash_window_unload(Window *window) {
  if (s_splash_timer) {
    app_timer_cancel(s_splash_timer);
    s_splash_timer = NULL;
  }
  layer_destroy(s_splash_canvas);
}

void splash_init(void) {
  s_has_transitioned = false;
  s_splash_window = window_create();
  window_set_click_config_provider(s_splash_window, splash_click_config_provider);
  window_set_window_handlers(
      s_splash_window,
      (WindowHandlers){
          .load = splash_window_load,
          .unload = splash_window_unload,
      });
  window_stack_push(s_splash_window, true);
}

void splash_deinit(void) {
  if (s_splash_window) {
    window_destroy(s_splash_window);
  }
}
