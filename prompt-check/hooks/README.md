# Optional hook: run the check on every prompt

A skill is chosen by the model from its description, so it can occasionally be skipped. If you want the check
to be applied to every substantive prompt, add a `UserPromptSubmit` hook. The hook does not ask anything
itself; it adds a short reminder to Claude's context, and only for prompts that deserve it (not for short
replies, slash commands, "no questions" requests, or automated turns).

Cost: a few lines of context on each substantive prompt, and a few milliseconds of local script time.

## Install

1. Install the skill (see the repository README) so that this file exists:
   `~/.claude/skills/prompt-check/hooks/prompt-check-hook.py`
2. Add this to `~/.claude/settings.json`, merging it into any `hooks` you already have:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/prompt-check/hooks/prompt-check-hook.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

3. Start a new session. To confirm it fires, run Claude Code with hook debugging, or send a substantive
   prompt and check that Claude applies the check.

## Turn off

Delete the entry from `settings.json`. The skill keeps working on its own, just less predictably.
To skip the check for one prompt, write "no questions" or "без вопросов" in it. (A leading `!` is not usable
for this: Claude Code treats it as a shell command.)

## Test the script without Claude

```bash
echo '{"prompt":"Fix the login page so it works on phones and push it"}' | python3 prompt-check-hook.py   # prints JSON
echo '{"prompt":"ok"}' | python3 prompt-check-hook.py                                                    # prints nothing
```
