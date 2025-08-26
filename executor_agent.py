import subprocess
import json
import time
import os
import datetime

class ExecutorAgent:
    def __init__(self, env):
        self.env = env  

    def _log_and_capture(self, message):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "execution_logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"log_{timestamp}.txt")

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

    def _find_clickable_node(self, ui_tree, keywords):
        """Find the best matching clickable node for the given keywords."""
        for node in ui_tree.get("nodes", []):
            text = node.get("text", "").lower()
            content_desc = node.get("content_description", "").lower()
            bounds = node.get("bounds", None)
            clickable = node.get("clickable", False)

            for keyword in keywords:
                if (keyword in text or keyword in content_desc) and clickable and bounds:
                    return bounds
        return None

    def _click_center_of_bounds(self, bounds):        
        import re
        match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
        if match:
            x1, y1, x2, y2 = map(int, match.groups())
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            subprocess.run(["adb", "shell", "input", "tap", str(center_x), str(center_y)])
            print(f"Tapped at ({center_x}, {center_y})")
            return True
        return False

    def execute(self, subgoal, observation):
        """Execute action for the subgoal using UI interaction."""
        self._log_and_capture(f"Executor received subgoal: {subgoal}")

        ui_tree_str = observation.get("ui_tree", "{}")
        try:
            ui_tree = json.loads(ui_tree_str)
        except Exception as e:
            self._log_and_capture(f"Failed to parse ui_tree: {e}")
            return

        subgoal_lower = subgoal.lower()
        if "toggle" in subgoal_lower and "wifi" in subgoal_lower:
            # Keywords to search in the UI tree
            possible_labels = ["wi-fi", "wifi", "toggle wifi", "network"]
            bounds = self._find_clickable_node(ui_tree, possible_labels)

            if bounds:
                self._click_center_of_bounds(bounds)
                self._log_and_capture(f"Tapped bounds: {bounds}")
            else:
                self._log_and_capture("No matching Wi-Fi toggle found in UI tree.")
