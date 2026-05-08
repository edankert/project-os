---
type: "[[change]]"
id: CHG-20260508-Sync-from-project-os
title: "Sync from project-os"
status: merged
owner: team:docs
created: 2026-05-08
updated: 2026-05-08
source:
  - ../project-os
commit: ""
pr: ""
impacts:
  - Template-owned docs and tools synced from ../project-os
  - Cockpit recursive docs/reference tree updates copied into this repo
  - Snapshot timestamp refreshed for the sync
issues: []
features: []
related: []
---

# Sync from project-os

## Summary
Sync template-owned project-os files from `../project-os` so this repo carries the latest cockpit, instruction, skill, adapter, and docs template updates.

## Impact
- Runs the standard project-os sync flow from the local sibling repo.
- Updates template-owned tooling and documentation only; project-owned lifecycle docs remain protected by the sync script.
- Pulls the current `../project-os` worktree state, including its local cockpit tree-navigation changes.

## Documentation Coverage (All Types Considered)
Set each item to one of: `updated`, `new`, `not-applicable`, `deferred`.

- features: not-applicable
- requirements: not-applicable
- tasks: not-applicable
- issues: not-applicable
- tests: not-applicable
- workflows: updated
- decisions: not-applicable
- risks: not-applicable
- changes: new
- snapshot: updated

## Follow-ups
- [ ] None.
