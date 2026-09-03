---
type: instruction
id: INSTR-STATUSES
status: active
owner: group:maintainers
created: 2026-01-27
updated: 2026-09-03
tags: [instructions, statuses]
---

# Status taxonomies and transitions

**This file is the single normative source for item state**: allowed values, the gate on each terminal transition, and who writes the value. Other documents link here and none restates these rules. Reason: a rule in two files is amended in one and left wrong in the other (ISS-0006; project-os-dev ADR-0024).

## The contract at a glance

| Type | Terminal | Gate on reaching terminal | Who writes the status |
|---|---|---|---|
| `task` | `done` | linked tests `passing`; parent gates apply | agent, at close-out |
| `issue` | `fixed` | linked tests `passing` and not stale | agent, at close-out |
| `feature` | `done` | every task scope-resolved (`done`/`cancelled`/`superseded`); linked tests `passing`; every requirement naming it has resolved criteria | agent, at close-out |
| `requirement` | `implemented` | every acceptance criterion ticked-with-evidence or reconciled; never gated on tests (ADR-0007) | agent, at feature close-out |
| `phase` | `done` | every exit criterion ticked-with-evidence or reconciled (PHASE-BOXES); every note naming it in `phase:` scope-resolved (PHASE-CHILDREN) | agent |
| `test` | `passing` / `failing`, or `retired` | — | the author, and only for a manual test, which carries `last_verified:` and goes stale. A test carrying a `command:` holds no verdict (ADR-0038) |
| `test` at `level: acceptance` | `retired` | — | agent or human; it rests at `active` and the verdict is `mark:` (see `[[test]]`) |
| `risk` | `closed` | — | agent |
| `release` | `released` | release verification | agent |
| `change` | `merged` | — | agent |
| `adr` | `accepted` / `superseded` | — | human decision |

Derived, never hand-written (ADR-0009): each item's status in `SNAPSHOT.yaml`, `counters`, and `metrics.counts`. Author the status in the note; `tools/scripts/sync-snapshot.py` propagates it.

## Two things that are not statuses

- **Blocked-ness** is `depends: [ID]`; an item can be blocked while still `doing`, which a status cannot express.
- **Staleness** is computed from `last_verified:` by the validator; a typed `stale` would reintroduce the assertion problem ADR-0010 removed.

## Grandfathering

Items already violating a gate when it was promoted to error are listed by ID in `tools/GRANDFATHERED.yaml` and report as warnings; everything else errors. There is no date-based exemption, because an `updated:`-date heuristic re-arms on every edit (ISS-0007, ADR-0011).

---

If a project needs different states, update this file and the templates in `../../docs/__templates__/`. `done`/`closed`/`cancelled`/`declined` **resolve** an item's place in its parent's scope; `deferred` does not ("Deferral and re-adoption" below).

## `[[task]]`
- Allowed: `backlog`, `doing`, `done`, `deferred`, `cancelled`, `superseded`
- Typical transitions:
  - `backlog` → `doing` → `done`
  - `backlog` → `deferred` (descoped and parked; see "Deferral and re-adoption") or `cancelled` (will not be done)
  - `deferred` → `backlog` (re-adopted)
  - any → `superseded` (absorbed into a successor; link it with `superseded_by:`)

## `[[issue]]`
- Allowed: `triage`, `open`, `fixed`, `declined`, `deferred`
- Typical transitions:
  - `triage` → `open` → `fixed`
  - `fixed` → `open` (regression; git holds the history and the note records why, so there is no `reopened`)
  - `triage`/`open` → `declined` (deliberate no-action, keep the note) or `deferred` (descoped and parked)
  - `deferred` → `open` (re-adopted)
- **`fixed` is the single terminal status.** There is no `fixed` → `closed` second step; verification lives in linked `[[test]]` notes, where it carries evidence (ADR-0008).

## `[[feature]]`
- Allowed: `backlog`, `planned`, `doing`, `review`, `done`, `deferred`, `cancelled`, `superseded`
- Typical transitions:
  - `backlog` → `planned` → `doing` → `review` → `done`
  - `backlog`/`planned` → `deferred` (descoped and parked) or `cancelled` (will not be built)
  - `deferred` → `planned` (re-adopted)
  - `done` → `superseded` (replaced by a newer feature; link the successor)
- **A feature may not reach `done` while a requirement naming it in `implements:` has an unresolved acceptance criterion** (ADR-0007, validator FEATURE-REQ), unless that requirement is descoped. The task and test gates in `QUALITY.md` also apply.

## `[[phase]]`
- Allowed: `planned`, `active`, `done`, `deferred`, `superseded`
- Typical transitions:
  - `planned` → `active` → `done`
  - `planned` → `deferred`
  - any → `superseded` (scope absorbed into a successor; link it with `superseded_by:`)
- **A phase may not be `done` or `superseded` while a note naming it in `phase:` is unresolved** (validator PHASE-CHILDREN): tasks, issues, requirements, features and risks all count, and `deferred` does not resolve a child. Reason: the common failure is a child left pointing at a closed phase after its feature moved on.
- **A phase may not be `done` with an unticked exit criterion** (validator PHASE-BOXES); tick each with evidence or mark it `- [~]` with the reason it was cut. No `## Exit Criteria` section, or zero boxes, fails the same gate. Reason: a phase closed without its criteria is the assertion problem ADR-0010 removed from tests. `superseded` phases are exempt.

