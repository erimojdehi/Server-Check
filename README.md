# 🖥️ Server Availability Monitor

This lightweight Windows application monitors a list of servers in real-time and notifies you when any of them go offline. It's fully GUI-based, customizable, portable, and includes smart email alerts and detailed logging — no Python installation required.

---

## 🚀 Features

### ✅ Real-Time Server Monitoring
- Pings each server on a schedule (you choose the interval: 5–120 minutes)
- Detects `ONLINE` or `OFFLINE` status
- Runs silently in the background

### ✅ Graphical User Interface
- Add or remove servers with a few clicks
- Adjust monitoring frequency from a dropdown
- Pause or resume background monitoring at any time
- Live countdown shows time until next ping
- Manually trigger a check with the "Check Now" button
- "Apply Changes" saves new settings and pings instantly
- "Records" opens the log file for easy viewing

### ✅ Smart Email Alerts
- Sends alert emails **only when a server goes from ONLINE → OFFLINE**
- Avoids spamming you with repeat alerts
- Enter one or more **recipient emails**
- Enter a **sender email** and **password** (used to send the alert)
- Works with **Outlook**, **Gmail**, **Hotmail**, and most custom SMTP accounts

### ✅ Logging & History
- Maintains a detailed `ping_log.txt` in the same folder as the app
- Automatically tracks:
  - Ping results
  - Server list changes
  - Timestamps for every event
- Keeps up to 30 days of records

### ✅ Portable `.exe` — No Installation Needed
- Runs on any Windows system (Windows 10 or 11)
- Does **not require Python or installation**
- Just double-click to launch

### ✅ Minimal System Footprint
- Runs silently in the background
- No flashing CMD windows or terminal pop-ups
- No files stored outside the app folder

---

## 📂 Files Created

These files are created automatically in the **same folder as the `.exe`**:

| File            | Purpose                          |
|-----------------|----------------------------------|
| `ping_log.txt`  | Log of server status checks      |
| `servers.json`  | Stores your saved server list    |

These are updated and reused each time you run the app.

---
