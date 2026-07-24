---
type: "[[change]]"
id: CHG-20260724-Sync-Force-Merge-Guard
aliases: ["CHG-20260724-Sync-Force-Merge-Guard"]
title: "sync --force no longer overwrites merge-owned files — it was destroying real project content"
status: merged
owner: user:edwin
created: 2026-07-24
updated: 2026-07-24
source: []
commit: ""
pr: ""
impacts:
  - "tools/scripts/sync-project-os.py"
issues: []
features: []
related: ["[[CHG-20260717-Manifest-Sync-And-Fleet-Validation]]"]
reviewed_by: ""
review_date: ""
review_verdict: ""
---

# sync `--force` merge-ownership guard

## Summary

`sync-project-os.py --force` overwrote **every** locally diverged template-owned file, including `merge`-owned paths. That ownership class exists precisely because real project content lives there — a repo's own `docs/PHASES.md`, `ROADMAP.md`, and `docs/__templates__/SCHEMAS.md` — and `MANIFEST.yaml` documents it as "never auto-overwritten when diverged". The force branch ran before the ownership check, so the documented protection did not apply.

This was found the hard way during a fleet-wide sync: the forced sync replaced a downstream repo's real 15-phase registry (MVP, Premium & Release, Localization, Accessibility…) with the template's placeholder table (Foundation, Core Engine, Product…). The loss was caught and restored from git, and every subsequent repo in that rollout needed a manual `git checkout --` of the merge-owned paths immediately after syncing.

Note the `--force` help text already read "Overwrite locally diverged **template-owned** files" — the contract was right, the implementation didn't match it.

## Impact

- `--force` now applies to `template`-owned paths only. `merge`-owned paths are always left for a hand-merge, reported under the existing "Expected-divergence" heading, which now states explicitly that `--force` does not touch them.
- No escape hatch was added: a `merge` path is by definition one a human must reconcile. If you truly want the upstream version, copy the file by hand.
- Verified against a real downstream repo: a forced sync now leaves `docs/PHASES.md` byte-identical and reports it as pending hand-merge.

## Documentation Coverage (All Types Considered)

- features: not-applicable
- requirements: not-applicable
- tasks: not-applicable
- issues: not-applicable
- tests: not-applicable (no test harness for the sync script; verified by a live forced sync against a downstream repo, asserting the checksum was unchanged)
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable (removes a data-loss hazard; adds none)
- changes: new
- snapshot: not-applicable (template placeholder)

## Follow-ups

- [ ] The fleet rollout of 2026-07-24 left every synced repo's merge-owned files restored-but-stale; they still need a hand-merge against the current template (notably `SCHEMAS.md`, which carries the acceptance-criteria-as-verification-record and deferral-provenance schema that REQ-BOXES warnings cite).
- [ ] Consider a regression test for the sync script — this class of bug is silent and destructive, and there is currently no automated coverage at all.
