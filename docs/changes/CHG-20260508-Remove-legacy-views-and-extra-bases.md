---
type: "[[change]]"
id: CHG-20260508-Remove-legacy-views-and-extra-bases
aliases: ["CHG-20260508-Remove-legacy-views-and-extra-bases"]
title: "Remove legacy views and extra Bases"
status: merged
owner: team:docs
created: 2026-05-08
updated: 2026-05-08
source: []
commit: ""
pr: ""
impacts:
  - docs/dashboards removed
  - docs/__templates__/dashboard.md removed
  - docs/__bases__ reduced to NAVIGATION.base and CONTEXT.base
  - cockpit note-type handling no longer treats dashboard as a supported type
issues: []
features: []
related:
  - "../__bases__/NAVIGATION.base"
  - "../__bases__/CONTEXT.base"
---

# Remove legacy views and extra Bases

## Summary
Removed dashboard documentation and the dashboard template from the project-os docs system, reduced Obsidian Bases to the navigation/context pair, and renamed `NAV.base` to `NAVIGATION.base`.

## Impact
- `docs/__bases__/` now contains only `NAVIGATION.base` and `CONTEXT.base`.
- Dashboard note/template references were removed from docs, instructions, sync helpers, and cockpit type handling.
- Template sync no longer copies a dashboard phase view.

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
