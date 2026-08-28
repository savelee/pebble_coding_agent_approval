# Rebble / Pebble App Store Submission Details

Use the following metadata and descriptions when submitting **Agent Approvals** to the [Rebble Appstore](https://apps.rebble.io/) / [Pebble Developer Portal](https://dev-portal.rebble.io/):

---

## 🏷️ Basic Metadata

* **App Title**: `Agent Approvals`
* **Developer Name**: `Lee Boonstra (@savelee)`
* **Category**: `Tools & Utilities` / `Daily`
* **Version**: `1.1.0`
* **Compatibility**: Pebble Time, Pebble Time Steel, Pebble Time 2, Pebble Time Round, Pebble 2 (`basalt`, `emery`, `chalk`, `diorite`)
* **Source Code & Listener Download**: [https://github.com/savelee/pebble_coding_agent_approval](https://github.com/savelee/pebble_coding_agent_approval)

---

## 🖼️ Store Image Assets (Generated in `/store_assets`)

Upload the corresponding image files from the **`store_assets/`** directory:

| Asset Type | File Path | Dimensions | Usage |
| :--- | :--- | :--- | :--- |
| **Store Header Banner** | `store_assets/banner_720x320.png` | 720 × 320 px | Featured store listing header banner |
| **Large App Icon** | `store_assets/icon_large_144x144.png` | 144 × 144 px | Main App Store icon |
| **Small App Icon** | `store_assets/icon_80x80.png` | 80 × 80 px | Store search results & list view icon |
| **Screenshot 1 (PT2)** | `store_assets/screenshot_1_action_emery.png` | 200 × 228 px | Pebble Time 2 Main Split-Screen (`READY`) |
| **Screenshot 2 (PT2)** | `store_assets/screenshot_2_splash_emery.png` | 200 × 228 px | Pebble Time 2 Splash & Info Screen |
| **Screenshot 3 (PT2)** | `store_assets/screenshot_3_sent_emery.png` | 200 × 228 px | Pebble Time 2 Confirmation (`SENT OK`) |
| **Screenshot 4 (PT)** | `store_assets/screenshot_4_action_basalt.png` | 144 × 168 px | Pebble Time Main Split-Screen |
| **Screenshot 5 (PT)** | `store_assets/screenshot_5_splash_basalt.png` | 144 × 168 px | Pebble Time Splash Screen |

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
• Branded splash screen on launch with layout preview
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
