# Learning log

What I learned, what broke, how I fixed it. Good interview material. Newest entries first.

## Template

### YYYY-MM-DD: short title
- **Context:**
- **What happened / what broke:**
- **Fix or insight:**
- **Numbers:**

## 2026-10-17: setting up the agent workflow
- **Context:** wrote a hook to protect `.env` from agent edits.
- **What broke:** the first version scanned the raw command text, so a commit message mentioning the file was blocked.
- **Fix or insight:** parse commands into words and only inspect real arguments and redirect targets; add tests for both the blocked and the allowed cases.
