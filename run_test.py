from planner_agent import PlannerAgent
import os
import subprocess
import datetime
import time
import json
import re

# Logging setup
script_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(script_dir, "execution_logs")
os.makedirs(log_dir, exist_ok=True)
_script_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_dir, f"log_{_script_timestamp}.txt")

def log_and_capture(message):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(log_file, "a") as lf:
        lf.write(f"{timestamp}: {message}\n")
    screenshot_path = os.path.join(log_dir, f"screenshot_{timestamp}.png")
    try:
        proc = subprocess.run(["adb", "exec-out", "screencap", "-p"], capture_output=True, check=True)
        with open(screenshot_path, "wb") as imgf:
            imgf.write(proc.stdout)
    except Exception as e:
        with open(log_file, "a") as lf:
            lf.write(f"{timestamp}: Screenshot failed: {e}\n")

def get_serial():
    output = subprocess.check_output(["adb", "devices"]).decode()
    print("ADB devices listing:\n", output)
    lines = output.strip().splitlines()[1:]
    for line in lines:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            serial = parts[0]
            print(f"Using device: {serial}")
            return serial
    return None

def check_wifi_enabled(serial):
    try:
        info = subprocess.check_output(["adb", "-s", serial, "shell", "dumpsys", "wifi"]).decode().lower()
        return "wi-fi is enabled" in info or "wifi is enabled" in info
    except Exception:
        return False

def find_wifi_toggle_bounds(serial):
    try:
        proc = subprocess.run(["adb", "-s", serial, "exec-out", "uiautomator dump /dev/tty"], stdout=subprocess.PIPE, check=True)
        xml = proc.stdout.decode('utf-8')
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_path = os.path.join(log_dir, f"ui_dump_{timestamp}.xml")
        with open(dump_path, "w") as dump_file:
            dump_file.write(xml)
        print(f"Saved UI dump to {dump_path}")
        log_and_capture(f"Saved UI dump to {dump_path}")
        pattern = r'node [^>]*?bounds="(\[\d+,\d+\]\[\d+,\d+\])"[^>]*?(?:text|content-desc|resource-id)="[^"]*wifi[^"]*"[^>]*?clickable="true"'
        match = re.search(pattern, xml, flags=re.IGNORECASE)
        if not match:
            pattern2 = r'node [^>]*?class="[^"]*Switch[^"]*"[^>]*?bounds="(\[\d+,\d+\]\[\d+,\d+\])"'
            match = re.search(pattern2, xml)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

def tap_bounds(serial, bounds):
    m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
    if m:
        x1, y1, x2, y2 = map(int, m.groups())
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        subprocess.run(["adb", "-s", serial, "shell", "input", "tap", str(cx), str(cy)], check=True)
        return True
    return False

def find_node_bounds(serial, keyword):
    try:
        proc = subprocess.run(["adb", "-s", serial, "exec-out", "uiautomator dump /dev/tty"], stdout=subprocess.PIPE, check=True)
        xml = proc.stdout.decode('utf-8')
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_path = os.path.join(log_dir, f"ui_dump_{keyword}_{timestamp}.xml")
        with open(dump_path, "w") as f:
            f.write(xml)
        log_and_capture(f"Saved UI dump for '{keyword}' to {dump_path}")
        pattern = fr'node [^>]*?(text|content-desc)="[^"]*{keyword}[^"]*"[^>]*?clickable="true"[^>]*?bounds="(\[.*?\])"'
        match = re.search(pattern, xml, flags=re.IGNORECASE)
        if match:
            return match.group(2)
    except Exception:
        pass
    return None

def run_test(goal):
    goal_lower = goal.lower()
    serial = get_serial()
    if not serial:
        print("No device found. Ensure a device is connected via adb.")
        log_and_capture("No device found. Test aborted.")
        return

    os.environ["ANDROID_SERIAL"] = serial
    before = check_wifi_enabled(serial)
    print(f"Wi-Fi enabled before test: {before}")
    log_and_capture(f"Wi-Fi enabled before test: {before}")

    planner = PlannerAgent()
    plan = planner.plan(goal)
    print(f"Plan returned: {plan}")
    log_and_capture(f"Plan returned: {plan}")

    for subgoal in plan:
        subgoal_lower = subgoal.lower()
        norm = subgoal_lower.replace('-', '').replace(' ', '')
        print(f"Executing: {subgoal}")
        log_and_capture(f"Executing: {subgoal}")

        if "opensettings" in norm or "open settings" in norm:
            subprocess.check_call(["adb", "-s", serial, "shell", "am", "start", "-a", "android.settings.SETTINGS"])
            time.sleep(2)

        elif "navigate to wifi" in norm or "navigatetowifi" in norm or "go to wifi" in norm:
            bounds1 = find_node_bounds(serial, "Network & Internet")
            if bounds1 and tap_bounds(serial, bounds1):
                print("Tapped on 'Network & Internet'")
                log_and_capture("Tapped on 'Network & Internet'")
                time.sleep(2)
            else:
                log_and_capture("Failed to find 'Network & Internet' in UI")

            bounds2 = find_node_bounds(serial, "Wi‑Fi") or find_node_bounds(serial, "Wi-Fi")
            if bounds2 and tap_bounds(serial, bounds2):
                print("Tapped on 'Wi-Fi'")
                log_and_capture("Tapped on 'Wi-Fi'")
                time.sleep(2)
            else:
                log_and_capture("Failed to find 'Wi-Fi' in UI")

        elif "wifi" in norm and ("toggle" in norm or "turn" in norm):
            current = check_wifi_enabled(serial)
            desired_on = "on" in goal_lower
            if current == desired_on:
                print("Already in desired state; skipping toggle.")
                log_and_capture("Already in desired state; skipping toggle.")
            else:
                if serial.startswith("emulator-"):
                    action = "enable" if desired_on else "disable"
                    subprocess.check_call(["adb", "-s", serial, "shell", "svc", "wifi", action])
                    print(f"Svc wifi {action} used on emulator.")
                    log_and_capture(f"Svc wifi {action} used on emulator.")
                else:
                    bounds = find_wifi_toggle_bounds(serial)
                    if bounds and tap_bounds(serial, bounds):
                        print(f"Tapped Wi-Fi toggle at bounds {bounds}")
                        log_and_capture(f"Tapped Wi-Fi toggle at bounds {bounds}")
                    else:
                        print("Could not find Wi-Fi toggle in UI dump.")
                        log_and_capture("Failed to locate Wi-Fi toggle via UI dump")
                time.sleep(2)

        else:
            print(f"[run_test] Unrecognized step '{subgoal}', skipping.")
            log_and_capture(f"Skipped unrecognized step: {subgoal}")

        state = check_wifi_enabled(serial)
        print(f"Wi-Fi state now: {state}")
        log_and_capture(f"Wi-Fi state now: {state}")

    after = check_wifi_enabled(serial)
    print(f"Wi-Fi enabled after test: {after}")
    log_and_capture(f"Wi-Fi enabled after test: {after}")

if __name__ == "__main__":
    import sys
    goal = sys.argv[1] if len(sys.argv) > 1 else "Turn Wi-Fi off and on"
    print(f"Running with goal: {goal}")
    run_test(goal)
