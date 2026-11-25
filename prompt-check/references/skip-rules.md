# When to skip the check

The check exists to catch gaps in a request that starts new work. A message that only moves an existing
conversation along has no such gap. Three layers decide this, from the most mechanical to the most
judgemental. The hook (`hooks/prompt-check-hook.py`) applies layers 1 and 2 deterministically; the model
applies all three when the hook is off or lets a message through.

## Layer 1. Reply words (a list)

A message is exempt when it consists only of words like these, in any combination, with any punctuation or
emoji. Case and "ё" versus "е" do not matter.

| Kind | Russian | English |
|---|---|---|
| Agree, accept | да, ок, окей, ага, угу, ладно, хорошо, ясно, понятно, принято, согласен, верно, точно, именно, конечно, подходит, годится, норм, идёт, пойдёт | yes, yeah, ok, okay, sure, fine, good, right, correct, exactly, agreed, got it, sounds good, works for me, lgtm |
| Decline, stop | нет, не надо, стоп, подожди, отмена, отбой | no, nope, nah, stop, wait, cancel |
| Continue | давай, делай, поехали, погнали, продолжай, дальше, вперёд | go ahead, go on, continue, proceed, next, do it |
| React, thank | отлично, супер, круто, класс, здорово, спасибо, благодарю, спс, пожалуйста | great, nice, cool, perfect, thanks, thank you, thx, please |
| Choose | 1, 2, 3 · «1 и 3» · А, Б, В, Г · «вариант 2» · первый, второй, последний · оба, все, любой | 1, 2, 3 · "1 and 3" · A, B, C, D · "option 2" · first, second, last · both, all, any |
| Filler | ну, так, вот, тогда, тоже, и, или, а, же, уже | well, so, then, also, and, or |

Examples that are exempt: «ага, давай», «Да!», «👍», «2 и 3», «вариант Б», «ну ок, спасибо», "sure, go ahead",
"option 2 please".

Examples that are **not** exempt by this layer, because one word is a new task or detail: «да, но без
тёмной темы», «давай сделаем сайт», «2, и ещё поправь шрифт», "yes, and also push it".

A vocabulary-only message of more than ten words is not treated as a reply.

## Layer 2. Context: it answers what was just asked

If the assistant's last message asked a question or offered options, and the user's reply is short (up to
about fifteen words), treat it as an answer, not as a new request, even if the words are not on the list:

> Assistant: "Which should I do first: the footer or the header?"
> User: "the footer, and keep the colours"  → an answer; no check.

The same goes for a reply to an offer ("Want me to push it?") or to a numbered list of options. A reply that
is long, or that opens a new subject, is a new request and goes to layer 3.

## Layer 3. Principle, for everything else

**A message is exempt when it only accepts, declines, chooses or continues something already on the table,
and adds no new task, constraint or fact that would change the work.**

Apply it like this:

1. Ask what the message adds. If an agent that had read the conversation would have to guess nothing new,
   skip.
2. If the message mixes an acceptance with something new, skip the acceptance and check only the new part:
   «да, но без пуша» → accept, and treat «без пуша» as a constraint to honour. Do not re-open the whole task.
3. If the new part is itself a request, check that part as usual.
4. Short is not the same as clear. «почини кнопку и выложи» is only 22 characters but names an action
   with no done-criterion and an irreversible step; check it. «rename fmt_date to format_date everywhere»
   is long enough to look like a task and is fully specified; skip it.
5. A single word that is an instruction rather than a reply («проверь», «запусти», «deploy») is clear in
   context if it refers to something just discussed (skip) and unclear out of the blue (check).
6. When in doubt after steps 1 to 5, skip silently if the work is easy to undo and ask one question if it is
   not (publishing, deleting, sending, spending).

## Always skipped, whatever the content

Slash commands; messages that waive questions in words («без вопросов», «сразу делай», "no questions", "just
do it"); messages from automation or other sessions; and any run where nobody can answer.

A leading `!` cannot serve as a "skip" marker: Claude Code treats it as a shell command.

## Keeping the layers in step

The vocabulary in layer 1 lives in two places: the table above and the `VOCAB_RU` / `VOCAB_EN` strings in the
hook. When you add a word, add it in both, then run `python3 scripts/validate.py`.