## `[[requirement]]`
- Allowed: `draft`, `approved`, `implemented`, `retired`, `deferred`, `cancelled`, `superseded`
- **`implemented` is terminal** (ADR-0007), gated on acceptance criteria alone and never on linked tests. There is no `verified` status; verification lives in `[[test]]` notes and the per-criterion evidence.
- Typical transitions:
  - `draft` → `approved` → `implemented`
  - `approved` → `implemented` is set at **feature close-out** (`../skills/close-out/SKILL.md`, "Requirement advancement"). A requirement left at `draft`/`approved` after its feature is terminal is a validator error (REQ-STALE); a cancelled or superseded feature supersedes or cancels its requirement instead.
  - `implemented` requires every acceptance criterion **ticked with evidence or reconciled** (validator REQ-BOXES).
  - `implemented` → `retired`
  - `draft`/`approved` → `deferred` (descoped and parked) or `cancelled`
  - `deferred` → `draft` (re-adopted)
  - any → `superseded` (replaced by a newer requirement; link the successor)
- **Ownership:** `implements:` names at most one feature (ADR-0007); two is a validator error, zero is permitted.

## `[[risk]]`
- Allowed: `open`, `closed`
- Typical transitions:
  - `open` → `closed`
- Mitigation progress is tracked in `mitigation_tasks:` and the note body, not as a status (ADR-0008).

## `[[workflow]]`
- Allowed: `draft`, `active`, `deprecated`
- Typical transitions:
  - `draft` → `active` → `deprecated`

## `[[change]]`
- Allowed: `merged`, `reverted`

## `[[adr]]`
- Allowed: `proposed`, `accepted`, `superseded`
- Typical transitions:
  - `proposed` → `accepted`
  - `accepted` → `superseded`
- A decision that is not taken is deleted or superseded, not marked `rejected`; a rejected proposal worth keeping is the alternative it lost to, and ADRs carry `alternatives:` (ADR-0008).

## `[[design]]`
- Allowed: `draft`, `proposed`, `accepted`, `implemented`, `superseded`, `cancelled`
- Typical transitions:
  - `draft` → `proposed` (offered for review)
  - `proposed` → `accepted` → `implemented`
  - `proposed` → `cancelled` (abandoned without a replacement)
  - any → `superseded` (a later design replaces it; link it with `superseded_by:`)
- Every value here already existed in the vocabulary; a new type is not a reason to add statuses (ADR-0008).
- A design records what a surface should look like and carries a rendered `asset:`; revisions are commits against the asset, not new notes. `implemented` means the design still describes the built surface; `superseded` means a newer design took over.

## `[[test]]`
- Allowed: `draft`, `active`, `ready`, `passing`, `failing`, `retired`
- Typical transitions:
  - `ready` → `passing` / `failing`
  - `failing` → `passing` (after a fix)
  - `draft` → `active` → `retired` (the acceptance lifecycle, below)
  - anything → `retired` (the subject is gone, or the test was folded into another)
- `ready` means defined but not yet executed: the state a test note is created in.
- **`passing`/`failing` belong to manual tests only.** A test with no `command:` records a verdict, carries `last_verified:` and goes stale; a stale test does not satisfy the verification gate. **A test with a `command:` records no verdict**, `last_run:` or `exit_code:` (ADR-0038): CI is the verdict. See `command:` in `SCHEMAS.md`.
- **`retired` is the only removal** (`TESTING.md`); deleting a test is forbidden by `LIFECYCLE.md`.

### `level: acceptance` — the acceptance half of the type

An acceptance test is a `[[test]]` at `level: acceptance`: the thing a person walks. Three rules apply to it and nothing else:

- **It rests at `active`, and the verdict is `mark:`, never status** (`TAXONOMY.md`). Walking one writes `mark:`, `verdict_date:` and `verdict_reason:`. Reason: the verdict rules, the review gate and the `Run` obligation are keyed on `passing` and `ready`, so they never engage for a suite of hundreds of self-re-arming rows.
- **Adding a `command:` makes it automated**: CI settles it, it leaves the manual list, and the note records no verdict (ADR-0038).
- **It carries no completeness gate of its own**: nothing is blocked by an acceptance test being `draft`.

The retired `check` type was merged into `[[test]]` so a check could be automated (project-os-cockpit ADR-0031); migrated notes keep the old `CHK-*` id as an alias.

## Deferral and re-adoption

`deferred` means out of the current parent's scope and still wanted later. It never satisfies completeness: a parent whose scope list holds a deferred item cannot reach a terminal status (validator DEFER checks). Deferring is a **descoping operation** (ADR-0005; procedure in `../skills/status-transition/SKILL.md`):

1. Move the item's ID from the parent's scope list to its `deferred:` list.
2. On the item, set `origin:` to the former parent and clear `parent:`.
3. Set `phase:` to a real future phase, else `PHASE-999` (create `docs/phases/PHASE-999-Parking-Lot.md` once; all-9s IDs are counter-exempt).
4. Mirror it in `SNAPSHOT.yaml`; deferred items are never pruned.

Re-adoption reverses it: a parent, the ID back in its scope list, the non-parked status, `origin:` kept as history. Backlog grooming reviews every parked item.

## `[[release]]`
- Allowed: `draft`, `released`, `reverted`
- Typical transitions:
  - `draft` → `released` (`draft` covers prepared and verified, not yet live; `../skills/release-verification/SKILL.md`)
  - `released` → `reverted` (rollback; keep the note and link the successor release)

## `[[plan]]`
- Allowed: `draft`, `active`, `done`, `superseded`
- A plan's status follows its feature and is advanced at close-out: `active` while building, `done` when the feature closes, `superseded` if the delivery sequence was replaced.
- Plans carry no `id:`; a `PLAN-FEAT-0012` id would resolve to `FEAT-0012` in the ID parser. They are found by `type: [[plan]]` (validator PLAN-STATE).

## `[[reference]]`
- Allowed: `active`, `deprecated`
