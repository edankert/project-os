---
type: instruction
id: INSTR-LIFECYCLE
status: active
owner: group:maintainers
created: 2026-01-27
updated: 2026-09-03
tags: [instructions, lifecycle]
---

# Lifecycle rules (LLM-maintained documentation system)

An LLM maintains this system across the lifecycle of work: intake, plan, implement, verify, close. Each rule is stated once, with its reason and a link; the history lives in the linked decision (project-os-dev REQ-0026).

## Source of truth
- `../../SNAPSHOT.yaml` is the canonical, machine-readable active context for agents. Notes under `../../docs/` are the durable human record, and their frontmatter must agree with it.

## Test storage (hybrid)
- A feature-scoped test lives at `docs/features/<feature-slug>/plan/tests/TST-####-*.md`; a system-wide one at `docs/tests/TST-####-*.md`.

## Statuses
- Allowed statuses and transitions are stated once, in `STATUSES.md`.

## The inbox
- `inbox/` at the repo root is gitignored staging for external material nobody has decided about. An item there is an unmade decision, not a record; triage it with `../skills/inbox-triage/SKILL.md` whenever the directory is not empty. Reason: `docs/` is the curated record the validator walks.

## Preflight (must happen before code changes)
When a prompt implies work (bugfix, feature, refactor, behaviour change):
1. **Classify** it as issue, feature, requirement, risk, or chore/docs-only, and run the spec-ambiguity check in `../skills/issue-intake/SKILL.md` step 1 before allocating any ID.
2. **Orchestration check**: an assigned task must be in the snapshot at a status that allows work (`backlog`, `doing`); otherwise pick work from `focus` and item statuses.
3. **Update `../../SNAPSHOT.yaml` first**: allocate IDs, create or update `items.*` entries and relationships, set `focus`.
4. **Create or update the notes** from `../../docs/__templates__/`: phase, issue, requirement, feature with its `plan/PLAN.md`, task (must have `parent`), risk.
5. **Impact analysis**: run `../skills/impact-analysis/SKILL.md` for a new or materially changed requirement, and for work touching a constrained area. A conflict is the user's decision; present the options and continue with what does not depend on them ("When to pause for the user" below).
6. Keep note frontmatter consistent with the snapshot.

A prompt that is only a question needs no preflight.

## Phase alignment (optional gating)
When the project uses phases (`../../docs/PHASES.md`):
1. **Verify phase**: read the task's or feature's `phase` before starting, and what that `PHASE-*` note bounds.
2. **No phase bleeding**: do not build a later phase's work inside an earlier phase's task.
3. **Flag scope concerns**: a task that needs a future-phase dependency is a scope change the user decides ("When to pause for the user" below).
4. Keep `focus.phase` on the current milestone.

## Mandatory Automated Documentation
- **No orphaned code**: every functional code change (feature, bug fix, behaviour-altering refactor, API change, dependency update) has a task under `docs/features/<slug>/plan/tasks/`. Typo, comment, formatting and documentation-only changes are exempt.
- **Notes are the authored source of state** (ADR-0009): write a status once, in the note. `tools/scripts/sync-snapshot.py` propagates statuses, `counters` and `metrics.counts` into the snapshot at pre-commit; CI checks it with `--check`. Never hand-copy a status into the snapshot.
- **Counters rise on their own**: allocating an ID means creating a note, and a deleted note never frees its number.
- **Membership is still yours**: which items the snapshot carries, and their `goal:` and `note:` prose, are curation the script leaves alone.

## Execution (implementation phase)
- Start code changes only once the planning artifacts exist, and keep `focus` on what is actually being worked.

### When to pause for the user
Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. Everything else is your judgment call. First do everything that does not depend on the answer; then put the question at the end of a turn that also delivers that progress. Reason: an early question hands the task back unfinished. Every other file that names a pause links here and says only which decision the user owns (project-os-dev ADR-0024).

### Scope of a change
A bug, a cleanup or a missing abstraction the task did not ask for is an `ISS-*` at `triage` or a follow-up in your summary, not a change in this diff, unless the requested behaviour cannot work without it. Reason: the document-first gate blocks an edit with no focus item, and widening the task is the bypass. When the wording admits two readings, implement the one it most directly supports and state the assumption in the task note; ask only when the readings lead to materially different work.

## Close-out (must happen after work)
1. Set the note status: task `done`, issue `fixed` (its only terminal status, ADR-0008), requirement `implemented`, feature `done`.
2. Update the snapshot: statuses, relationships, focus, metrics.
3. Add a change note, `docs/changes/CHG-YYYYMMDD-Short-Description.md`, when behaviour, paths or contracts change.
4. Add or update a `RISK-*` for a new hazard: a dependency, an env var, a contract.
5. Never delete a completed note; status and links preserve history.
6. Apply the verification gate in `QUALITY.md`: a terminal status needs its required `[[test]]` notes `passing`.
7. Run `bash tools/scripts/validate-docs.sh` and fix what it reports.
8. Before pushing, run `bash tools/scripts/validate-docs.sh --as-committed`. Reason: local checks read the working tree and CI reads the commit, so an ignored or unstaged file passes here and is absent there.
9. After pushing, confirm the run went green (`gh run list --limit 1`). A change is not landed until you have seen that.
10. If the work touched a `TST-*` or `CHG-*` note, or moves a requirement to `implemented` or a feature to `done`, run `../skills/independent-review/SKILL.md`.

## Snapshot retention (active + recent)
- Keep the snapshot to active and recent items; the notes are the archive (`SNAPSHOT.md`).

## Risk scan triggers (create/update a `RISK-*`)
- A new external dependency or version constraint; a new required env var or configuration surface; a directory layout or artifact path change; a runtime increase or new long-running step; a security, credential or licence exposure.
