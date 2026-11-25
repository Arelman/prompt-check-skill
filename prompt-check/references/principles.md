# Principles digest

A short, paraphrased digest of the guidance behind the checklist. Nothing here is copied from the sources;
read the originals (listed in `sources.md`) for exact wording and current versions, because these pages are
updated often.

## The shortest version

A good request tells a capable newcomer five things: what result is wanted and why, what they cannot find on
their own, what is in and out of bounds (and which actions need a yes), how to tell it is finished, and what
form the answer should take. Everything else in the guides is a refinement of one of those.

## Themes where the sources agree

**Be explicit and direct.** Recent models do what is asked, closely. If more than the minimum is wanted, say
so ("include edge cases and empty states, go beyond the basics"). Leading with an action verb and skipping
preamble helps. A colleague with no context should be able to follow the request; if they would be confused,
so will the model. [BP, BLOG]

**Give the reason.** Explaining why a rule exists lets the model apply it sensibly to cases you did not list.
This is repeated in the general guide, the blog, and the Fable 5 page. [BP, BLOG, F5]

**Show, do not describe, when you can.** Examples steer format and tone more reliably than adjectives. Start
with one; add three to five diverse ones if needed, and make sure the examples contain only patterns you want
copied. Screenshots, files and command output beat descriptions. [BP, BLOG, CC]

**Say what to do, not only what to avoid.** "Write in flowing paragraphs" works better than "no bullet
points". The style of the request leaks into the style of the answer. [BP, BLOG]

**Define success before polishing the wording.** Anthropic's own advice is to settle success criteria and a
way to test them first, and to prompt-engineer only what prompting can fix; some problems are solved by a
different model or setting. Good criteria are specific, measurable, achievable and relevant. [OVR, DEF]

**Give the agent a check it can run.** A pass/fail signal lets the agent iterate to correct without the user
watching. Options run from "keep going until the tests pass" in the prompt, through a goal condition, to a
hook that blocks stopping until a script passes, to a reviewer that has not seen the reasoning. Ask for
evidence (the command and its output, or a screenshot), not for the word "done". [CC, S55]

**Separate the doer from the judge.** Models grade their own work too kindly, especially on subjective
output. A second pass with named criteria, run by a separate agent or session, is far more reliable. Taste
becomes gradable when written as a few criteria with weights. [HARN]

**Keep context lean.** Context is a finite resource; more is not better. Put the minimum that fully describes
the behaviour, curate examples rather than listing every edge case, load material on demand, and restart
from a clean session with a written handoff instead of patching a long, polluted one. [CTX, CC, HARN]

**Ask for uncertainty.** Permission to say "I don't know", and a request for sources and dates on anything
that may have changed, reduces invented answers. [BLOG, S55]

**Put long material first, the question last.** Mark where each document begins and ends; for long inputs
ask for relevant quotes before the analysis. [BP]

**Do not over-engineer the prompt.** Longer is not better. Start simple, add a technique only when it fixes a
specific problem, and test whether it helped. [BLOG, BEA]

## What has changed as models improved

- Structure tags and role lines are optional now; the blog calls them less necessary, while the general guide
  still shows them for complex, mixed content. Use them when the prompt mixes instructions with data or when
  the boundaries must be certain. [BLOG, BP]
- "Think step by step", "be thorough", capital letters and "never" lines are ordinary text, not switches.
  Reasoning depth is controlled by the effort setting; piling on emphasis makes models over-apply a rule. [CC, S55, F52]
- Newer models follow instructions literally and do not silently generalize them from one item to another;
  say the scope ("every section, not just the first"). [O48, S5]
- Some models verify on their own, so a blanket "verify everything" can waste tokens; a specific check the user
  cares about is still worth stating. [O5]
- Prompting is converging with context engineering: less scaffolding, more curation of what the model sees,
  and standing rules belong in CLAUDE.md files, skills or hooks rather than being retyped. [BLOG, CC]

## Model notes (for chat and Claude Code users)

Each model page is mainly for developers, but several findings change what a user should say. Re-check them
when a newer page appears.

- **Sonnet 5.5:** at lower effort in long agentic work it may stop to check in; it tends to add tests, docs and
  small files unprompted unless told to stay in scope; when you ask for ideas or a plan, say "stop after the
  options"; for facts that may have changed it can answer from memory unless asked to search. [S55]
- **Opus 5.5:** can be told which pasted text is the user's own and which came from elsewhere. A line telling
  it to treat earlier answers as settled makes it less likely to correct them. [O55]
- **Opus 5:** answers run long by default; asking for brevity works, lowering effort does not. It may widen scope; a
  line like "deliver what was asked, flag a better approach in one sentence, do not silently change the task"
  helps. [O5]
- **Fable 5 / 5.1 / 5.2:** short instructions are enough; state boundaries; give the reason; ask it to ground
  progress claims in real tool results. Approvals should be specific ("yes, run the migration on staging").
  An absolute "never" is read as absolute. A hard style rule can make prose choppy. Final reports should stand
  alone for a reader who saw none of the work. Saying the code is the model's own invites it to restructure;
  leave that out where changes should stay minimal. [F5, F51, F52]
- **Haiku 5.5:** with a long system prompt at low effort it may stop early; higher effort helps. [H55]

## MIT

- **Effective prompts (Sloan teaching technologies):** provide context, be specific, build on the conversation;
  start a new chat for a new topic; the skill that lasts is stating the problem (focus, scope, boundaries)
  more than polishing wording; expect errors and bias, and check results; read data-privacy guidance
  before pasting anything sensitive. [MIT-ESS]
- **Study of prompts and model upgrades:** in a large experiment, about half the gain from a better model came
  from users changing their prompts, and prompting looked like communication rather than coding. Silent
  automatic rewriting of users' prompts hurt results in that image task, because it changed the meaning. The
  authors caution that the finding is for tasks with a clear target. This is why this skill asks and
  restates, and never replaces the user's request behind their back. [MIT-STUDY]
- **Templates:** a library of proven prompts for recurring tasks beats inventing one each time. [MIT-TPL]

## Tag legend

BP, BLOG, OVR, DEF, CC, CTX, BEA, HARN, S55, S5, O48, O5, O55, F5, F51, F52, H55, MIT-ESS, MIT-STUDY, MIT-TPL
are defined in `sources.md`.
