---
type: "[[change]]"
id: CHG-20260903-Instruction-Weight
title: "Five instruction files carry rules and reasons, not history"
status: merged
owner: user:edwin
created: 2026-09-03
updated: 2026-09-03
source: ["project-os-dev FEAT-0026, TASK-0098 to TASK-0101, REQ-0026", "project-os-dev docs/reference/Prompting-Guide-Review-2026-09-03.md, findings 4.1, 4.3, 4.4"]
commit: "38db9ad, 244f0e6, cb92705, e6b33a5, 6acf773, 28c857a, 74753d1, 2025f32"
pr: ""
impacts: ["tools/instructions/LIFECYCLE.md", "tools/instructions/STATUSES.md", "tools/instructions/TESTING.md", "tools/instructions/QUALITY.md", "tools/instructions/DECISIONS.md", "tools/instructions/TAXONOMY.md", "tools/skills/feature-scaffold/SKILL.md", "docs/__templates__/feature.md", "docs/__templates__/test.md", "tools/scripts/generate-adapters.py", "tools/scripts/validate-docs.py", ".claude/skills/*/SKILL.md", ".cursor/rules/lifecycle.mdc", ".cursor/rules/statuses.mdc", ".cursor/rules/quality.mdc", ".cursor/rules/snapshot.mdc"]
issues: []
features: []
reviewed_by: model:claude-opus-5[1m]
review_date: 2026-09-03
review_verdict: approved
related: ["[[INSTR-LIFECYCLE]]", "[[INSTR-STATUSES]]", "[[INSTR-TESTING]]", "[[INSTR-QUALITY]]", "[[INSTR-DECISIONS]]", "[[CHG-20260903-Pause-And-Scope-Rules]]", "[[CHG-20260903-Writing-Rules-And-Lengths]]"]
---

# Five instruction files are rules, reasons and links

## Summary

Five instruction files now state their rules without the history behind them: LIFECYCLE.md, STATUSES.md, TESTING.md, QUALITY.md and DECISIONS.md are between 30 and 40 percent shorter, and every rule they held is still there. Every Claude Code session imports LIFECYCLE.md and every Cursor session inlines four of the five, so the cut is paid back on every session. What left was the fleet count that retired a status, the anecdote behind a gate and the story of a check type that no longer exists; the moved text is listed below. The independent review found seven rules the first trim had dropped, restored in the review-round commit.

Two smaller changes in the same feature: the template frontmatter comments on `feature.md` and `test.md` are one line per field plus a pointer to SCHEMAS.md, so a scaffolded note no longer inherits a paragraph of rule text; and the 25 generated `.claude/skills/*/SKILL.md` bodies are the pointer to the playbook and its when-to-use bullets, with the three close-out steps in the close-out skill only and "execute exactly" replaced by "follow its checklist; where it and the repo disagree, say so and file an ISS-*".

## Counts

| File | At the review | Before the trim | After |
|---|---|---|---|
| LIFECYCLE.md | 1,343 | 1,632 (after FEAT-0024) | 966 at the trim; 996 after the review round and the ISS-0045 sentence |
| STATUSES.md | 2,772 | 2,772 | 1,663; 1,672 after the review round |
| TESTING.md | 1,608 | 1,608 | 961; 967 |
| QUALITY.md | 1,408 | 1,418 | 884; 902 |
| DECISIONS.md | 1,381 | 1,381 | 954; 973 |
| `.cursor/rules/lifecycle.mdc` | 1,374 | 1,663 | 1,005; 1,034 |
| The four always-on Cursor rules together | 5,711 | | 3,843 at the trim |

Measured with `wc -w`, frontmatter included. The commit messages for QUALITY.md and DECISIONS.md quote 895 and 860; the measured values at those commits were 884 and 954. This table is the record.

The budgets in project-os-dev REQ-0026 were 60% of each file's count on the morning of the review. LIFECYCLE.md lands at 59% of its post-FEAT-0024 size; the other four land at 60%, 60%, 63% and 69%. Each was trimmed until the next cut would remove a reason, and the requirement is reconciled to the measured numbers rather than met by cutting one.

## Moved text

Every passage removed either already lives in the decision the rule cites, or is preserved here. Nothing was deleted without a destination.

