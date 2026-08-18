---
type: instruction
id: INSTR-TAXONOMY
status: active
owner: group:maintainers
created: 2026-01-27
updated: 2026-07-17
tags: [instructions, taxonomy]
---

# Taxonomy (allowed values)

This file defines default allowed values for common fields so multiple agents/LLMs stay consistent.

Projects may override; if you do, update templates and any automation that assumes these values.

## `owner` (all notes)
See `OWNERSHIP.md` for allowed formats and the canonical registry.

## `severity` (issues)
- `low`, `medium`, `high`, `critical`

## `priority` (requirements)
- `low`, `medium`, `high`

## `order` (phases)
Positive integer sort order for roadmap sequencing.

## `effort` (tasks)
- `XS`, `S`, `M`, `L`, `XL`

## `likelihood` (risks)
- `low`, `medium`, `high`

## `impact` (risks)
- `low`, `medium`, `high`

## `component` (issues)
Project-defined free text label, but keep it stable. Examples:
- `docs`, `build`, `tests`, `tooling`, `runtime`, `ui`, `api`

## `kind` (tests)
- `manual`, `automated`

## `level` (tests)
- `unit`, `integration`, `system`, `e2e`, `acceptance`
- **`acceptance` is the discriminator of the merged type (ADR-0031)**: a test at this level is the thing a person walks — it rests at `status: active`, its verdict is `mark:`, and it carries the acceptance fields below. Everything else on the scale is executable. The field has always been here; since ADR-0031 it carries the distinction the retired `check` type used to.
- A test moves along the scale rather than between types. **Adding a `command:` to an `acceptance` test is how a walk becomes automated**, and a `passing` test named in another's `covered_by:` settles it (see `TESTING.md` tiers and `../skills/release-verification/SKILL.md`).

## `scope` (tests)
- `feature`, `system`

## `mark` (tests at `level: acceptance`)

The verdict on an acceptance test — one character, [Minimal's alternate checkbox vocabulary](https://minimal.guide/checklists), read exactly as the acceptance suite reads it:

| `mark` | means | blocks a release |
|---|---|---|
| `" "` | nobody has walked it | yes |
| `x` | walked and passed | no |
| `/` | partial pass — some clauses hold, some do not | no |
| `-` | canceled: will not be walked, and is not holding the release | no |
| `!` | walked and failed, with the failure tracked | yes |
| `?` | walked and not understood — the check itself is unclear | yes |

`/`, `-`, `!` and `?` are **refused without a `verdict_reason:`**. The mark and its justification are one write, so an acceptance test cannot leave the gate without saying why.

**`mark:` is not `status:`.** An acceptance test's lifecycle is `status:` — it rests at `active`, and `retired` is terminal; its verdict is `mark:`. Ticking never touches `status:`, and that is precisely what keeps it outside the runner-only rule, the independent-review gate and the `Run` obligation now that it shares a type with executable tests — see `STATUSES.md` `[[test]]`. The protection is the same one the `check` type provided, held by status rather than by type.

## `automation` (tests at `level: acceptance`)
- `full`, `partial`, `manual`
- What already covers this check mechanically. `covered_by:` names the `TST-*` (or test module) doing the covering; a `full` check with no `covered_by:` is a claim with nothing behind it.

## `burden` (tests at `level: acceptance`)
Optional, project-defined free text naming what a walker must have to hand — `App`, `Trainer`, `Strava`, `hardware`. Its purpose is to avoid making somebody set the same thing up twice, so keep the labels stable and few.

## `check` versus `level: acceptance` on a test

Both exist and they are not the same thing. `level: acceptance` on a `[[test]]` is a **specification** — usually one automated module, statuses written by the runner. A `[[check]]` is one line of a **manual walk** with a persistent human verdict. `TESTING.md` has always said the two coexist; the type boundary is what stops the release gate, the runner-status rule and the independent-review gate from being applied to the wrong population.
