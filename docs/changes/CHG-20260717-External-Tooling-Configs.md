---
type: "[[change]]"
id: CHG-20260717-External-Tooling-Configs
aliases: ["CHG-20260717-External-Tooling-Configs"]
title: "External tooling wired: lint/format configs, lychee link-check CI, named mutation-testing tools, generator freshness gates"
status: merged
owner: user:edwin
created: 2026-07-17
updated: 2026-07-17
source:
  - ../project-os-dev/docs/features/template-completeness/plan/tasks/TASK-0045-External-Tool-Wiring.md
commit: ""
pr: ""
impacts:
  - ".markdownlint.jsonc"
  - ".yamllint.yml"
  - ".github/workflows/link-check.yml"
  - ".github/workflows/validate-docs.yml"
  - "tools/scripts/hooks/pre-commit"
  - "tools/instructions/TESTING.md"
  - "tools/instructions/MARKDOWN.md"
issues: []
features: []
related: []
---

# External Tooling Configs

## Summary

MARKDOWN.md mandated prettier's `proseWrap: never` without shipping tooling, TESTING.md's `mutation_score` field named no tool, and external URLs were never checked. This wires the named external tools into the template. Program tracking: project-os-dev FEAT-0010 / TASK-0045.

## Impact

- Ships `.markdownlint.jsonc` and `.yamllint.yml` tuned to house style (`.prettierrc` already existed); all three are `seed`-owned in the sync manifest (copied once, downstream-owned after).
- `.github/workflows/link-check.yml`: weekly lychee run over external URLs (internal links stay with validate-docs).
- TESTING.md names per-stack mutation tools (mutmut, Stryker, cargo-mutants, PIT, muter) so `mutation_score` is actionable.
- Generator freshness is now gated: `generate-adapters.py --check` runs in the pre-commit hook and the validate-docs CI workflow.

## Documentation Coverage (All Types Considered)

- features: not-applicable (tracked in project-os-dev FEAT-0010)
- requirements: not-applicable
- tasks: not-applicable (project-os-dev TASK-0045)
- issues: not-applicable
- tests: not-applicable
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable
- changes: new
- snapshot: not-applicable (template placeholder)

## Follow-ups

- [ ] Downstream repos with real code test suites: wire the matching mutation tool and start recording `mutation_score` on guarding tests.
