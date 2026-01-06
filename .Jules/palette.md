## 2024-10-27 - Mining Feedback in CLI
**Learning:** Users of CLI applications (even simple simulations) feel more rewarded when "long-running" or significant actions (like mining) provide detailed summary statistics rather than a generic success message.
**Action:** When implementing CLI commands that process data, always summarize the *result* of the processing (e.g., "3 items processed", "Reward: 10 ZAR") instead of just saying "Done". Use emojis as visual anchors for success/status.
