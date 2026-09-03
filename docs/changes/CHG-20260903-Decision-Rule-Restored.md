---
type: "[[change]]"
id: CHG-20260903-Decision-Rule-Restored
title: "The DECISION-RULE check is back in the validator after sixteen days missing"
status: merged
owner: user:edwin
created: 2026-09-03
updated: 2026-09-03
source: ["project-os-dev ISS-0047", "project-os-dev TST-0004"]
commit: "8faea70"
pr: ""
impacts: ["tools/scripts/validate-docs.py"]
issues: []
features: []
related: ["[[INSTR-DECISIONS]]", "[[CHG-20260812-Rule-ADRs]]"]
---

# The DECISION-RULE check is back

## Summary

A decision note that carries a `## Rule` heading and no `## Domain` or `## Conformance` section is a validator error again. `DECISIONS.md` has said so since 2026-08-12, and the harness `tools/scripts/test-decision-rule.py` has tested it since then. The check itself was gone: commit `6ca15f4` added `validate_decision_rule` on 2026-08-12, and commit `57739c9` on 2026-08-18, an acceptance-model change hand-merged from a downstream repo, dropped the function, its two helpers and its call site without saying so. For sixteen days the instruction said "this is checked", the harness failed on a clean tree with `AttributeError: module 'vd' has no attribute 'validate_decision_rule'`, and no commit ran it.

This change restores the four pieces verbatim from `6ca15f4`: the HTML-comment and `TST-####` regexes, `_decision_sections`, `validate_decision_rule`, and the call in `validate()` after `validate_decision_options`. Nothing about the check's contract changes; the harness passes 26 of 26 assertions, the same count the review of 2026-08-12 recorded.

## Impact

- The template's own validator errors again on a malformed rule-ADR. Run against every repo under `~/Dev/repos` on 2026-09-03 the restored check reports zero findings, so no downstream repo breaks at its next sync.
- Downstream copies of `tools/scripts/validate-docs.py` still lack the check until they sync. The bundled cockpit validator, `tools/cockpit/src/project_os_cockpit/validate_docs_bundled.py`, is a separately maintained fork owned by project-os-cockpit and also lacks it; that is filed as a follow-up rather than patched in the vendored copy.

## Documentation Coverage (All Types Considered)
Set each item to one of: `updated`, `new`, `not-applicable`, `deferred`.

- features: not-applicable
- requirements: not-applicable
- tasks: not-applicable
- issues: updated
- tests: updated
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable
- changes: new
- snapshot: not-applicable

The issue (ISS-0047) and the test note (TST-0004) live in project-os-dev, which tracks this template's development.

## Follow-ups

- [ ] Restore the same check in project-os-cockpit's validator and ship it in the next cockpit release.
- [ ] Wire `tools/scripts/run-tests.py` into pre-commit or CI in project-os-dev, so a `TST-*` with a `command:` cannot sit at `passing` for sixteen days after its harness broke.
