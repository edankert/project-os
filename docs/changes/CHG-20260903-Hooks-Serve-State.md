---
type: "[[change]]"
id: CHG-20260903-Hooks-Serve-State
title: "The hint states where the work stands, the Stop hook names two actions and blocks for the first time, and the gate lets files outside project-os through"
status: merged
owner: user:edwin
created: 2026-09-03
updated: 2026-09-03
source: ["project-os-dev FEAT-0027, TASK-0102 to TASK-0105, ISS-0003", "project-os-dev docs/reference/Prompting-Guide-Review-2026-09-03.md, findings 2.2, 2.4, 3.1, 3.2, 7.3"]
commit: "80a4a85, 7b6890f, 3e5c1b3, f6ac538, 8d35297"
pr: ""
impacts: ["tools/adapters/claude-code/hooks/close-out-check.sh", "tools/adapters/claude-code/hooks/model-routing-hint.sh", "tools/adapters/claude-code/hooks/document-first-gate.sh", "tools/instructions/HOOKS.md", "tools/adapters/claude-code/ADAPTER.md", "tools/scripts/generate-adapters.py", "tools/scripts/test-hooks.sh", "docs/__templates__/issue.md", "tools/skills/ad-hoc-intake/SKILL.md", "tools/skills/issue-intake/SKILL.md", ".claude/agents/planner.md"]
issues: []
features: []
related: ["[[INSTR-HOOKS]]", "[[CHG-20260903-Pause-And-Scope-Rules]]", "[[CHG-20260718-Cross-Repo-Hook-Root]]"]
reviewed_by: model:claude-opus-5[1m]
review_date: 2026-09-03
review_verdict: changes-requested
---

# The hooks serve state and name actions

## Summary

Three Claude Code hooks change what they print, and one of them starts working. The per-prompt hint (HC-008) stated on every prompt that preflight should be delegated to the planner subagent, and ended every variant with the review sentence, on questions included. It now says where the work stands: the focus item, its status and its phase. It says who writes the note for new work: a single issue or task in the main loop, a multi-item scaffold or an ambiguous ask through the planner, with the user's prompt verbatim and one sentence on what the result enables, while the lead keeps reading the code. The documentation requirement is unchanged and is restated in the same sentence. The reviewer is named only in review states.

The Stop hook (HC-006) blocked with "acknowledge to continue", which is not an action. It now names two: set the status and clear focus if the work is complete, or write the handoff into the task note and stop. Writing the harness showed the hook had never blocked on focus at all: it extracted the focus values through `echo "" | jq`, which runs no filter on an empty input. The extraction is fixed, so downstream repos will see this hook block for the first time after their next sync.

The document-first gate (HC-001) denied any write outside every project-os repo whenever the session repo's focus was empty, a scratchpad included, and the workaround was the shell. It now falls back to the session repo only for a relative path or a path under that repo.

The issue template carries an "As reported" callout under Problem for the reporter's own words, in the shape DECISIONS.md uses for a decision, and the planner prompt says to expect the verbatim prompt and the reason.

## Impact

- **The Stop hook now blocks when focus is left set.** Every downstream repo inherits this at its next sync. The block names what to do, and the loop guard lets the second stop through, so a session that writes its handoff can still end.
- The hint's prefix changes from "project-os delegation hint:" to "project-os:". Nothing parses it.
- `tools/scripts/test-hooks.sh` is new: 25 assertions over the three hooks against fixture snapshots under a tempdir. project-os-dev TST-0007 runs it; it also carries the four-path table from ISS-0003.
- ADAPTER.md's routing table says preflight runs in the main loop for a single issue or task and in the planner for a multi-item scaffold or an ambiguous ask, in the same commit as the hint, so the two do not disagree.
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

The feature, its four tasks, the issue and the test note live in project-os-dev (FEAT-0027, TASK-0102 to TASK-0105, ISS-0003, TST-0007).

## Follow-ups

- [ ] Sync to the downstream repos and re-run the generator in each; expect the Stop hook to start blocking there.
- [ ] Read the first sessions on the new hint for a case where the main loop should have delegated and did not, or the reverse.
