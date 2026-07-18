---
type: "[[change]]"
id: CHG-20260717-Consistency-Debt-Pass
aliases: ["CHG-20260717-Consistency-Debt-Pass"]
title: "Consistency-debt pass: release lifecycle, unified hook codes, computed metrics, taxonomy and docs fixes"
status: merged
owner: user:edwin
created: 2026-07-17
updated: 2026-07-17
source:
  - ../project-os-dev/docs/features/template-completeness/plan/tasks/TASK-0041-Consistency-Debt-Pass.md
commit: ""
pr: ""
impacts:
  - "tools/instructions"
  - "tools/scripts/validate-docs.py"
  - "tools/adapters"
  - "docs/__templates__"
  - "docs/__bases__"
  - ".claude/settings.json"
issues: []
features: []
related: []
---

# Consistency-Debt Pass

## Summary

A full review of the template (2026-07-17) found a layer of internal contradictions accumulated across waves. This change makes the template consistent with its own doctrine. Program tracking lives in project-os-dev (FEAT-0010 / TASK-0041).

## Impact

- **Release lifecycle unified** on `draft → staged → released → rolled-back`: STATUSES.md gains `[[release]]` (plus `[[plan]]`, `[[reference]]`) sections; the validator enforces release statuses; release-prep no longer uses `published`; SCHEMAS.md documents `release.md` and `plan.md`; SNAPSHOT.md lists `items.releases` and release fields. Downstream `published` releases normalize to `released` at next sync.
- **Hook contracts renumbered to one scheme**: HOOKS.md is now tool-neutral "Hook contracts" HC-001..007 matching the Claude Code adapter and script headers; a legacy CHC→HC mapping is included; risk-scan (HC-005) is now a first-class contract.
- **Metrics are computed, not hand-maintained**: the validator recomputes `metrics.counts` from notes+snapshot (definitions in SNAPSHOT.md "Metrics"), errors on drift, and `--fix-metrics` rewrites the block. QUALITY.md's enforcement claim is now literally true. Fleet note: your-trainer/your-sudoku/yourtrainer-mcp/cockpit currently drift against these definitions (your-sudoku counts code tests, not TST notes, in `tests_total`) — resolve per-repo at rollout.
- **document-first-gate.sh fixed** (found by dogfooding the hooks in this repo): the focus grep ranges could never see `task:`/`issue:` in a standard focus block, so the gate denied code edits even with focus set; config dotfiles/`.github/`/`.claude/` are now exempt per the contract; `template.replace_me: true` snapshots bypass the gate (a placeholder snapshot cannot carry focus).
- `level: acceptance` added to TAXONOMY.md/SCHEMAS; `docs/__templates__/acceptance-tests.md` created (TESTING.md's referenced ACCEPTANCE_TESTS.md structure, previously unscaffoldable); TESTING.md gains standard instruction frontmatter.
- adapters/README.md rewritten (four adapters, enforcement asymmetry table — it falsely claimed only Codex shipped); instructions/README.md indexes all 16 instruction files; LIFECYCLE.md close-out step 1 lists correct terminal statuses.
- Bases fixed: issue grouping uses `parent` (`affects` is not in the schema); "Open" filters use only taxonomy statuses.
- The template repo now dogfoods its own adapter: `.claude/settings.json` installed (the HC-* gates fired during this very change set and caught real bugs).

## Documentation Coverage (All Types Considered)

- features: not-applicable (tracked in project-os-dev FEAT-0010)
- requirements: not-applicable
- tasks: not-applicable (project-os-dev TASK-0041)
- issues: not-applicable
- tests: not-applicable
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable
- changes: new
- snapshot: not-applicable (template placeholder)

## Follow-ups

- [ ] Fleet rollout: sync + normalize `published`→`released`, run `--fix-metrics` per repo (decide per-repo whether `tests_*` keys mean TST notes or code tests before fixing).
