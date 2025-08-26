# multi_agent_qa/supervisor_agent.py

class SupervisorAgent:
    def __init__(self):
        pass

    def evaluate(self, logs, screenshots):
        """
        Evaluates the outcome of an execution trace.

        Parameters:
        - logs (List[str]): Logs from the VerifierAgent or execution trace
        - screenshots (List[str]): Paths to captured screenshots

        Returns:
        - str: Summary of the evaluation
        """
        print("\n📋 Supervisor Evaluation Report:")
        passed = 0

        for idx, log in enumerate(logs):
            status = "✅" if "passed" in log.lower() else "❌"
            print(f"Step {idx + 1}: {status} — {log.strip()}")
            if "passed" in log.lower():
                passed += 1

        total = len(logs)
        print("\n🖼️ Screenshots captured:")
        for shot in screenshots:
            print(f" - {shot}")

        summary = f"\n📊 Summary: {passed}/{total} steps passed.\n"
        return summary
