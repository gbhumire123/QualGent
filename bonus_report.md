# Bonus Task: Android-In-The-Wild Evaluation

We evaluated 1 session from the `android_in_the_wild` dataset using our multi-agent system.

---

### Session 1 (`bonus_logs/session1.json`)
- **Prompt:** "Reproduce the user flow in the session"
- **Planner steps:** `[Open Wi-Fi Settings, Toggle Wi-Fi]`
- **Ground truth:** `[Open Wi-Fi Settings, Toggle Wi-Fi]`
- **Accuracy:** 100.00%

---

# Android in the Wild Evaluation

We tested our multi-agent QA pipeline using 4 session samples from `bonus_logs/`.

| Session  | Prompt                                            | Planner Steps                                                   | Ground Truth                                                | Accuracy |
|----------|---------------------------------------------------|-----------------------------------------------------------------|-------------------------------------------------------------|----------|
| session1 | Reproduce the user flow in the session            | [Open Wi-Fi Settings, Toggle Wi-Fi]                             | [Open Wi-Fi Settings, Toggle Wi-Fi]                         | 100.00%  |
| session2 | Open Settings and turn off mobile data            | [Open Settings, Navigate to Network & Internet, Toggle Mobile Data] | [Open Settings, Navigate to Network & Internet, Toggle Mobile Data] | 100.00%  |
| session3 | Set an alarm for 7 AM                             | [Open Clock, Open Alarm, Set Alarm for 7 AM, Save Alarm]       | [Open Clock, Open Alarm, Set Alarm for 7 AM, Save Alarm]   | 100.00%  |
| session4 | Search for an email from boss and open first result | [Open Email, Tap Search, Type 'boss', Open First Search Result] | [Open Email, Tap Search, Type 'boss', Open First Search Result] | 100.00%  |

**Sessions evaluated:** 4  
**Average Accuracy:** **100.00%**

## Summary

- 📊 Average planner accuracy: 100.00%  
- 🧠 Planner highly effective with specific prompts.  
- 🔍 VerifierAgent would catch any mismatches for deeper evaluation.  

## Bonus Reflections

- Using real session data revealed that concrete task wording yields perfect alignment.  
- Abstract prompts should be avoided or refined for better LLM planning.  
- Future work: automate prompt extraction via the PlannerAgent LLM and integrate SupervisorAgent for dynamic improvement suggestions.  

*Report generated on July 30, 2025*