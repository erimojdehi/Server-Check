import os
import platform
import json
import datetime
import subprocess
import threading
import time

# --- Setup ---
script_dir = os.path.dirname(os.path.realpath(__file__)) if '__file__' in globals() else os.getcwd()
os.chdir(script_dir)

LOG_FILE = "ping_log.txt"
SERVERS_FILE = "servers.json"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
CHECK_INTERVAL_SECONDS = 3600  # 1 hour

# --- Load/Save Servers ---
def load_servers():
    if not os.path.exists(SERVERS_FILE):
        with open(SERVERS_FILE, "w") as f:
            json.dump(["v-fleetfocus", "v-fleetfocustest", "v-cnbfuel"], f, indent=4)
    with open(SERVERS_FILE, "r") as f:
        return json.load(f)

def save_servers(server_list):
    with open(SERVERS_FILE, "w") as f:
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

# --- Trim old logs ---
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

# --- Main Ping Loop ---
def run_check():
    servers = load_servers()
    statuses = {server: is_online(server) for server in servers}
    log_status_block(statuses)
    trim_log()
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Ping check complete.")

# --- Start Background Loop ---
def start_hourly_loop():
    def loop():
        while True:
            run_check()
            time.sleep(CHECK_INTERVAL_SECONDS)

    t = threading.Thread(target=loop, daemon=True)
    t.start()

# --- For CLI/Debug Use Only ---
if __name__ == "__main__":
    print("Running initial ping and starting hourly loop...")
    run_check()
    start_hourly_loop()
    while True:
        time.sleep(1)
