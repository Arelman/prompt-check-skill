# prompt-check

An Agent Skill for Claude Code (and other tools that read `SKILL.md`) that checks each substantive request
against published prompting guidance and asks a few short questions when something that would change the
result is missing. If nothing is missing, it stays out of the way.

Русская версия ниже.

## What it does

When you send a request, the skill:

1. **Skips** trivial replies, slash commands, already-clear one-liners, runs where nobody can answer, and
   anything you wave through with "no questions" or "just do it".
2. **Finds the mode:** explore, propose, or do. Loose requests are fine when exploring; gaps are costly when doing.
3. **Checks five things:** how to tell the work is done, scope and approvals, the goal and its reason, context
   that cannot be found in the files, and output format and reader.
4. **Asks at most three questions**, each with a default you can accept by answering "ok", only for gaps that
   change the work. For a large, fuzzy project it offers a short interview that ends in a `SPEC.md`.
5. **Restates the brief** in a few lines, does the work, and reports evidence rather than the word "done".

It never silently rewrites your request. MIT Sloan researchers found that automatic prompt rewriting that
changes meaning can hurt results, so this skill asks and restates instead.

## Install

```bash
git clone https://github.com/Arelman/prompt-check-skill.git
mkdir -p ~/.claude/skills
cp -r prompt-check-skill/prompt-check ~/.claude/skills/
```

Restart your session. The skill lives at `~/.claude/skills/prompt-check/`. To install for one project only, copy
it to `<project>/.claude/skills/` instead.

## Make it run on every prompt (optional)

A skill is chosen by the model from its description, so it can be skipped now and then. For a guaranteed
reminder on every substantive prompt, add the small hook in
[`prompt-check/hooks/README.md`](prompt-check/hooks/README.md). It is opt-in and never blocks a prompt.

## What is inside

| Path | Purpose |
|---|---|
| `prompt-check/SKILL.md` | The workflow Claude follows |
| `prompt-check/references/checklist.md` | Every check, why it matters, source, question templates |
| `prompt-check/references/question-bank.md` | Questions with defaults by task type |
| `prompt-check/references/principles.md` | Paraphrased digest of the guidance, with model notes |
| `prompt-check/references/examples.md` | Worked dialogues and the review report format |
| `prompt-check/references/sources.md` | Sources, how much of each was read, retrieval dates |
| `prompt-check/hooks/` | Optional `UserPromptSubmit` hook |
| `prompt-check/evals/` | Eight test cases (four should ask, four should not) |

## Based on

Anthropic's prompting best practices, its blog on prompt engineering, the Claude Code best-practices page, the
success-criteria and harness-design posts and the model-specific prompting pages, plus MIT Sloan's prompting
guide, study and templates. Everything is paraphrased and linked; see
[`sources.md`](prompt-check/references/sources.md), which also says how much of each page was read.

## Limits, stated plainly

- The skill is guidance for a model, not a program. How strictly a given model follows it varies.
- The tests in `evals/` are written but have not been run with an independent model. They follow the format
  used by `claude plugin eval`; run them yourself before relying on the skill.
- The guidance it is built on changes with each model release. Check the sources when behaviour drifts.
- Not produced, endorsed or reviewed by Anthropic or MIT.

## License

MIT, see [LICENSE](LICENSE).

---

# prompt-check (по-русски)

Навык (Agent Skill) для Claude Code и других инструментов, читающих `SKILL.md`. Он проверяет каждый
содержательный запрос по опубликованным методикам промптинга и задаёт несколько коротких вопросов, если не
хватает того, что изменит результат. Если всё нужное есть, навык молчит.

## Что делает

1. **Пропускает** короткие ответы («да», «готово»), слэш-команды, уже ясные запросы в одну строку, запуски без
   человека и всё, что вы пускаете без вопросов фразой «без вопросов» или «сразу делай».
2. **Определяет режим:** исследовать, предложить или сделать.
3. **Проверяет пять вещей:** как понять, что готово; границы и согласования; цель и причина; контекст, которого
   нет в файлах; формат ответа и читатель.
4. **Задаёт не больше трёх вопросов**, у каждого есть вариант по умолчанию («ок» принимает все). Для большого
   неясного проекта предлагает интервью, которое заканчивается файлом `SPEC.md`.
5. **Повторяет задачу** в нескольких строках, делает работу и приносит доказательство, а не слово «готово».

Ваш запрос он молча не переписывает: по данным MIT Sloan, автоматическая переделка запроса, меняющая смысл,
ухудшает результат. Поэтому навык спрашивает и пересказывает.

## Установка

```bash
git clone https://github.com/Arelman/prompt-check-skill.git
mkdir -p ~/.claude/skills
cp -r prompt-check-skill/prompt-check ~/.claude/skills/
```

Перезапустите сессию. Чтобы поставить только на один проект, копируйте в `<проект>/.claude/skills/`.

## Чтобы срабатывал на каждый запрос (по желанию)

Навык выбирается моделью по описанию и иногда может быть пропущен. Для гарантии добавьте маленький hook из
[`prompt-check/hooks/README.md`](prompt-check/hooks/README.md). Он необязателен и никогда не блокирует запрос.

## Ограничения

- Это инструкция для модели, а не программа; строгость выполнения зависит от модели.
- Тесты в `evals/` написаны, но независимой моделью не запускались. Запустите их сами, прежде чем полагаться на навык.
- Методики меняются с каждым релизом моделей; при расхождениях сверяйтесь с источниками.
- Проект независимый, Anthropic и MIT его не выпускали и не одобряли.

Лицензия: MIT.
