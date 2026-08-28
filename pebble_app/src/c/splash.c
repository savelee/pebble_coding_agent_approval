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
static GBitmap *s_logo_bitmap = NULL;
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
      "ANTIGRAVITY",
      fonts_get_system_font(FONT_KEY_GOTHIC_18_BOLD),
      GRect(0, 4, bounds.size.w, 20),
      GTextOverflowModeWordWrap,
      GTextAlignmentCenter,
      NULL);

  // 3. Official Antigravity Logo Bitmap
  int logo_size = 60;
  int logo_x = (bounds.size.w - logo_size) / 2;
  int logo_y = 26;

  if (s_logo_bitmap) {
    graphics_context_set_compositing_mode(ctx, GCompOpSet);
    graphics_draw_bitmap_in_rect(ctx, s_logo_bitmap, GRect(logo_x, logo_y, logo_size, logo_size));
  } else {
    // Fallback circle if bitmap not yet loaded
    graphics_context_set_fill_color(ctx, GColorKellyGreen);
    graphics_fill_circle(ctx, GPoint(bounds.size.w / 2, logo_y + logo_size / 2), 24);
  }

  // 4. Detailed Explanation Text
  graphics_context_set_text_color(ctx, GColorWhite);
  graphics_draw_text(
      ctx,
      "Approve your coding agent (like Antigravity) from your wrist, with the Pebble Time 2 app (and web extension).",
      fonts_get_system_font(FONT_KEY_GOTHIC_14),
      GRect(6, logo_y + logo_size + 4, bounds.size.w - 12, 54),
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

#if defined(RESOURCE_ID_IMAGE_ANTIGRAVITY_LOGO)
  s_logo_bitmap = gbitmap_create_with_resource(RESOURCE_ID_IMAGE_ANTIGRAVITY_LOGO);
#endif

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
  if (s_logo_bitmap) {
    gbitmap_destroy(s_logo_bitmap);
    s_logo_bitmap = NULL;
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
