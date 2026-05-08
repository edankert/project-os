---
type: skill
id: SKILL-PHASE-PLANNING
status: active
owner: group:maintainers
created: 2026-05-05
updated: 2026-05-08
tags: [skills, phases, planning]
---

# Skill: Phase planning

## When to use
- A project adopts phase-gated development.
- A new milestone needs durable scope, linked work, or exit criteria.
- Existing numeric phase values should be migrated to `PHASE-*` notes.

## Inputs
- Roadmap or milestone description.
- Existing feature, requirement, task, and issue IDs.
- `../../../SNAPSHOT.yaml`.
- `../../../docs/PHASES.md`.

## Outputs
- New or updated `../../../docs/phases/PHASE-###-Short-Name.md` notes.
- `../../../SNAPSHOT.yaml` updated (`counters.PHASE`, `items.phases`, `focus.phase` when active).
- Phase links added to related notes and snapshot items.

## Checklist
1. Decide whether a first-class phase note is needed:
   - Use a `PHASE-*` note when the milestone has scope, exit criteria, or linked work.
   - A simple integer phase in `phase:` is acceptable only for lightweight projects or migration.
2. Allocate the next `PHASE-###` from `../../../SNAPSHOT.yaml -> counters.PHASE`.
3. Create the phase note from `../../../docs/__templates__/phase.md`.
4. Populate:
   - `order`
   - `goal`
   - scope and out-of-scope sections
   - exit criteria
5. Update `../../../SNAPSHOT.yaml`:
   - add `items.phases.<PHASE-###>` with `file`, `title`, `status`, `order`, and `goal`
   - increment `counters.PHASE`
   - set `focus.phase` if this is the active milestone
   - update `metrics.counts.phases_total` and `metrics.counts.phases_done`
6. Update related notes/items:
   - set `phase: ["[[PHASE-###-Short-Name]]"]` in note frontmatter where applicable
   - set `phase: PHASE-###` or the matching phase note link in snapshot item entries
   - rely on backlinks from those related notes rather than maintaining child lists on the phase note
7. Run `../snapshot-sync/SKILL.md` to verify phase links and metrics.
