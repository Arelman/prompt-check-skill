#!/usr/bin/env python3
"""UserPromptSubmit hook for the prompt-check skill.

Why a hook: a skill is chosen by the model, so it can be skipped. A hook runs on every prompt and
reliably reminds Claude to apply the skill. This script decides, deterministically and cheaply,
which prompts deserve the reminder, so short replies are never slowed down.

It reads the hook JSON from stdin, and prints a JSON object with `additionalContext` when the prompt
is substantive. It never blocks a prompt and never fails loudly: any error means "say nothing".
"""
import json
import re
import sys

MIN_CHARS = 40

# Short acknowledgements and continuations, in Russian and English.
ACK = re.compile(
    r"^\s*(да|нет|ок|окей|ok|okay|yes|no|sure|go|готово|давай|продолжай|продолжи|делай|"
    r"поехали|принято|спасибо|thanks|thank you|continue|go on|proceed|done|"
    r"да,? делай|да,? давай|ага|угу|хорошо|ладно)\W*$",
    re.IGNORECASE,
)
WAIVER = re.compile(
    r"(без вопросов|не задавай вопрос|сразу делай|просто сделай|no questions|just do it|skip the check)",
    re.IGNORECASE,
)

AUTOMATED = re.compile(
    r"(<task-notification|<side-sessions-event|<ci-monitor-event|This session is being continued)",
    re.IGNORECASE,
)

REMINDER = (
    "prompt-check: before doing the work, apply the prompt-check skill to the user's latest message. "
    "Triage first: skip if it is a trivial reply, an already-clear one-liner, or nobody can answer. "
    "Otherwise ask at most three short questions, each with a default, only for gaps that would change the "
    "result (done-criterion, scope/approvals, goal, context not findable, format). Do not announce the check."
)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    prompt = (data.get("prompt") or "").strip()
    if len(prompt) < MIN_CHARS:
        return
    if prompt.startswith("/"):
        return
    if ACK.match(prompt) or WAIVER.search(prompt):
        return
    # Turns started by automation (background tasks, other sessions, context-compaction summaries)
    # carry no human to answer, so they get no reminder.
    if AUTOMATED.search(prompt[:400]):
        return
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": REMINDER,
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
