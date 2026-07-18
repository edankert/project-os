---
type: "[[change]]"
id: CHG-20260717-Native-Adapter-Generation
aliases: ["CHG-20260717-Native-Adapter-Generation"]
title: "Native adapter generation: Claude Code skills/subagent from canonical playbooks, Cursor rules, one-step install, mechanical review check"
status: merged
owner: user:edwin
created: 2026-07-17
updated: 2026-07-17
source:
  - ../project-os-dev/docs/features/template-completeness/plan/tasks/TASK-0042-Native-Claude-Adapter.md
commit: ""
pr: ""
impacts:
  - "tools/scripts/generate-adapters.py"
  - ".claude/skills"
  - ".claude/agents"
  - ".cursor/rules"
  - "tools/adapters"
  - "tools/skills/adapter-sync"
  - "tools/scripts/validate-docs.py"
issues: []
features: []
related: []
---

# Native Adapter Generation

## Summary

project-os previously delivered its 23 skill playbooks as a bullet list of paths the agent was asked to read, used no native Claude Code machinery beyond hooks, and left the Cursor adapter an ungenerated stub. `tools/scripts/generate-adapters.py` now derives the native adapter surface from the canonical sources in one idempotent step. Program tracking: project-os-dev FEAT-0010 / TASK-0042.

## Impact

- **Native Claude Code skills**: `.claude/skills/<name>/SKILL.md` generated per playbook — auto-discovered, `/close-out`-style invocable, `description` carries the playbook's "When to use" triggers; body defers to the canonical playbook (single source of truth). Generated files carry a do-not-edit header.
- **Independent-reviewer subagent**: `.claude/agents/independent-reviewer.md`, pinned to a fixed Claude model for a deterministic `reviewed_by`, briefed to refute rather than confirm, and required to flag same-family authorship (cross-vendor review still recorded manually per QUALITY.md).
- **One-step install**: `generate-adapters.py --install-hooks` regenerates all artifacts and installs/merges the Claude Code hook set into `.claude/settings.json`, replacing SYNCING.md's manual copy step; `--check` verifies freshness and now runs at pre-commit and CI.
- **Cursor un-stubbed**: `.cursor/rules/*.mdc` generated (instructions inlined per the adapter mapping + always-active `skills.mdc` index); cursor adapter `status: active`.
- **Mechanical review check**: the validator now warns when a `passing` TST-* or `merged` CHG-* item lacks `review_verdict`, and errors when one is settled with `review_verdict: changes-requested` — the independent-review rule is no longer purely advisory.
- **Adapter layer repositioned**: `AGENTS.md`/`LLM_BRIEF.md` documented as the generic (cross-tool) layer; codex adapter is a consumer of it; adapter-sync SKILL rewritten as the multi-tool regeneration playbook.

## Documentation Coverage (All Types Considered)

- features: not-applicable (tracked in project-os-dev FEAT-0010)
- requirements: not-applicable
- tasks: not-applicable (project-os-dev TASK-0042)
- issues: not-applicable
- tests: not-applicable
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable
- changes: new
- snapshot: not-applicable (template placeholder)

## Follow-ups

- [ ] Fleet rollout: run the generator in each downstream repo (the manifest sync does this automatically).
- [ ] Consider packaging the generated artifacts as an installable Claude Code plugin (marketplace form) if out-of-repo installation is ever needed; the in-repo `.claude/` form was chosen to avoid duplicating every skill three times.
