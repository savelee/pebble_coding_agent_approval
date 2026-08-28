# Rebble / Pebble App Store Submission Details

Use the following metadata and descriptions when submitting **Agent Approvals** to the [Rebble Appstore](https://apps.rebble.io/) / [Pebble Developer Portal](https://dev-portal.rebble.io/):

---

## 🏷️ Basic Metadata

* **App Title**: `Agent Approvals`
* **Developer Name**: `Lee Boonstra (@savelee)`
* **Category**: `Tools & Utilities` / `Daily`
* **Version**: `1.0.0`
* **Compatibility**: Pebble Time, Pebble Time Steel, Pebble Time 2, Pebble Time Round, Pebble 2 (`basalt`, `emery`, `chalk`, `diorite`)
* **Source Code & Listener Download**: [https://github.com/savelee/pebble_coding_agent_approval](https://github.com/savelee/pebble_coding_agent_approval)

---

## 📝 Short Description (Max 100 characters)

> One-click physical wrist approvals for Antigravity, Cursor, and Claude AI agents.

---

## 📖 Long Description / Store Listing

```markdown
Approve or disapprove AI coding assistant actions directly from your wrist!

Designed for developers working with agentic coding environments—including Google Antigravity, Cursor, and Claude Code—Agent Approvals pairs your Pebble smartwatch with a lightweight local Python listener service running on your computer.

Whenever your AI assistant prompts you for approval (to execute a command, modify files, or accept a plan), simply press the physical button on your watch without switching focus away from your editor:

🟢 UP BUTTON: Confirms the action (injects "i confirm\n") with haptic pulse.
🔴 DOWN BUTTON: Disapproves the action (injects "i disapprove\n") with haptic pulse.

Features:
• Instant two-color split UI (Kelly Green Confirm / Crimson Red Disapprove)
• Real-time delivery status header (READY, CONFIRMING, SENT OK, NET ERROR)
• Branded splash screen on launch
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

---

## 🖼️ Suggested Screenshots / Store Visuals
1. **Screenshot 1**: Splash screen with "AGENT APPROVALS - Antigravity".
2. **Screenshot 2**: Main split-screen action screen showing green `CONFIRM [UP]` and red `DISAPPROVE [DOWN]`.
3. **Screenshot 3**: Status header showing `CONFIRMING...` $\rightarrow$ `SENT OK`.
