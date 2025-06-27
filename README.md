# 🛡️ Server Availability Monitor

A secure, standalone desktop monitoring tool built for corporate IT, sysadmins, and fleet managers.  
Continuously checks multiple internal or external servers, logs their status, and alerts your team when something goes down — all from a beautifully designed tray-based interface.

---

## 🚀 Features

✅ **Real-time server monitoring** (unlimited servers)  
✅ **Smart email alerts** (only when server status changes)  
✅ **Runs silently in system tray**  
✅ **Start with Windows** (optional)  
✅ **Start minimized** (optional)  
✅ **Secure sender email handling** (password never stored)  
✅ **Log reports with 30-day auto-trimming**  
✅ **Dark/Light mode toggle**  
✅ **Network-aware** (automatically detects if you're offline and skips checks)  
✅ **Dashboard counts and scrollable log viewer**  
✅ **Fully portable `.exe` — no install or Python required**

---

## 🧱 Designed for Corporates & Teams

🔒 **Built with Security First**  
- Email passwords are never saved or exposed  
- Log files are local only, never transmitted  
- Safe for internal/corporate networks behind firewalls  

🧠 **Built for IT Scalability**  
- Supports any number of server endpoints  
- Perfect for monitoring internal apps, telematics systems, intranet servers, or cloud endpoints  
- No third-party services required

📂 **Built for Audit Readiness**  
- Logs are timestamped and auto-trimmed after 30 days  
- View logs from the GUI or open directly from file  
- Server configuration is customizable via GUI

---

## 📦 How It Works

1. **Run the `.exe`** – no installation needed  
2. **Add servers** via the GUI  
3. **Set alert email(s)** and optional sender credentials  
4. **Apply changes** and let it run in the background  
5. Close the window — it minimizes to the system tray  
6. Right-click tray icon to Show or Exit

---

## 📨 Email Alerts

- Works with Gmail, Outlook, Hotmail, or internal SMTPs  
- Add one or more recipients  
- Only sends an alert if a server goes **offline** (not every cycle)  
- Internet-aware: no false alerts if your laptop is offline

---

## 🌐 Network Smart

- If you disconnect from Wi-Fi or LAN, the app automatically detects it  
- Logs "No internet connection" and **skips that check**  
- Never alerts on false negatives due to local connectivity issues

---

## 📋 Requirements

- Windows 10 or 11  
- No Python installation needed  
- Built-in SMTP support  
- Optional `.ico` for branding (already included in `.exe`)

---

## 🧰 Tech Stack

- **Python** (compiled with PyInstaller)  
- **Tkinter** GUI  
- **pystray + Pillow** for tray icon  
- **winshell** for startup integration  
- **subprocess**, `ping` for connectivity checks  
- No internet access required to run (except for alerts)

---

## 📥 Download

> 🚀 [Click here to download the latest `.exe`](https://drive.google.com/file/d/1OZgoMp9dQMpJzRCPuSuXMdmRJbf4G8hg/view?usp=drive_link)

---

## 🔒 License

MIT License — free to use, share, and customize.

---

## 🤝 Contribute

Have an idea or bug report? [Open an issue](https://github.com/erimojdehi/Server-Check/issues) or submit a PR.

---

## 🧑‍💼 Perfect For

- IT departments
- Fleet and infrastructure teams
- Internal server monitoring
- Secure environments where SaaS tools aren't allowed

---

