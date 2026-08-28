# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Split-screen Pebble Time / Pebble Time 2 watch UI with green Confirm checkmark badge (Up button) and red Disapprove cross badge (Down button).
- PebbleKit JS client with Clay settings configuration for target listener Host IP and Port.
- Python Flask listener application managing `/api/action`, `/healthz`, and `/api/notify` endpoints.
- `KeystrokeService` supporting macOS AppleScript and Linux `xdotool` keystroke dispatch with automatic Return key submission.
- Complete Pytest suite with 99% statement coverage and strict flake8/black formatting.
- `Makefile` with targets for virtual environment management (`venv`), test (`test`), format (`format`), lint (`lint`), and execution (`run-apis`).
