---
type: "[[change]]"
id: CHG-20260903-Writing-Rules-And-Lengths
title: "WRITING.md covers the final message; snapshot fields get a length"
status: merged
owner: user:edwin
created: 2026-09-03
updated: 2026-09-03
source: ["project-os-dev FEAT-0025, TASK-0096, TASK-0097", "project-os-dev docs/reference/Prompting-Guide-Review-2026-09-03.md, findings 4.2, 5.1, 5.2"]
commit: "e490420, e4d0688"
pr: ""
impacts: ["tools/instructions/WRITING.md", "AGENTS.md", "tools/instructions/SNAPSHOT.md", "docs/__templates__/change.md", "docs/__templates__/issue.md", "docs/__templates__/feature.md", ".cursor/rules/snapshot.mdc"]
issues: []
features: []
reviewed_by: model:claude-opus-5[1m]
review_date: 2026-09-03
review_verdict: approved
related: ["[[INSTR-WRITING]]", "[[INSTR-SNAPSHOT]]", "[[CHG-20260831-Writing-Rules]]", "[[CHG-20260903-Pause-And-Scope-Rules]]"]
---

# Writing rules for the final message, and lengths for the snapshot

## Summary

WRITING.md now has rules for the message a person reads after a long run, not only for note prose. Four rules are added as 7 to 10. Say what you mean instead of reaching for a metaphor. Write the final message for a reader who did not watch the work, with no arrow chains or invented labels. Keep it short by leaving things out, not by compressing them. Open with one line on what you are about to do, and close with a recap that stands alone. A short section says how a line between tool calls differs from the final message. AGENTS.md links these rules instead of asking for a fixed preamble.

The second half is length. A snapshot title is at most twelve words, and because the sync script derives it from the note that is a limit on note titles. The goal and note prose on any snapshot item, and the focus note, are at most two sentences each. The longer text goes to the note's own sections. The change, issue and feature templates ask for a two-or-three-sentence, point-first summary.

## Impact

- An agent writing its closing message has a rule to follow and a reader in mind. Whether it follows the rule is judged by the independent review of the first notes written afterwards, which is the acceptance recorded on project-os-dev FEAT-0025.
- Rule 2 of WRITING.md lost its own figure of speech; rule 7 quotes it as the example. The six instruction files that still carry the pattern are rewritten by project-os-dev FEAT-0026.
- Existing long titles and focus notes are not backfilled, and no validator check enforces the numbers. Both wait for a counted violation set (ADR-0011).
- Downstream repos pick the rules up at the next template sync plus a generator run.

## Documentation Coverage (All Types Considered)
Set each item to one of: `updated`, `new`, `not-applicable`, `deferred`.

- features: not-applicable
- requirements: not-applicable
- tasks: not-applicable
- issues: not-applicable
- tests: not-applicable
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable
- changes: new
- snapshot: not-applicable

The feature and its two tasks live in project-os-dev (FEAT-0025, TASK-0096, TASK-0097).

## Follow-ups

- [ ] Count the titles over twelve words and the goal and note fields over two sentences across the fleet, then decide the validator check and the backfill.
- [ ] Sync to the downstream repos and re-run the generator in each.
