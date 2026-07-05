---
type: "[[change]]"
id: CHG-20260705-Mechanical-verification-and-independent-review
aliases: ["CHG-20260705-Mechanical-verification-and-independent-review"]
title: "Mechanical verification enforcement and independent review capabilities"
status: merged
owner: unassigned
created: 2026-07-05
updated: 2026-07-05
source:
  - compass_artifact_wf-84fa61ff-0d47-4742-a0b7-97fec656e051_text_markdown.md
commit: ""
pr: ""
impacts:
  - "tools/scripts"
  - "tools/adapters/claude-code"
  - "tools/skills"
  - "tools/instructions"
  - "docs/__templates__"
  - ".github/workflows"
issues: []
features: []
related:
  - tools/scripts/validate-docs.py
  - tools/skills/independent-review/SKILL.md
  - tools/skills/docs-audit/SKILL.md
---

# Mechanical Verification Enforcement and Independent Review Capabilities

## Summary
Implements the six evidence-backed capability changes recommended by the 2026 reliability research review (see source): the strongest documented failure mode of documentation-centric agent systems is that rules enforced by convention are silently bypassed, so this change converts project-os's core invariants from convention into mechanism and adds independent-review and audit capabilities.

## Impact
- **New docs validator (`tools/scripts/validate-docs.py` + `.sh` wrapper):** one deterministic script checks snapshot↔filesystem agreement, frontmatter/status consistency, counter integrity, link-graph integrity, and the verification invariant (no terminal status without passing linked tests). Called from the Stop hook, the git pre-commit hook, and CI, so QUALITY.md's "discrepancies are a build failure" is now literally true.
- **Verification gate is now blocking:** `tools/adapters/claude-code/hooks/verification-gate` moved from advisory PostToolUse to blocking PreToolUse; it denies edits that set `done`/`closed`/`verified` while linked `TST-*` notes are not `passing`, with an explicit recorded-waiver escape (`verification_waiver`).
- **Git + CI enforcement:** `tools/scripts/install-git-hooks.sh` installs a pre-commit hook running the validator; `.github/workflows/validate-docs.yml` runs it in CI as the non-bypassable backstop.
- **New skill `independent-review`:** a different-model review pass over changes that create/update `TST-*` or `CHG-*` notes, recorded via `reviewed_by` frontmatter.
- **New skill `docs-audit`:** periodic full-scope cross-document consistency audit run to quiescence (two consecutive clean passes), referenced from backlog grooming.
- **Intake ambiguity checks:** `issue-intake` gains a spec-ambiguity checklist before ID allocation.
- **Test adequacy:** `TST-*` template and TESTING.md gain adequacy/mutation-score fields answering "who verifies the tests?".

## Documentation Coverage (All Types Considered)
Set each item to one of: `updated`, `new`, `not-applicable`, `deferred`.

- features: not-applicable
- requirements: not-applicable
- tasks: not-applicable
- issues: not-applicable
- tests: not-applicable
- workflows: not-applicable
- decisions: not-applicable
- risks: deferred
- changes: new
- snapshot: updated

## Follow-ups
- [ ] Downstream repos: run `tools/scripts/sync-project-os.sh`, then `tools/scripts/install-git-hooks.sh`, and re-copy `tools/adapters/claude-code/hooks.json` into `.claude/settings.json` to pick up the PreToolUse verification gate.
- [ ] Consider a `RISK-*` note in downstream repos for the new `python3` (stdlib-only) requirement of the validator and hooks.
- [ ] Evaluate after ~a quarter: if mutation scores on guarding tests are consistently >80%, reduce audit cadence (threshold from the source research).
