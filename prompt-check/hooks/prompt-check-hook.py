#!/usr/bin/env python3
"""UserPromptSubmit hook for the prompt-check skill.

Why a hook: a skill is chosen by the model, so it can be skipped. A hook runs on every prompt and
reliably reminds Claude to apply the skill. This script decides, deterministically and cheaply,
which prompts deserve the reminder, so replies that need no check are never slowed down.

It reads the hook JSON from stdin and prints a JSON object with `additionalContext` when the prompt
is substantive. It never blocks a prompt and never fails loudly: any error means "say nothing".

Three layers decide that a message needs no reminder (the same rules, in prose, are in
references/skip-rules.md and SKILL.md; keep them in step):

  1. Vocabulary: the whole message is made of acknowledgement, continuation, thanks, choice and similar
     words (Russian and English), numbers, or single option letters.
  2. Context: the message is short and the assistant's last message asked a question or offered options,
     so the message is most likely an answer.
  3. Length: very short messages are never worth a reminder. Everything else gets the reminder, and the
     model applies the principle in SKILL.md to decide.
"""
import json
import os
import re
import sys

MIN_CHARS = 15          # below this, a message cannot hold a real task
SHORT_WORDS = 15        # "short" for the context rule
SHORT_CHARS = 200
MAX_VOCAB_TOKENS = 10   # vocabulary-only messages longer than this are not treated as acknowledgements

# Words that, on their own, carry no new task. Written normalised: lower case, "ё" as "е".
VOCAB_RU = """
да нет не надо нужно ок окей окэй оке ага угу ладно хорошо ясно понятно понял поняла принято
отлично супер круто класс здорово прекрасно замечательно спасибо благодарю спс пасиб пожалуйста
давай делай делайте поехали погнали продолжай продолжи продолжайте дальше далее вперед
идет пойдет подходит годится согласен согласна верно точно именно конечно разумеется естественно
безусловно ну так вот тогда тоже и или а же уже норм нормально стоп подожди погоди отмена отбой
первый второй третий четвертый последний первая вторая третья первое второе третье
вариант номер оба обе все любой любое никакой ничего это то тот эта этот эти
"""
VOCAB_EN = """
yes no yep yeah nope nah ok okay sure fine good great nice cool perfect thanks thank you thx ty please pls
go ahead on continue proceed next done right correct exactly got it understood agreed sounds looks
that works for me lgtm stop wait cancel do option first second third last both all none any either
"""
VOCAB = set((VOCAB_RU + " " + VOCAB_EN).split())
OPTION_LETTERS = set("abcdабвг")

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
    "Triage first: skip if it only accepts, declines, chooses or continues something already on the table, "
    "is an already-clear one-liner, or nobody can answer. "
    "Otherwise ask at most three short questions, each with a default, only for gaps that would change the "
    "result (done-criterion, scope/approvals, goal, context not findable, format). Do not announce the check."
)


def normalize(text: str) -> str:
    text = text.lower().replace("ё", "е")
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)  # punctuation and emoji become spaces
    return re.sub(r"\s+", " ", text).strip()


def vocabulary_only(prompt: str) -> bool:
    """Layer 1: every token is a known acknowledgement/choice word, a 1-2 digit number or an option letter."""
    tokens = normalize(prompt).split()
    if not tokens:
        return True  # nothing but punctuation or emoji
    if len(tokens) > MAX_VOCAB_TOKENS:
        return False
    return all(t in VOCAB or re.fullmatch(r"\d{1,2}", t) or t in OPTION_LETTERS for t in tokens)


def last_assistant_text(path: str) -> str:
    """Text of the most recent assistant message that has any, read from the tail of the transcript."""
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            f.seek(max(0, size - 400_000))
            chunk = f.read().decode("utf-8", errors="replace")
    except Exception:
        return ""
    for line in reversed(chunk.splitlines()):
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get("type") != "assistant" or o.get("isSidechain"):
            continue
        content = (o.get("message") or {}).get("content")
        if isinstance(content, list):
            text = "\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
        elif isinstance(content, str):
            text = content
        else:
            text = ""
        if text.strip():
            return text.strip()
    return ""


def assistant_asked(text: str) -> bool:
    """True if the assistant's message ends in a question or offers options to choose from."""
    tail = text[-700:]
    if "?" in tail:
        return True
    has_list = re.search(r"(?m)^\s*(\d+[.)]|[-*•])\s+", tail)
    asks_choice = re.search(r"(по умолчанию|default|вариант|option|ответьте|answer|выберите|choose)", tail, re.I)
    return bool(has_list and asks_choice)


def short_reply(prompt: str) -> bool:
    return len(prompt) <= SHORT_CHARS and len(prompt.split()) <= SHORT_WORDS


def needs_reminder(data: dict) -> bool:
    prompt = (data.get("prompt") or "").strip()
    if len(prompt) < MIN_CHARS or prompt.startswith("/"):
        return False
    if WAIVER.search(prompt) or AUTOMATED.search(prompt[:400]):
        return False
    if vocabulary_only(prompt):                                                # layer 1
        return False
    if short_reply(prompt) and assistant_asked(last_assistant_text(data.get("transcript_path") or "")):
        return False                                                           # layer 2
    return True                                                                # layer 3: the model decides


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if needs_reminder(data):
        print(json.dumps({
            "hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": REMINDER}
        }, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
