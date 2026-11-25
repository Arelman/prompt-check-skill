# Worked examples

All examples are invented. Questions are shown in English and Russian; use the user's language.

## 1. Do mode, real gaps: ask three questions with defaults

**User:** "The yellow arrow next to the Fill brief button isn't showing up. Fix it and push to main."

**Check:** goal is clear; done-criterion missing (previous fix did not show up); scope clear; evidence not
named. Push is explicitly requested, so no approval question is needed.

**Reply:**

> Before I start, two quick points (answer "ok" to take my defaults):
> 1. How do we confirm it is fixed? Default: CI green, then I open the live page at 390 and 1440 px in both
>    themes and attach screenshots.
> 2. If the live page does not show it after deploy, should I keep investigating without asking? Default: yes,
>    until it shows or I find a blocker, then report.

RU: «Перед началом два коротких вопроса (ответьте «ок», чтобы принять мои значения по умолчанию): 1. Как
подтвердим, что исправлено? По умолчанию: CI зелёный, затем открываю боевую страницу на 390 и 1440 px в обеих
темах и прикладываю скриншоты. 2. Если после деплоя на странице не видно, продолжать искать причину без
вопросов? По умолчанию: да, пока не появится или не найду препятствие, потом отчёт.»

After "ok": brief (3 lines) → work → run the check → report with screenshots.

## 2. Already clear: do not ask

**User:** "In `utils.py` rename `fmt_date` to `format_date` everywhere and run the tests."

Goal, scope and check are all present. Say nothing about the check; do the task. Report the test output.

## 3. Propose mode: options, no questions, stop

**User:** "Suggest two directions for restructuring the course page."

The request is exploratory and says "suggest". Give two directions with one downside each and stop. Do not
edit files. Do not ask for a done-criterion.

## 4. Large and fuzzy: offer the interview

**User:** "I want to rework the whole site, make it more suitable for me."

Too large and too open for three questions. Offer:

> This is big enough that a short interview will save rework. I will ask in rounds of three or four questions
> with options, then write a SPEC.md for your approval before I change anything. Start?

RU: «Задача большая, короткое интервью сэкономит переделки. Задам вопросы раундами по 3–4 с вариантами, потом
запишу SPEC.md, и только после вашего одобрения что-то меняю. Начинаем?»

## 5. Nobody to ask: state assumptions

Running as a scheduled or background task, or started by another session. Do not ask.

> Assumptions: only the `docs/` folder is in scope; done means the link checker exits 0; nothing is pushed.
> (then the work)

## 6. Facts that may have changed

**User:** "How much does it cost to register a company there, and is it OK for foreigners? It's fine, right?"

Two issues: facts that change, and a leading question. Do not just agree. Ask one question if it changes the
search: "Should I cite the official document and date, and mark what I am unsure of? Default: yes." Then
answer on the sources, and say what would change the conclusion.

## 7. Pressure instead of a criterion

**User:** "You wasted my tokens again. Do it properly this time."

Do not apologise at length and do not add extra caution. The missing piece is the criterion. Ask one
question: "What would you see on screen if it were right?" Default: "the change visible on the live page,
checked at phone width". Then proceed.

## 8. Sensitive data typed into the chat

**User:** (types a password to let you run a system command)

Use it only if the task cannot be done otherwise, never write it to a file or memory, and mention once that a
safer way exists (run the command in your own terminal, or set up a narrow no-password rule).

---

## Review report format (when asked to review a prompt)

Use this when the user says "check my prompt", "разбери мой промпт" and so on. Keep it short.

```
Prompt review

| Check | Result | Note |
|---|---|---|
| Done-criterion | missing | nothing says how to confirm it worked |
| Scope / approvals | ok | push explicitly requested |
| Goal and reason | partial | goal clear, reason missing |
| Context not findable | ok | |
| Format and reader | missing | length and audience not stated |

Fix first: 1) add how to confirm, 2) add the reason, 3) say the reader.

Rewritten (for you to edit, not applied):
<one improved version in the user's own voice, changing as little as possible>
```

Show the rewrite as a suggestion. Do not substitute it for the user's original without their say-so: silent
rewriting can change what was meant.
