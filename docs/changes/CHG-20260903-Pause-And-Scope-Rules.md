---
type: "[[change]]"
id: CHG-20260903-Pause-And-Scope-Rules
title: "One pause rule stated once, six one-sentence rules the guides state, and a harness that greps for both"
status: merged
owner: user:edwin
created: 2026-09-03
updated: 2026-09-03
source: ["project-os-dev FEAT-0024, TASK-0090 to TASK-0095", "project-os-dev docs/reference/Prompting-Guide-Review-2026-09-03.md, findings 2.1, 2.3, 5.3, 6.1, 6.2, 7.1, 7.2, 7.4, 8.1"]
commit: "0154e9d, bb6eb70, 7ae32ed, f5bf4f5, 1760161, 9b53acb, 79e0332"
pr: ""
impacts: ["tools/instructions/LIFECYCLE.md", "tools/instructions/HOOKS.md", "tools/instructions/QUALITY.md", "tools/instructions/HANDOFF.md", "tools/instructions/MARKDOWN.md", "tools/skills/README.md", "tools/skills/status-transition/SKILL.md", "tools/skills/issue-intake/SKILL.md", "tools/skills/feature-scaffold/SKILL.md", "tools/skills/release-prep/SKILL.md", "tools/skills/close-out/SKILL.md", "tools/skills/test-authoring/SKILL.md", "tools/skills/independent-review/SKILL.md", "tools/scripts/generate-adapters.py", "tools/scripts/test-pause-rule.sh", "docs/PHASES.md", ".claude/agents/planner.md", ".cursor/rules/lifecycle.mdc", ".cursor/rules/quality.mdc", ".cursor/rules/markdown.mdc"]
issues: []
features: []
related: ["[[INSTR-LIFECYCLE]]", "[[INSTR-QUALITY]]", "[[INSTR-HANDOFF]]", "[[INSTR-MARKDOWN]]", "[[CHG-20260903-Prompting-Guide-Contradictions]]"]
reviewed_by: "model:claude-opus-5[1m]"
review_date: 2026-09-03
review_verdict: changes-requested
---

# One pause rule, and the scope rules the guides state

## Summary

An agent reading the template was told to stop and ask the user in twelve places across nine files, each in its own words and none saying what to finish first. The review found eleven; the independent review of this change found the twelfth, in `docs/PHASES.md`, which restates the phase-alignment rule for repos that adopt phases. LIFECYCLE.md now states the rule once, under "Execution", in a section called "When to pause for the user": pause only for a destructive or irreversible action, a real scope change, or input only the user can provide; do everything that does not depend on the answer first, then ask at the end of a turn that also delivers that progress. Every other site names the decision the user owns and links that section.

The same pass adds six rules the Claude 5 prompting guides state and project-os did not, each one or two sentences in the file that owns the neighbouring rule:

1. **Scope of a change** (LIFECYCLE.md): a bug, a cleanup or a missing abstraction the task did not ask for is an `ISS-*` at `triage` or a follow-up in the summary, not a change in this diff. When the wording admits two readings, implement the one it most directly supports and state the assumption.
2. **Ambiguity has a threshold** (issue-intake step 1, the planner prompt): the five-test check still runs on every intake; a failure is the user's decision only when the readings lead to materially different work. The planner allocates what is settled and returns the ambiguities beside it, instead of returning nothing.
3. **Evidence in the final message** (QUALITY.md): each progress claim is audited against a tool result from this session; a failing test is reported with its output, a skipped step is named.
4. **Roads not taken and the user's exact words** (HANDOFF.md): two new handoff items, both recorded in the task note's Notes section.
5. **Edit, do not rewrite** (MARKDOWN.md): a rewrite drops `reviewed_by`, `review_verdict`, `verification_waiver` and `origin:` without failing anything.
6. **Checklist numbers are not an order** (skills README); **a TST note is the record and scratch checks are not kept** (test-authoring); **the reviewer reports every finding** and the repro filter moves to transcription (independent-review).

## Impact

- The twelve stop-points read as one rule with twelve decisions. Close-out step 1 also says what to do with the rest of a close-out when one test blocks it: finish every other part, then say what was left out.
- `tools/scripts/test-pause-rule.sh` is new. It asserts the rule is stated in exactly one file under a heading that exists, that all twelve sites in nine files link it, that no old phrasing remains, and that the generated planner is current. project-os-dev TST-0005 runs it. The first review round found that a renamed heading, a dropped link in LIFECYCLE.md or release-prep, and the PHASES.md site were all invisible to the first version; the second version sees them.
- LIFECYCLE.md grew from 1,343 to 1,632 words (the first version of this note said 1,599, which was the count after the first commit alone; the review corrected it). project-os-dev FEAT-0026 trims it next; the new rules were written without anecdotes so the trim does not have to re-trim them.
- The reviewer's schema in project-os-dev's `review-external.py` gains a `reproduced` label and stops dropping unreproduced findings. A human transcribing a verdict now sees the leads too.
- Downstream repos pick everything up at the next template sync plus a generator run.

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

The feature, its six tasks and the test note live in project-os-dev (FEAT-0024, TASK-0090 to TASK-0095, TST-0005), which tracks this template's development.

## Follow-ups

- [ ] Sync to the downstream repos and re-run the generator in each.
- [ ] project-os-dev's `review-external.py` docstring header still says QUALITY.md requires a different model family, which ISS-0041 retired. Noticed while changing the same file; left for its own change under the scope rule this note adds.
