---
type: "[[change]]"
id: CHG-20260508-merge-upstream-functionality
aliases: ["CHG-20260508-merge-upstream-functionality"]
title: "Merge upstream project-os functionality"
status: merged
owner: unassigned
created: 2026-05-08
updated: 2026-05-08
source:
  - ../project-os
commit: ""
pr: ""
impacts:
  - "tools/cockpit"
  - "tools/agents"
  - "tools/adapters/codex"
  - "docs/reference"
  - "docs/phases"
issues: []
features: []
related:
  - tools/cockpit/README.md
  - tools/scripts/sync-project-os.sh
---

# Merge Upstream Project-os Functionality

## Summary
Merged selected upstream functionality from `../project-os` into this repo while preserving local release tracking, Claude/Cursor/generic adapters, Obsidian cockpit layout, and upward-linking schema conventions.

## Impact
- Cockpit now includes upstream reference-note support, image asset rendering, project support pages, and `/index/references`.
- Codex/agent startup support now includes `AGENTS.md`, `LLM_BRIEF.md`, and helper scripts under `tools/agents/`.
- Documentation now includes reference and phase starter areas plus Markdown prose-wrapping policy.
- The sync helper now covers cockpit, agent helpers, phase/base navigation seeds, Codex root files, and reference README seeding.

## Documentation Coverage (All Types Considered)
Set each item to one of: `updated`, `new`, `not-applicable`, `deferred`.

- features: not-applicable
- requirements: not-applicable
- tasks: not-applicable
- issues: not-applicable
- tests: not-applicable
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable
- changes: new
- snapshot: updated

## Follow-ups
- [ ] Decide whether to import upstream template-history `CHG-*` notes into this repo's long-term history.
