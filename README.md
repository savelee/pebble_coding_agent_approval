# Pebble Coding Agent Approval (Antigravity & Jetski)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Pebble SDK](https://img.shields.io/badge/Pebble-SDK_4.3-orange.svg)](https://rebble.io)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)

A Pebble Smartwatch application (Pebble Time, Pebble Time Steel, Pebble Time 2) and companion Python Flask listener service that enables developers to approve or disapprove AI coding assistant prompts (**Google Antigravity**, **Jetski**, **Cursor**, **Claude Code**) directly from their wrist.

Repository: **[https://github.com/savelee/pebble_coding_agent_approval](https://github.com/savelee/pebble_coding_agent_approval)**

---

## ⌚ Smartwatch Interface & Physical Controls

* **Splash Screen**: Branded startup screen displaying `AGENT APPROVALS - Antigravity & Jetski by @savelee`.
* **Top Half (Kelly Green)**: Confirm circle button with checkmark badge.
  * **Up Button**: Sends confirmation action (`"i confirm\n"`) with haptic vibration pulse.
* **Bottom Half (Crimson Red)**: Disapprove circle button with cross ('X') badge.
  * **Down Button**: Sends disapproval action (`"i disapprove\n"`) with haptic vibration pulse.
* **Top Header Bar**: Real-time status indicator (`READY`, `CONFIRMING...`, `DISAPPROVING...`, `SENT OK`, `NET ERROR`, `TIMEOUT`).
* **Settings (Clay / Webview)**: Configure the host IP address and port directly on your watch/phone or emulator browser.

---

## 🏗️ Architecture Overview

```mermaid
flowchart LR
    PebbleWatch[Physical Pebble Watch / Emulator] -- Bluetooth AppMessage --> PhonePKJS[Phone / PebbleKit JS]
    PhonePKJS -- Wi-Fi HTTP POST /api/action --> FlaskListener[Python Flask Listener (Mac)]
    FlaskListener -- AppleScript System Events --> Antigravity[Antigravity / Jetski / Active IDE]
```

1. **Watch App (`pebble_app/src/c/`)**: Handles button clicks, renders the splash screen and split-color interface, and displays delivery status.
2. **PebbleKit JS (`pebble_app/src/pkjs/`)**: Dispatches HTTP POST requests with JSON payloads (`{"action": "confirm"}` or `{"action": "disapprove"}`) to the listener service.
3. **Flask Listener (`listener/`)**: Web server running on `0.0.0.0:5000` that brings the target AI agent (Antigravity / Jetski) into focus and executes synthetic keystrokes.

---

## 🔒 Mandatory macOS Setup: Accessibility Permissions

Synthetic keystroke injection and window activation on macOS require Accessibility permissions:

1. Open **System Settings** on your Mac.
2. Navigate to **Privacy & Security** > **Accessibility**.
3. Enable (toggle **ON**) the following applications:
   * **Antigravity IDE** (or `Antigravity.app`)
   * **Jetski**
   * **Terminal** / **iTerm2** / **Visual Studio Code** (the terminal from which you launch `python -m listener.app` or `pebble`).

---

## 🚀 Setting Up the Python Listener Service

Manage dependencies using **UV**:

```bash
# 1. Clone the repository
git clone https://github.com/savelee/pebble_coding_agent_approval.git
cd pebble_coding_agent_approval

# 2. Create the virtual environment and install dependencies
make venv

# Or manually via UV:
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt -r requirements-dev.txt

# 3. Start the Flask listener service (binds to 0.0.0.0:5000)
source .venv/bin/activate
python -m listener.app
```

*(Alternatively, run `DEVELOPER_DIR=/Library/Developer/CommandLineTools make run-apis`)*

---

## 📱 How to Install and Run on a Physical Pebble Watch

### Step 1: Ensure Same Wi-Fi Network
Make sure your **Mac** and your **Phone (with Pebble app)** are connected to the **same Wi-Fi network**.

### Step 2: Find Your Mac's Local IP Address
In your Mac terminal, run:
```bash
ipconfig getifaddr en0
```
*(Example output: `192.168.1.100`)*

### Step 3: Install onto Your Wrist

#### On Android (Direct File Sideload):
1. Start a local download server on your Mac:
   ```bash
   cd pebble_app/build && python3 -m http.server 8080
   ```
2. On your Android phone, open Chrome and navigate to `http://<YOUR_MAC_IP>:8080/pebble_app.pbw`.
3. Download the file, tap **Open with Pebble**, and tap **Install**!

#### On iPhone (AirDrop):
1. Locate `pebble_app/build/pebble_app.pbw` in Finder.
2. AirDrop the file to your iPhone and select **Open in Pebble**.

---

### Step 4: Configure Listener IP in the Mobile App
1. In the Pebble app on your phone, navigate to the **Locker / Apps** tab.
2. Tap the **Agent Approvals** app and tap **Settings** (gear icon).
3. In the settings page:
   * **Listener Host / IP Address**: Enter your Mac's IP (e.g. `192.168.1.100`).
   * **Port**: `5000`.
4. Tap **Save & Close**.

Now whenever Antigravity or Jetski requests approval, click the **UP** button on your wrist!

---

## 🏬 Rebble App Store Submission

Store metadata and description copy are prepared in **[APPSTORE.md](file:///Users/leeboonstra/Documents/Github/pebble/approve/APPSTORE.md)**.

---

## 🧪 Testing & Verification

```bash
# Direct terminal curl test
curl -X POST http://127.0.0.1:5000/api/action \
  -H "Content-Type: application/json" \
  -d '{"action": "confirm"}'

# Run automated unit tests (99% coverage)
DEVELOPER_DIR=/Library/Developer/CommandLineTools make test

# Check linting and formatting
DEVELOPER_DIR=/Library/Developer/CommandLineTools make lint
DEVELOPER_DIR=/Library/Developer/CommandLineTools make format
```

---

## 📄 License

Copyright 2026 Google LLC. Licensed under the Apache License, Version 2.0.
