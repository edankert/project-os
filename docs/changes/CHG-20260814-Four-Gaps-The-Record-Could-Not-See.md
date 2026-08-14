---
type: "[[change]]"
id: CHG-20260814-Four-Gaps-The-Record-Could-Not-See
title: "Four gaps the record could not see"
status: merged
owner: user:edwin
created: 2026-08-14
updated: 2026-08-14
source: ["project-os-cockpit ISS-0155, ISS-0163, ISS-0124, ISS-0147 — four downstream issues that could not be fixed downstream because tools/scripts/validate-docs.py is template-owned"]
commit: ""
pr: ""
impacts: ["what TEST-FIELDS demands of a never-run manual test", "a new TEST-ENTRYPOINT warning", "a new STATUS-TYPE warning", "docs/workflows/ no longer ships three stubs"]
issues: []
features: []
related: ["[[ADR-0010]]", "[[ADR-0011]]"]
---

# Four gaps the record could not see

## Summary

Four fixes batched into one upstream visit because they share a cause: **a downstream repo cannot fix its own validator.** `tools/scripts/validate-docs.py` is template-owned, and project-os-cockpit's suite asserts its bundled copy is verbatim — so each of these had been filed downstream and could only be closed here.

1. **A never-run manual test can exist again.** `TEST-FIELDS` demanded `last_verified:` from every manual test including one whose status is `ready` — the state `STATUSES.md` calls *"defined but not yet executed"*. The gate required the author to record a run that did not happen.
2. **`TEST-ENTRYPOINT`, new.** A test the corpus treats as automated, at a runner status, with no `command:` — nothing can re-run it, so its status cannot be refreshed by machine.
3. **`STATUS-TYPE`, new.** A note type appearing in `docs/` with no entry in any status table. The tables were guarded against each other and never against the corpus.
4. **`WF-0001`, `WF-0002`, `WF-0003` are no longer shipped.**

## 1 is a restoration, and how it was lost is the finding

The `ready` exemption was added on **2026-08-01 by `5a487ad`** and removed by **`59bd47c`** three weeks later — not by decision, but by a whole-file overwrite from a downstream copy that predated it. `5a487ad`'s own commit message had predicted it:

> *"Two fixes that had been made downstream and never pushed up, so every sync reported them as local divergence and they were one `--force` away from being lost."*

They were then lost. The cost was paid downstream on 2026-08-13, where authoring a genuinely never-run manual test required typing a verification date for a walk nobody had performed, plus a paragraph of prose explaining that the field did not mean what the field means.

Restored with that history in the code comment, so the next overwrite has to read it first.

## 2 and 3 are warnings with room to land

Both follow [[ADR-0011]]'s shape rather than erroring on day one. Measured across all twelve fleet repos with the new checks:

| repo | TEST-ENTRYPOINT | STATUS-TYPE |
|---|---|---|
| yourtrainer-mcp | 15 | — |
| your-sudoku | 12 | — |
| your-health | 11 | — |
| obsidian-supernote-sync | 4 | 1 |
| your-trainer | 1 | 2 |
| your-applications.com | — | 1 |
| **project-os-cockpit** | **0** | **0** |
| the other five | — | — |

**43 findings for TEST-ENTRYPOINT.** Erroring would have failed five repos on the day this shipped for a rule none of them knew existed — the mistake project-os-cockpit's ISS-0057 records. project-os-cockpit reads 0 because it fixed its own 22 notes the day before; that is the evidence the check is satisfiable, not that it is inert.

Every repo's overall verdict is unchanged by this commit. `your-trainer` still reports one error and it is `DEFER-RETENTION`, present identically with the unmodified validator.

## 3 had to walk the files, and its first version could not see its own subjects

`STATUS-TYPE` was written first over `note_index` — and reported nothing. That index is keyed by IDs matching `ID_PREFIXES` (`ADR`, `DES`, `FEAT`, `ISS`, `PHASE`, `REL`, `REQ`, `RISK`, `TASK`, `TST`, `WF`), and the notes this check exists for carry none of them: `ARCHITECTURE.md` is `ARCH`, the glossary is `GLOSSARY`, a signpost is `DOCS-README`. **The types with no status table are exactly the types with no ID prefix, for the same reason: nobody tabulated them.** It walks `docs/` directly now.

Two tables were added from measurement rather than intuition — `reference` (206 `active` fleet-wide) and `glossary` (10 `active`). `glossary` sat in the status-free set for about ten minutes until the check's first run reported project-os's own `GLOSSARY.md` carrying a status. `dashboard` was dropped from that set: it exists only as a template, which the walk excludes, so listing it would be a rule about a note that does not exist.

`STATUS_FREE_TYPES` and `MANUAL_DECLARATION_KEYS` were both caught by the validator's own unregistered-collection guard on the day they were added, and are registered in `_NON_STATUS_COLLECTIONS`. That guard is what ISS-0012 and ISS-0013 paid for.

## 4 removes 3 notes, not 8

The three shipped stubs: **24 copies across 8 repos, every one `status: draft`, every one `updated: 2026-01-29`**, byte-identical to the template's — six and a half months, not one edit anywhere. Each named its real home in its own frontmatter (`tools/skills/project-derive/SKILL.md`, `tools/scripts/sync-project-os.sh`, `tools/instructions/HANDOFF.md`).

**Eight project-authored workflow notes across three repos were not touched**, and `docs/workflows/README.md` now says why: `tools/` is template-owned and a sync overwrites it, so *"how you build and run this app"* has nowhere else to live. The counter stays at `WF: 3` — counters are a high-water mark and never fall.

## Documentation Coverage (All Types Considered)

- features: not-applicable
- requirements: not-applicable
- tasks: not-applicable
- issues: not-applicable (the four live downstream, in project-os-cockpit)
- tests: not-applicable
- workflows: **removed** — WF-0001..0003
- decisions: not-applicable — [[ADR-0010]] and [[ADR-0011]] already decided the shapes used
- risks: not-applicable
- changes: new
- snapshot: updated (WF counter comment)

## Evidence

Each check proved against a synthetic corpus, both directions:

| probe | result |
|---|---|
| `ready` manual test, no `last_verified` | **no error** (was an error) |
| same note flipped to `passing` | errors, unchanged |
| `passing` test, `kind: automated`, no `command:` | `TEST-ENTRYPOINT` fires |
| a `telemetry` type with no ID prefix | `STATUS-TYPE` fires |
| a `glossary` note acquiring `status: draft` | `STATUS-TYPE` fires |
| project-os itself, and 11 fleet repos | verdicts unchanged |

## Follow-ups

- [ ] Downstream repos carrying `WF-0001..0003` keep them until each chooses to remove its copies; the template no longer supplies them.
- [ ] The 43 `TEST-ENTRYPOINT` findings are each repo's to answer — a `command:`, or `kind: manual`.