| Passage | From | Destination |
|---|---|---|
| "a local pass is not a CI pass": an unanchored `inbox/` line in `.gitignore` swallowed `docs/features/inbox/`, so a feature note, its plan and three task notes were missing from main for weeks; a stock `.claude/` line from a language scaffold swallowed the generated adapters, so `generate-adapters --check` could never pass in CI while passing locally, and every push failed for days | LIFECYCLE.md, "A local pass is not a CI pass" | this note; the rule is close-out step 8 with its reason |
| The ISS-0006 story: requirement advancement stated in four files, three corrected, `status-transition/SKILL.md` not, every repo instructing a reverted gate | STATUSES.md preamble | project-os-dev ADR-0024, Context table |
| `fixed` → `closed` was taken by 3% of issues (10 of 324) | STATUSES.md `[[issue]]`, QUALITY.md | project-os-dev ADR-0008 |
| `mitigating` and `monitoring` written once and never across 5,890 status writes; `rejected` never written; 64 values collapsed to 53 | STATUSES.md `[[risk]]`, `[[adr]]`, `[[design]]` | project-os-dev ADR-0008 |
| The retired `check` type: introduced so a human verdict could not collide with test machinery, which cost automation; 200-odd checks whose bodies named a covering automated test still blocked releases waiting for a person | STATUSES.md "`[[check]]` — retired" | this note; one sentence remains under `level: acceptance` pointing at cockpit ADR-0031 |
| The requirement `verified` status "was set on delivery or on nothing far more often than on proof" | STATUSES.md `[[requirement]]` | project-os-dev ADR-0007 |
| The PHASE-CHILDREN and PHASE-BOXES consequence paragraphs | STATUSES.md `[[phase]]` | One reason each remains in place. Removed and preserved here: "Resolve the child, or re-home it to the phase that now owns its work"; "park it under a real future phase (or PHASE-999) so the relationship, not the status word, records where the work went"; "exempting it would make the gate vacuous exactly where it matters most"; "their criteria moved to the successor" |
| "54 rows carried a hand-written RE-RUN annotation and all 54 were still ticked, because clearing the tick destroyed the only record that the check had ever passed and there was nowhere to say why" | TESTING.md, "When to invalidate" | this note; TESTING.md cites it |
| The 30-line document-form skeleton | TESTING.md, "Where the acceptance suite lives" | `docs/__templates__/acceptance-tests.md`, which is the template for it |
| The ISS-0196 paragraph: this file said the review gate applied to "any change that creates or updates a TST-*" while TESTING.md and the validator keyed it on status; under ADR-0031 the note-touched reading would have made several hundred migrated acceptance tests gate-bearing overnight | QUALITY.md, "Independent review" | this note; the rule (keyed on a status) remains |
| 206 REVIEW findings fleet-wide, 87 in one repo, none discharged in six months | QUALITY.md | project-os-dev ADR-0019 |
| The ADR-0013 experiment in full | QUALITY.md | project-os-dev ADR-0013 |
| "measured in one repo across six write paths, exactly one carried the person's own words, and only onto a checkbox" | DECISIONS.md, "Recording why" | project-os-dev ADR-0020 |
| The DECISION-RULE census of 2026-08-12 (two notes fleet-wide carrying `## Rule`, both conforming) and the landing narrative | DECISIONS.md, "A decision that states a rule" | project-os-dev ADR-0023 and TST-0004 |
| The second worked example of the `## Options` syntax (the `### N. Title` subsection form) | DECISIONS.md | Deleted, not moved: DECISIONS.md now names both forms in one sentence, and `docs/__templates__/adr.md` carries only the numbered-list form |
| "the drift travelling under its own fix"; "decided by whoever was tired" | TAXONOMY.md 113; feature-scaffold step 9; the `feature.md` template comment | TAXONOMY.md: the clause deleted, the sentence kept (`28c857a`); feature-scaffold: rewritten as "under time pressure" (`28c857a`); `feature.md`: the whole comment replaced by one line in `74753d1` |

## Review round 1

The independent review read all five files in full before and after and found seven rules the trim had dropped, none of them in the table above. All seven are restored in the review-round commit: STATUSES.md "not `ready`" in the no-verdict rule and the list of non-parked statuses on re-adoption; LIFECYCLE.md "Bases views are not canonical for agents" and the six note paths in preflight step 4; TESTING.md the below-80% half of the cadence rule; DECISIONS.md the three ADR-0011 clauses (encoded in code, no more than 90 days out, no promotion over unpaid debt); QUALITY.md the validator's five-item coverage list and the two enforcement file paths. The same review found that the bare `ADR-00NN` citations these files carry resolve to nothing in the template, whose `docs/decisions/` holds only a README, and to unrelated decisions downstream; that predates this change and is a follow-up below.

## Impact

- A session loads about half the words it did, and what it loads is rules with reasons. Whether the shorter files still steer as well is judged by the review of the first sessions that run on them.
- Every section heading other files link to is unchanged; test-pause-rule.sh and test-decision-rule.py pass against the trimmed files, and the fourteen `Allowed:` lines the validator parses are byte-identical.
- Downstream repos that edited their own copy of any of these files lose that edit at the next sync, which was true before this change.
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

The feature, requirement, tasks and test note live in project-os-dev (FEAT-0026, REQ-0026, TASK-0098 to TASK-0101, TST-0006).

## Follow-ups

- [ ] Sync to the downstream repos and re-run the generator in each.
- [ ] Read the first few sessions on the trimmed files for a rule that lost its reason in practice.
- [ ] Qualify the bare `ADR-00NN` citations in the instruction files as `project-os-dev ADR-00NN`, or ship the decisions they cite; the template's own `docs/decisions/` is empty and a downstream repo's ADR-0008 is a different decision.
