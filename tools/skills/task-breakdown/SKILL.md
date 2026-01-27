---
type: skill
id: SKILL-TASK-BREAKDOWN
status: active
owner: group:maintainers
created: 2026-01-27
updated: 2026-01-27
tags: [skills, tasks]
---

# Skill: Task breakdown

## When to use
- You have a `FEAT-*` (and optionally `REQ-*`) but tasks are missing or too large.

## Inputs
- Feature note + requirements + any linked issues.

## Outputs
- `../../../SNAPSHOT.yaml` updated (`items.tasks`, feature `tasks` list, `focus` if applicable).
- New/updated task notes under `../../../docs/features/<slug>/plan/tasks/`.

## Checklist
1. Read the feature goal + acceptance and decide the smallest set of deliverable tasks.
2. For each task:
   - allocate a `TASK-####`
   - define `title`, `status`, `effort`, `parent`, `depends`, `blocks`
3. Update `../../../SNAPSHOT.yaml`:
   - add `items.tasks.<TASK-####>`
   - append the task ID to `items.features.<FEAT-####>.tasks`
4. Create each task note from `../../../docs/__templates__/task.md` with a measurable DoD.
5. If tasks expose unknowns, file an `ISS-*` rather than inflating tasks.
