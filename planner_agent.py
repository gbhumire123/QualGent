import os
import json
import openai
import re

class PlannerAgent:
    def __init__(self, model: str = None):
        # Explicit API key (recommended to set this in environment variable for safety)
        self.api_key = os.getenv("OPENAI_API_KEY", "<your fallback key>")
        self.model = model or "gpt-3.5-turbo"
        self.client = openai.OpenAI(api_key=self.api_key)

    def plan(self, goal: str):
        """Generate a list of high-level steps for a natural-language goal."""
        # Normalize goal text (remove hyphens) and lowercase
        norm_goal = goal.lower().replace('-', '')

        
        messages = [
            {
                "role": "system",
                "content": "You are an automation planner that turns user instructions into an ordered list of concise, actionable steps."
            },
            {
                "role": "user",
                "content": (
                    f"Given the instruction: '{goal}', assume the phone is already unlocked and on the home screen. "
                    "Output only a clean JSON array of 2–4 word high-level action steps, like 'Open Settings', 'Navigate to Wi-Fi', 'Toggle Wi-Fi'. "
                    "Ensure that intermediate steps like opening submenus are included if required to reach the final toggle. "
                    "Do not include explanations, markdown, or extra text — only the pure JSON array."
                )
            }
        ]

        # Make the API call using chat.completions.create
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        # Extract the message content
        content = response.choices[0].message.content.strip()

        # Remove markdown if present
        content = re.sub(r"^```(?:json)?\n?", "", content)
        content = re.sub(r"\n?```$", "", content)

        # Try to parse as JSON array
        try:
            steps = json.loads(content)
        except json.JSONDecodeError:
            # Fallback to plain line split
            steps = [line.strip("- ").strip() for line in content.splitlines() if line.strip()]

        return steps


# Usage
if __name__ == "__main__":
    planner = PlannerAgent()
    steps = planner.plan("Toggle the Wifi on my phone")
    print(steps)
