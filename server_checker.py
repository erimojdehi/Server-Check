import tkinter as tk
from tkinter import messagebox
import subprocess
import platform
import json
import datetime
import os
import threading
import time

# --- Setup ---
script_dir = os.path.dirname(os.path.realpath(__file__)) if '__file__' in globals() else os.getcwd()
os.chdir(script_dir)

LOG_FILE = "ping_log.txt"
SERVERS_FILE = "servers.json"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_INTERVAL_SECONDS = 3600

# --- Load/Save Servers ---
def load_servers():
    if not os.path.exists(SERVERS_FILE):
        with open(SERVERS_FILE, "w", encoding="utf-8") as f:
            json.dump(["v-fleetfocus", "v-fleetfocustest", "v-cnbfuel"], f, indent=4)
    with open(SERVERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_servers(server_list):
    with open(SERVERS_FILE, "w", encoding="utf-8") as f:
        json.dump(server_list, f, indent=4)

# --- Ping ---
def is_online(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    result = subprocess.run(["ping", param, "1", host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

# --- Logging ---
def log_line(line=""):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def log_separator():
    log_line("=" * 60)

def log_status_block(server_statuses):
    timestamp = datetime.datetime.now().strftime(DATE_FORMAT)
    log_line("")
    log_line(f"🔁 PING CHECK @ {timestamp}")
    for server, status in server_statuses.items():
        log_line(f"{server:<25} | {'✅ ONLINE' if status else '❌ OFFLINE'}")
    log_separator()

def log_server_change(change_type, affected_server, updated_list):
    timestamp = datetime.datetime.now().strftime(DATE_FORMAT)
    log_line("")
    log_line(f"⚙️ SERVER LIST UPDATED @ {timestamp}")
    action = "+ Added" if change_type == "add" else "- Removed"
    log_line(f"{action}: {affected_server}")
    log_line("Updated server list:")
    for s in updated_list:
        log_line(f"- {s}")
    log_separator()

def trim_log():
    if not os.path.exists(LOG_FILE):
        return
    cutoff = datetime.datetime.now() - datetime.timedelta(days=30)
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        keep = False
        for line in lines:
            if line.startswith("🔁 PING CHECK @"):
                timestamp_str = line.split("@")[1].strip()
                try:
                    timestamp = datetime.datetime.strptime(timestamp_str, DATE_FORMAT)
                    keep = timestamp >= cutoff
                except:
                    keep = False
            if keep or line.startswith("⚙️ SERVER LIST UPDATED @") or line.startswith("="):
                f.write(line)

# --- GUI App ---
class ServerMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server Availability Monitor")
        self.servers = load_servers()
        self.buffered_servers = self.servers.copy()
        self.status_labels = {}
        self.monitoring_active = True
        self.check_interval = DEFAULT_INTERVAL_SECONDS
        self.time_remaining = self.check_interval
        self.countdown_label = None

        self.build_gui()
        self.start_hourly_loop()

    def build_gui(self):
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack()

        tk.Label(self.frame, text="Servers:", font=("Segoe UI", 12, "bold")).pack()

        self.server_list_frame = tk.Frame(self.frame)
        self.server_list_frame.pack()

        self.render_server_list()

        self.add_frame = tk.Frame(self.frame)
        self.add_frame.pack(pady=5)

        self.new_server_var = tk.StringVar()
        self.add_entry = tk.Entry(self.add_frame, textvariable=self.new_server_var)
        self.add_entry.pack(side=tk.LEFT)
        tk.Button(self.add_frame, text="Add", command=self.add_server).pack(side=tk.LEFT, padx=5)

        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(pady=10)

        tk.Button(self.button_frame, text="Apply Changes", command=self.apply_changes).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Check Now", command=self.check_now).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Records", command=self.open_log_file).pack(side=tk.LEFT, padx=5)
        self.pause_button = tk.Button(self.button_frame, text="Pause Monitor", command=self.toggle_monitoring)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.results_frame = tk.Frame(self.frame)
        self.results_frame.pack(pady=10)
        interval_frame = tk.Frame(self.frame)
        interval_frame.pack(pady=(5, 0))

        tk.Label(interval_frame, text="Ping interval (minutes):").pack(side=tk.LEFT)
        self.interval_var = tk.StringVar(value="60")
        interval_dropdown = tk.OptionMenu(interval_frame, self.interval_var, "5", "10", "15", "30", "60", "120", command=self.update_interval)
        interval_dropdown.pack(side=tk.LEFT)

        self.countdown_label = tk.Label(self.frame, text="Next ping in: 60m 0s", font=("Segoe UI", 10))
        self.countdown_label.pack(pady=(5, 0))
        self.update_countdown()

    def render_server_list(self):
        for widget in self.server_list_frame.winfo_children():
            widget.destroy()

        for server in self.buffered_servers:
            row = tk.Frame(self.server_list_frame)
            row.pack(fill=tk.X, pady=1)

            tk.Label(row, text=server, width=30, anchor="w").pack(side=tk.LEFT)
            tk.Button(row, text="Delete", command=lambda s=server: self.delete_server(s)).pack(side=tk.RIGHT)

    def render_results(self, results):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        for server, status in results.items():
            color = "green" if status else "red"
            text = f"{server} is {'ONLINE ✅' if status else 'OFFLINE ❌'}"
            label = tk.Label(self.results_frame, text=text, fg=color, font=("Segoe UI", 10, "bold"))
            label.pack()

    def add_server(self):
        new_server = self.new_server_var.get().strip()
        if new_server and new_server not in self.buffered_servers:
            self.buffered_servers.append(new_server)
            self.new_server_var.set("")
            self.render_server_list()

    def delete_server(self, server):
        if server in self.buffered_servers:
            self.buffered_servers.remove(server)
            self.render_server_list()

    def apply_changes(self):
        original = set(self.servers)
        updated = set(self.buffered_servers)

        added = updated - original
        removed = original - updated

        for s in added:
            log_server_change("add", s, list(updated))
        for s in removed:
            log_server_change("remove", s, list(updated))

        self.servers = list(updated)
        save_servers(self.servers)
        self.run_ping(self.servers)

    def check_now(self):
        self.run_ping(self.servers)

    def run_ping(self, server_list):
        def ping_and_update():
            results = {}
            for s in server_list:
                results[s] = is_online(s)
            log_status_block(results)
            trim_log()
            self.render_results(results)

        threading.Thread(target=ping_and_update).start()

    def toggle_monitoring(self):
        self.monitoring_active = not self.monitoring_active
        self.pause_button.config(text="Resume Monitor" if not self.monitoring_active else "Pause Monitor")

    def update_countdown(self):
        if self.monitoring_active:
            minutes, seconds = divmod(self.time_remaining, 60)
            self.countdown_label.config(text=f"Next ping in: {minutes}m {seconds}s")
            self.time_remaining -= 1
        else:
            self.countdown_label.config(text="Monitoring paused.")

        self.root.after(1000, self.update_countdown)

    def update_interval(self, selected):
        try:
            minutes = int(selected)
            self.check_interval = minutes * 60
            self.time_remaining = self.check_interval
            self.countdown_label.config(text=f"Next ping in: {minutes}m 0s")
        except ValueError:
            messagebox.showerror("Invalid Input", "Interval must be a number.")

    def open_log_file(self):
        os.startfile(LOG_FILE)

    def start_hourly_loop(self):
        def loop():
            while True:
                if self.monitoring_active:
                    self.run_ping(self.servers)

                for _ in range(self.check_interval):
                    if not self.monitoring_active:
                        break
                    time.sleep(1)
                    self.time_remaining = self.check_interval - (_ + 1)

        t = threading.Thread(target=loop, daemon=True)
        t.start()

# --- Launch ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ServerMonitorApp(root)
    root.mainloop()
