---
type: "[[change]]"
id: CHG-20260717-Manifest-Sync-And-Fleet-Validation
aliases: ["CHG-20260717-Manifest-Sync-And-Fleet-Validation"]
title: "Manifest-driven sync with baseline divergence detection; fleet-wide validator"
status: merged
owner: user:edwin
created: 2026-07-17
updated: 2026-07-17
source:
  - ../project-os-dev/docs/features/template-completeness/plan/tasks/TASK-0044-Sync-Manifest-Fleet-Validator.md
commit: ""
pr: ""
impacts:
  - "tools/sync/MANIFEST.yaml"
  - "tools/scripts/sync-project-os.py"
  - "tools/scripts/sync-project-os.sh"
  - "tools/scripts/validate-fleet.sh"
  - "tools/instructions/SYNCING.md"
issues: []
features: []
related: []
---

# Manifest Sync + Fleet Validation

## Summary

The 2026-07-05 rollout showed the rsync-based sync clobbers repos that keep real content in nominally template-owned paths; the safe recipe (compare each file against the template baseline commit) had to be improvised by hand, per repo. This change mechanizes it. Program tracking: project-os-dev FEAT-0010 / TASK-0044.

## Impact

- **`tools/sync/MANIFEST.yaml`**: per-path ownership (`template`/`merge`/`seed`/`project`/`generated`), most specific path wins; known clobber hazards (`docs/PHASES.md`, `docs/phases/`, `SCHEMAS.md`) are `merge`-owned instead of tribal knowledge.
- **`sync-project-os.py`** (`sync-project-os.sh` is now a thin wrapper, same CLI plus `--force`/`--baseline`): each template-owned file is compared against the baseline commit recorded in `.project-os-sync` — clean fast-forwards are overwritten, locally modified files are skipped and reported for hand-merge, seeds copy once, upstream-deleted files are reported (never deleted). Post-sync it reinstalls git hooks and regenerates adapter artifacts. Verified against project-os-dev in dry-run: with `--baseline 77b4d5e`, 11 previously "diverged" files resolve to clean fast-forwards.
- **`validate-fleet.sh`**: runs the validator across every SNAPSHOT-bearing repo under a root, printing a per-repo errors/warnings/waivers table (first run: 5 of 10 repos fail under the new stricter checks — expected pre-rollout drift, see the consistency-debt CHG).
- SYNCING.md rewritten around the manifest + baseline model, with a Fleet check section.

## Documentation Coverage (All Types Considered)

- features: not-applicable (tracked in project-os-dev FEAT-0010)
- requirements: not-applicable
- tasks: not-applicable (project-os-dev TASK-0044)
- issues: not-applicable
- tests: not-applicable
- workflows: not-applicable (WF-0002 entrypoint unchanged: sync-project-os.sh)
- decisions: not-applicable
- risks: not-applicable
- changes: new
- snapshot: not-applicable (template placeholder)

## Follow-ups

- [ ] First manifest-based sync per downstream repo should pass `--baseline <last-synced-template-sha>` so fast-forwards resolve mechanically.
