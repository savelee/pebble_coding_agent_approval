# Rebble / Pebble App Store Submission Details

Use the following metadata and image assets when submitting **Agent Approvals** to the [Rebble Appstore](https://apps.rebble.io/) / [Pebble Developer Portal](https://dev-portal.rebble.io/):

---

## 🏷️ Basic Metadata

* **App Title**: `Agent Approvals (Antigravity)`
* **Developer Name**: `Lee Boonstra (@savelee)`
* **Category**: `Tools & Utilities` / `Daily`
* **Version**: `1.1.0`
* **Compatibility**: Pebble Time 2, Pebble Time, Pebble Time Steel, Pebble Time Round, Pebble 2 (`emery`, `basalt`, `chalk`, `diorite`, `aplite`, `flint`, `gabbro`)
* **Source Code & Listener Download**: [https://github.com/savelee/pebble_coding_agent_approval](https://github.com/savelee/pebble_coding_agent_approval)

---

## 🖼️ Store Image Assets by Platform (in `/store_assets`)

Upload the corresponding image files under each platform tab in the Rebble Developer Portal:

| Platform / Slot | File Path | Exact Dimensions | Display Style |
| :--- | :--- | :---: | :--- |
| **Store Header Banner** | `store_assets/banner_720x320.png` | **720 × 320 px** | Official Antigravity full-color logo banner with app copy |
| **Large App Icon** | `store_assets/icon_144x144.png` | **144 × 144 px** | Antigravity full-color icon with green approve checkmark |
| **Small App Icon** | `store_assets/icon_48x48.png` | **48 × 48 px** | Antigravity full-color icon with green approve checkmark |
| **Emery** *(Pebble Time 2)* | `store_assets/screenshot_emery_200x228.png` | **200 × 228 px** | Color 64-color split screen |
| **Aplite** *(Pebble Classic)* | `store_assets/screenshot_aplite_144x168.png` | **144 × 168 px** | Monochrome 1-bit high-contrast split screen |
| **Basalt** *(Pebble Time)* | `store_assets/screenshot_basalt_144x168.png` | **144 × 168 px** | Color 64-color split screen |
| **Chalk** *(Time Round)* | `store_assets/screenshot_chalk_180x180.png` | **180 × 180 px** | Circular round watch face with transparent corners |
| **Diorite** *(Pebble 2)* | `store_assets/screenshot_diorite_144x168.png` | **144 × 168 px** | Monochrome 1-bit split screen |
| **Flint** *(Color Prototype)* | `store_assets/screenshot_flint_144x168.png` | **144 × 168 px** | Color split screen |
| **Gabbro** *(High-Res)* | `store_assets/screenshot_gabbro_260x260.png` | **260 × 260 px** | High-res color split screen |

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
