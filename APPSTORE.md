# Rebble / Pebble App Store Submission Details

Use the following metadata and image assets when submitting **Agent Approvals** to the [Rebble Appstore](https://apps.rebble.io/) / [Pebble Developer Portal](https://dev-portal.rebble.io/):

---

## 🏷️ Basic Metadata

* **App Title**: `Agent Approvals (Antigravity)`
* **Developer Name**: `Lee Boonstra (@savelee)`
* **Category**: `Tools & Utilities` / `Daily`
* **Version**: `1.1.0`
* **Compatibility**: Pebble Time 2, Pebble Time, Pebble Time Steel, Pebble Time Round, Pebble 2 (`emery`, `basalt`, `chalk`, `diorite`)
* **Source Code & Listener Download**: [https://github.com/savelee/pebble_coding_agent_approval](https://github.com/savelee/pebble_coding_agent_approval)

---

## 🖼️ Store Image Assets (Generated in `/store_assets`)

Upload the corresponding image files to the Rebble Developer Portal:

| Platform / Slot | File Path | Exact Dimensions | Description |
| :--- | :--- | :---: | :--- |
| **Store Header Banner** | `store_assets/banner_720x320.png` | **720 × 320 px** | Antigravity full-color logo, watch mockup & developer branding |
| **Large App Icon** | `store_assets/icon_144x144.png` | **144 × 144 px** | Antigravity full-color icon with green approve checkmark badge |
| **Small App Icon** | `store_assets/icon_48x48.png` | **48 × 48 px** | Antigravity full-color icon with green approve checkmark badge |
| **Emery Screenshot 1 (PT2)** | `store_assets/screenshot_emery_200x228.png` | **200 × 228 px** | Real split-screen layout (`READY`, Confirm [UP], Disapprove [DOWN]) |
| **Emery Screenshot 2 (PT2)** | `store_assets/screenshot_emery_splash_200x228.png` | **200 × 228 px** | Splash & explanation screen with Antigravity logo |
| **Emery Screenshot 3 (PT2)** | `store_assets/screenshot_emery_sent_200x228.png` | **200 × 228 px** | Confirmed state (`SENT OK`) |

---

## 📝 Short Description (Max 100 characters)

> Approve your coding agent (like Antigravity) from your wrist, with the Pebble Time 2 app!

---

## 📖 Long Description / Store Listing

```markdown
Approve your coding agent (like Antigravity) from your wrist, with the Pebble Time 2 app (and web extension).

Designed for developers working with agentic coding environments—including Google Antigravity, Cursor, and Claude Code—Agent Approvals pairs your Pebble smartwatch with a lightweight local Python listener service running on your computer.

Whenever your AI assistant prompts you for approval (to execute a terminal command, modify files, or accept an architectural plan), simply press the physical button on your watch without switching focus away from your editor:

🟢 UP BUTTON: Confirms the action (injects "i confirm\n") with haptic pulse.
🔴 DOWN BUTTON: Disapproves the action (injects "i disapprove\n") with haptic pulse.
🔵 SELECT BUTTON: Opens the info / layout preview screen.

Features:
• Instant two-color split UI (Kelly Green Confirm / Crimson Red Disapprove)
• Real-time delivery status header (READY, CONFIRMING, SENT OK, NET ERROR)
• Branded splash screen on launch with Antigravity logo
• Haptic vibration feedback for both click dispatch and network acknowledgment
• In-app configuration page to set your Mac / PC local IP and port
• Zero cloud dependencies—communicates strictly across your local Wi-Fi network

🚀 COMPANION DESKTOP EXTENSION REQUIRED:
Download the open-source Python listener and setup instructions from GitHub:
https://github.com/savelee/pebble_coding_agent_approval
```

---

## ⚙️ Configuration Help Text (In-App Settings)

> **Listener Host / IP**: The local network IP address of your Mac or PC running the Python listener (e.g. `192.168.1.100` or `127.0.0.1` for emulator).  
> **Port**: The listener port (defaults to `5000`).
