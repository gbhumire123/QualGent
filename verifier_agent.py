# multi_agent_qa/verifier_agent.py

class VerifierAgent:
    def __init__(self):
        pass

    def verify(self, goal, result_ui_tree):
        """
        Verifies if the intended goal is reflected in the resulting UI tree.

        Parameters:
        - goal (str): The current subgoal, e.g., "Toggle Wi-Fi"
        - result_ui_tree (str): The post-action UI tree in raw JSON/text format

        Returns:
        - (bool, str): Tuple indicating success and explanation
        """
        keyword = ""
        if "Wi-Fi" in goal:
            keyword = "Wi-Fi"
        elif "Bluetooth" in goal:
            keyword = "Bluetooth"
        elif "Settings" in goal:
            keyword = "Settings"
        elif "Network" in goal:
            keyword = "Network"

        if keyword and keyword.lower() in result_ui_tree.lower():
            return True, f"'{keyword}' found in UI. Step passed."
        else:
            return False, f"'{keyword}' not found in UI. Step failed."
