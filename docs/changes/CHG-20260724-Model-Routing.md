---
type: "[[change]]"
id: CHG-20260724-Model-Routing
aliases: ["CHG-20260724-Model-Routing"]
title: "Model routing: planner subagent, HC-008 routing hint, and reviewer/planner model pins that keep review off the authoring model"
status: merged
owner: user:edwin
created: 2026-07-24
updated: 2026-07-24
source:
  - ../project-os-cockpit/docs/features/model-routing/FEAT-0039-Model-Routing-Subagents.md
commit: ""
pr: ""
reviewed_by: "model:claude-opus-4-8"
review_date: 2026-07-24
review_verdict: approved
review_note: "First pass returned changes-requested (9 findings, one HIGH: this change had weakened the QUALITY.md different-model-FAMILY rule to same-model and mis-stated opusplan). All addressed before merge; re-reviewed clean. Same-family review — NOT independent per QUALITY.md; a cross-vendor or human pass is still owed."
impacts:
  - "tools/scripts/generate-adapters.py"
  - "tools/adapters/claude-code/hooks/model-routing-hint.sh"
  - "tools/adapters/claude-code/hooks.json"
  - "tools/adapters/claude-code/ADAPTER.md"
  - "tools/instructions/HOOKS.md"
  - ".claude/agents"
  - ".claude/settings.json"
issues: []
features: []
related: []
---

# Model Routing

## Summary

Claude Code has no native "model A plans, model B implements" split along project-os phases — the only built-in combo alias is `opusplan` (Opus in plan mode → Sonnet for execution), and it governs the main loop only. project-os now gets per-phase model routing from the one place a model can be pinned declaratively: subagent frontmatter. The generator emits a second model-pinned subagent (`planner`, owning LIFECYCLE preflight) alongside the existing `independent-reviewer`, both pinned via named constants, and a new advisory `UserPromptSubmit` hook (HC-008) derives a routing hint from the focus item's status so the delegation actually happens instead of depending on the agent remembering to delegate. Prototyped downstream in project-os-cockpit FEAT-0039 and upstreamed here so the fleet inherits it through the manifest sync plus a generator run.

## Impact

- **Planner subagent**: `.claude/agents/planner.md` generated from `PLANNER_AGENT`, owning preflight only (classify, run the spec-ambiguity check, allocate IDs, update `SNAPSHOT.yaml`, create notes from templates) and explicitly barred from writing implementation code. It defers to the canonical playbooks rather than restating them, so it cannot drift from `tools/skills/`.
- **Reviewer model pin changed** from `claude-opus-4-8` to `claude-fable-5`, and both pins now live in named constants (`PLANNER_MODEL`, `REVIEWER_MODEL`) at the top of the generator. This changes the recorded `reviewed_by` value for future reviews. The pin is a *harm-reduction* choice, not a fix for independence: it moves the reviewer off the model most likely to have authored the work, which avoids literal self-review. It does **not** satisfy `QUALITY.md`, which requires a different model *family* or a human — subagents can only pin Claude models, so no pin can. The reviewer's briefing and `ADAPTER.md` now say this explicitly instead of implying the pin difference is the safeguard.
- **HC-008 model routing hint**: new advisory `UserPromptSubmit` hook, added to `hooks.json` and documented in `HOOKS.md`. Maps planning statuses → `planner`, execution statuses → main loop, review statuses → `independent-reviewer`; stays silent on a template placeholder snapshot (`replace_me: true`) or when no snapshot exists. Advisory by necessity — a hook cannot change the session model, so the pins do the enforcing.
- **ADAPTER.md** gains a "Model routing" section with the phase→model table, an explicit statement that the pins do not deliver independence (with the reason), the advice to keep the session model off `REVIEWER_MODEL` as harm reduction, the note that subagent pins take precedence over the session model (so they survive `opusplan`), and how to retarget the pins.

## Documentation Coverage (All Types Considered)

- features: not-applicable (prototype tracked in project-os-cockpit FEAT-0039)
- requirements: not-applicable
- tasks: not-applicable (project-os-cockpit TASK-0195/TASK-0196)
- issues: not-applicable
- tests: not-applicable (no test surface for adapter generation beyond `generate-adapters.py --check`, which runs at pre-commit and CI; hook exercised manually across all status branches)
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable (advisory hook, always exits 0; no new dependency — stdlib/bash only)
- changes: new
- snapshot: not-applicable (template placeholder)

## Follow-ups

- [ ] Fleet rollout: downstream repos pick this up on their next manifest sync plus `python3 tools/scripts/generate-adapters.py --install-hooks`; repos with a hand-written `hooks` key in `.claude/settings.json` need `--force-hooks` or a manual merge to gain the `UserPromptSubmit` entry.
- [ ] Revisit `PLANNER_MODEL`/`REVIEWER_MODEL` when the next model generation ships — full IDs are pinned deliberately (deterministic `reviewed_by`) and therefore need a manual bump.
