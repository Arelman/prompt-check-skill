# Question bank

Pick at most three, most important first. Every question carries a default. Offer "answer ok to accept all
defaults". Translate into the user's language; the Russian lines are ready to use.

Format when asking (adapt):

> Before I start, three quick points (answer "ok" to take my defaults):
> 1. <question> - default: <default>
> 2. ...

## Change code or a site

| Gap | Question | Default |
|---|---|---|
| done-criterion | How do we confirm it is done? | CI green, change visible at the live URL at 390 and 1440 px; I attach screenshots |
| scope | Anything not to touch? Extras like tests or docs? | Only what you asked; I list other things I notice as follow-ups |
| irreversible | Should I commit and push, or stop before that? | Commit locally, ask before push |
| mode | Propose first, or make the change? | Make the change if it is small, propose first if it spans files |

RU: «Как подтвердим, что готово?» · «Что не трогать? Нужны ли тесты и документация?» ·
«Коммитить и пушить самому или остановиться перед этим?» · «Сначала предложить или сразу править?»

## Write or edit text

| Gap | Question | Default |
|---|---|---|
| reader | Who reads it, and what should they do after? | General reader, one clear next step |
| format | Length, structure, language? | As short as the content allows; plain paragraphs |
| voice | Is there a sample of your own writing or a text you like? | Neutral, direct |
| facts | Are numbers and names given by you, or may I invent plausible ones? | Never invent; I mark gaps with [?] |

RU: «Кто читает и что должен сделать после?» · «Какой объём и язык?» ·
«Есть образец вашего стиля?» · «Цифры и имена даёте вы или можно придумать? (по умолчанию — не придумываю, ставлю [?])»

## Design or layout

| Gap | Question | Default |
|---|---|---|
| criteria | What makes this good for you: three words or criteria? | Coherent identity, clear hierarchy, usable on a phone, not a template look |
| reference | Any reference, competitor or image to match or avoid? | None; I propose two directions first |
| constraints | Fixed colours, fonts, brand rules, dark theme? | Keep what exists |
| check | I will check at phone and desktop width and send screenshots, OK? | Yes |

RU: «Какие три слова или критерия описывают хороший результат?» · «Есть образец или то, чего избегать?» ·
«Что фиксировано: цвета, шрифты, тёмная тема?» · «Проверю на телефоне и десктопе, пришлю скриншоты — ок?»

## Research, legal, money, health

| Gap | Question | Default |
|---|---|---|
| sources | Which sources count (official documents only, or also commentary)? | Primary documents first, with dates |
| freshness | Does it need rules valid today? | Yes: I check current sources, not memory |
| uncertainty | Should I mark what I am unsure of? | Yes, separately at the end |
| decision | What decision will this inform? | Unknown; I answer the question as asked |

RU: «Какие источники считать: только официальные документы или и разбор?» · «Нужны действующие на сегодня нормы?» ·
«Отмечать, в чём не уверен?» · «Какое решение за этим стоит?»

## Plan, strategy, ideas (Propose mode)

| Gap | Question | Default |
|---|---|---|
| constraints | Budget, time, people, hard limits? | State my assumptions explicitly |
| options | How many options, and with what trade-offs? | Three, each with one downside |
| stop | Should I stop after the options? | Yes, change nothing until you pick |

RU: «Бюджет, сроки, ограничения?» · «Сколько вариантов?» · «Остановиться после вариантов?»

## Big or fuzzy project: interview mode

Offer: "This is large enough that a short interview will save rework. I will ask in rounds of three or four
questions with options, then write a SPEC.md for you to approve before I build anything. Start?"

Round 1: goal and audience, what exists today, what is wrong with it, what must not change.
Round 2: scope and structure, priorities (must / nice / later), constraints (time, budget, tools).
Round 3: how success is checked, who approves, first milestone.
End: write `SPEC.md` with goal, audience, scope, out of scope, done-when, open questions. Suggest a fresh
session for the build so it starts from the spec, not the interview.

RU: «Задача большая, короткое интервью сэкономит переделки. Я задам вопросы раундами по 3–4 с вариантами,
потом запишу SPEC.md, вы утвердите, и только после этого начну. Начинаем?»

## Automation or an agent

| Gap | Question | Default |
|---|---|---|
| trigger | What starts it, and how often? | Manual start |
| tools | Which systems may it touch? | Read-only until you say otherwise |
| approvals | Which actions need your yes? | Anything that sends, spends, deletes or publishes |
| stop | When should it stop and report? | Done-criterion met, or two failed attempts |
| failure | What happens if it fails at night? | Do nothing and tell me |

RU: «Что запускает и как часто?» · «К каким системам есть доступ?» · «Какие действия только с вашего «да»?» ·
«Когда останавливаться и отчитываться?» · «Что делать при сбое?»
