---
type: skill
id: SKILL-ISSUE-INTAKE
status: active
owner: group:maintainers
created: 2026-01-27
updated: 2026-01-27
tags: [skills, issues]
---

# Skill: Issue intake

## When to use
- A prompt reports a bug, mismatch, broken workflow, unclear documentation, or unexpected behavior.

## Inputs
- User prompt, repro steps/logs, and any affected repo paths.

## Outputs
- `../../../SNAPSHOT.yaml` updated (`items.issues` + links to affected features/tasks).
- A new/updated `../../../docs/issues/ISS-####-Short-Description.md` note.
- Optional: new `TASK-*` entries/notes if work can be immediately planned.

## Checklist
1. Assign the next `ISS-####` (use `../../../SNAPSHOT.yaml -> counters.ISS`).
2. Update `../../../SNAPSHOT.yaml`:
   - add `items.issues.<ISS-####>` with `title`, `status`, `severity`, `component`, `file`
   - link to impacted `features` and/or planned `tasks`
   - set `focus.issue` if this is the current work
3. Create/update the issue note from `../../../docs/__templates__/issue.md`:
   - include repro, expected vs actual, evidence paths
4. If the fix requires implementation:
   - ensure there is a parent `FEAT-*` (create if needed)
   - create one or more `TASK-*` under the feature and link them in snapshot + notes
5. Run a quick risk scan (use `../risk-scan/SKILL.md`) if the issue implies contract/dependency changes.
6. If verification is needed, create a `TST-*` note (use `../test-authoring/SKILL.md`) and link it from the issue/task/requirement as appropriate.
