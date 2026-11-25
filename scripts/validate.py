#!/usr/bin/env python3
"""Structural checks for the prompt-check skill. Run from the repository root:

    python3 scripts/validate.py [path/to/prompt-check]

Checks: frontmatter, name matches folder, description length, every referenced file exists, Markdown links
between files resolve, eval cases have the required files, hook behaves as intended, no stray private data.
Exits 1 if anything fails. It checks structure, not whether a model follows the skill well.
"""
import json
import os
import re
import subprocess
import sys

root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "prompt-check")
problems = []
ok = lambda m: print("ok   ", m)
bad = lambda m: (print("FAIL ", m), problems.append(m))

# 1. Frontmatter
text = open(os.path.join(root, "SKILL.md"), encoding="utf-8").read()
m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
if not m:
    bad("SKILL.md has no frontmatter")
    fm = {}
else:
    fm = dict(re.findall(r"^(\w[\w-]*):\s*(.*)$", m.group(1), re.M))
    ok("frontmatter parsed, keys: " + ", ".join(fm))
name = fm.get("name", "")
(ok if name == os.path.basename(root) else bad)(f"name '{name}' matches folder '{os.path.basename(root)}'")
(ok if re.fullmatch(r"[a-z0-9-]{1,64}", name) else bad)("name is lowercase letters, digits, hyphens")
desc = fm.get("description", "")
(ok if 0 < len(desc) <= 1024 else bad)(f"description length {len(desc)} (limit 1024)")
lines = text.count("\n")
(ok if lines < 500 else bad)(f"SKILL.md is {lines} lines (limit 500)")

# 2. Referenced files exist
for ref in sorted(set(re.findall(r"`((?:references|hooks|evals)/[\w./-]+)`", text))):
    (ok if os.path.exists(os.path.join(root, ref)) else bad)(f"referenced file exists: {ref}")

# 3. Relative Markdown links resolve
for dirpath, _, files in os.walk(root):
    for f in files:
        if f.endswith(".md") and "evals" not in dirpath:
            p = os.path.join(dirpath, f)
            for link in re.findall(r"\]\((?!https?:|#|mailto:)([^)\s]+)\)", open(p, encoding="utf-8").read()):
                target = os.path.normpath(os.path.join(dirpath, link.split("#")[0]))
                (ok if os.path.exists(target) else bad)(f"link in {os.path.relpath(p, root)} -> {link}")

# 4. Eval cases
evals = os.path.join(root, "evals")
cases = sorted(d for d in os.listdir(evals) if os.path.isdir(os.path.join(evals, d)))
for c in cases:
    d = os.path.join(evals, c)
    need = ["prompt.md", "case.yaml"]
    miss = [n for n in need if not os.path.exists(os.path.join(d, n))]
    gdir = os.path.join(d, "graders")
    graders = sorted(os.listdir(gdir)) if os.path.isdir(gdir) else []
    good = all(open(os.path.join(gdir, g), encoding="utf-8").read().startswith("---\ntype: llm") for g in graders)
    yaml = open(os.path.join(d, "case.yaml"), encoding="utf-8").read() if not miss else ""
    fine = not miss and graders and good and f"name: {c}" in yaml and 'schema_version: "1.1"' in yaml
    (ok if fine else bad)(f"eval case {c}: {len(graders)} graders")

# 5. Hook behaviour
hook = os.path.join(root, "hooks", "prompt-check-hook.py")
def run(prompt):
    r = subprocess.run([sys.executable, hook], input=json.dumps({"prompt": prompt}), capture_output=True, text=True)
    return r.returncode, r.stdout.strip()
expect = [
    ("Fix the login page so it works on phones and push it to main", True),
    ("Исправь стрелку у кнопки «Заполнить бриф» и выложи на боевой сайт", True),
    ("ok", False), ("да, делай", False), ("/ship", False),
    ("just do it however you think best, this is a long enough message to pass the length gate", False),
    ("без вопросов: перепиши этот абзац покороче, он слишком длинный для слайда", False),
    ("This session is being continued from a previous conversation that ran out of context. " * 2, False),
]
for prompt, fires in expect:
    rc, out = run(prompt)
    good = rc == 0 and (bool(out) == fires) and (not out or "additionalContext" in json.loads(out)["hookSpecificOutput"])
    (ok if good else bad)(f"hook {'fires' if fires else 'is silent'}: {prompt[:50]!r}")
rc, out = subprocess.run([sys.executable, hook], input="not json", capture_output=True, text=True).returncode, ""
(ok if rc == 0 else bad)("hook exits 0 on malformed input")

# 6. Private data scan (extend the patterns for your own case)
patterns = [r"\b\d{12}\b", r"\+\d[\d ()-]{9,}", r"[\w.+-]+@(gmail|yandex|mail)\.\w+", r"sk-[A-Za-z0-9]{20,}", r"gh[pousr]_[A-Za-z0-9]{20,}"]
hits = []
for dirpath, _, files in os.walk(os.path.dirname(root)):
    if ".git" in dirpath.split(os.sep):
        continue
    for f in files:
        if f.endswith((".md", ".py", ".yaml", ".json")):
            p = os.path.join(dirpath, f)
            t = open(p, encoding="utf-8", errors="replace").read()
            for pat in patterns:
                if re.search(pat, t):
                    hits.append((os.path.relpath(p, os.path.dirname(root)), pat))
(ok if not hits else bad)("no obvious private data" if not hits else f"possible private data: {hits}")

print("\n%d problem(s)" % len(problems))
sys.exit(1 if problems else 0)
