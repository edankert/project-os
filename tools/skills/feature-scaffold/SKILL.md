---
type: skill
id: SKILL-FEATURE-SCAFFOLD
status: active
owner: group:maintainers
created: 2026-01-27
updated: 2026-01-27
tags: [skills, features]
---

# Skill: Feature scaffold

## When to use
- A prompt requests a new capability or significant enhancement (not just a bugfix).

## Inputs
- Feature request text, constraints, acceptance expectations, affected workflows/areas.

## Outputs
- `../../../SNAPSHOT.yaml` updated (`items.requirements`, `items.features`, `items.tasks`, `focus`).
- A new feature folder under `../../../docs/features/<slug>/` containing:
  - `FEAT-####-Short-Description.md`
  - `plan/PLAN.md`
  - `plan/tasks/TASK-####-*.md` (initial breakdown)

## Checklist
1. Decide whether new `REQ-*` notes are needed (acceptance criteria that should outlive tasks).
2. Allocate IDs (use `../../../SNAPSHOT.yaml -> counters`).
3. Update `../../../SNAPSHOT.yaml`:
   - create `items.requirements` (if needed) and link them to the feature
   - create `items.features.<FEAT-####>` with `goal`, `requirements`, `tasks`, `workflows`
   - create initial `items.tasks` entries with `parent: FEAT-####`
   - set `focus.feature` and `focus.task` (if starting immediately)
4. Create the feature notes from templates:
   - requirement note(s): `../../../docs/__templates__/requirement.md`
   - feature note: `../../../docs/__templates__/feature.md`
   - plan: concise sequence for delivery
   - tasks: each with clear DoD
5. Run a risk scan if this feature introduces new dependencies/contracts.
6. If the feature requires verification, create `TST-*` notes (use `../test-authoring/SKILL.md`) and link them from the feature/requirements/tasks.
