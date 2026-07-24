---
type: "[[change]]"
id: CHG-20260724-Unregistered-Note-Checks
aliases: ["CHG-20260724-Unregistered-Note-Checks"]
title: "Validator reaches notes the snapshot cannot see: NOTE-DUP-ID (error) and NOTE-STATUS (warning)"
status: merged
owner: user:edwin
created: 2026-07-24
updated: 2026-07-24
source: []
commit: ""
pr: ""
impacts:
  - "tools/scripts/validate-docs.py"
issues: []
features: []
related: ["[[CHG-20260717-Manifest-Sync-And-Fleet-Validation]]"]
reviewed_by: ""
review_date: ""
review_verdict: ""
---

# Checks for notes the snapshot cannot see

## Summary

Every existing check resolves an item's status *through* `SNAPSHOT.yaml`. Snapshot retention is deliberately active-and-recent — completed work is pruned and the note becomes the archive — so a large share of notes in a mature repo are unregistered, and **none of them were ever inspected**. Drift accumulated there permanently invisible.

Two real defects were found by hand in a downstream repo and traced to exactly this gap: fifteen requirement IDs each claimed by two different notes, and thirty-seven requirements carrying a `status:` value that is not in the taxonomy — both of which had survived an earlier repo-wide cleanup precisely because that cleanup worked from the validator's error list.

`validate_unregistered_notes()` now walks every note and reports what used to hide there.

## What is and is not checked

Being unregistered is **not** itself reported. That would fight the retention policy, which intends pruning. What is reported is the drift:

- **`NOTE-DUP-ID` (error).** Two or more notes declaring the same ID. `build_note_index` keeps only the first claimant (`setdefault`), so rival notes are silently unreachable — bare-ID links and lookups resolve to whichever sorts first. This is unambiguous corruption of the ID space, so it fails the build.
- **`NOTE-STATUS` (warning).** A note whose frontmatter `status:` is outside the taxonomy for its type, checked only for notes absent from the snapshot (registered ones are already covered by `STATUS-VALUE` and the `ITEM-STATUS` drift check, so nothing is double-reported).

`NOTE-STATUS` is a warning on purpose. It reaches notes never validated before and therefore surfaces years of accumulated legacy vocabulary at once — 173 across the fleet at introduction (task `superseded` ×71, issue `done` ×45, issue `pending` ×30, test `active` ×8, phase `superseded` ×1, plus 18 elsewhere). Failing those builds outright would punish repos for drift the tooling itself allowed. It should graduate to an error once the fleet is migrated.

## Claiming an ID is stricter than indexing it

The first implementation produced false positives, worth recording because the cause is subtle. `extract_ids` scans for ID substrings, and composite IDs legitimately embed another note's ID: a plan is `PLAN-FEAT-0006`, and a change note may be `CHG-20260525-FEAT-0009-Chrome-Polish`. Both were being counted as rival claims on `FEAT-0006` / `FEAT-0009`, which would have flagged 44 healthy notes across the fleet.

A note now *claims* an ID only when its frontmatter `id` is exactly that ID, or its filename begins with it. The loose substring behaviour of the index itself is unchanged — other checks depend on it for link resolution.

## Fleet impact at introduction

Six of ten repos are entirely clean. `NOTE-DUP-ID` fires in two (your-trainer 8: ADR-0001, ISS-0003..0008, REL-0007; your-applications.com 2: TASK-0014, TASK-0173) — all genuine collisions between unrelated notes, e.g. `ISS-0003` is simultaneously "HrmStatusMismatch" and "RiderSelectionAddButton". Those must be renumbered for the affected repos to go green.

## Documentation Coverage (All Types Considered)

- features: not-applicable
- requirements: not-applicable
- tasks: not-applicable
- issues: not-applicable
- tests: not-applicable (no test harness for the validator; verified by running it against all ten fleet repos before and after, and by confirming the false-positive class disappeared)
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable
- changes: new
- snapshot: not-applicable (template placeholder)

## Follow-ups

- [ ] Renumber the 10 `NOTE-DUP-ID` collisions in your-trainer and your-applications.com; until then those two repos fail validation.
- [ ] Migrate the 173 `NOTE-STATUS` legacy values, then graduate the check from warning to error.
- [ ] `HOOKS.md` HC-007 describes the validator's checks in prose; consider listing the check codes there so the contract stays discoverable.
