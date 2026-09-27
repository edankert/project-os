---
type: glossary
id: GLOSSARY
status: active
owner: team:docs
created: 2026-01-26
updated: 2026-01-26
tags: [glossary]
---

# Glossary

> REPLACE ME (template): Replace these terms with your project’s vocabulary (and delete terms that don’t apply).

- **workflow**: A canonical “front door” activity documented under `workflows/`.
- **feature**: A work package (goal + scope + acceptance) tracked under `features/`.
- **issue**: A problem/gap/bug tracked under `issues/`.
- **change note**: A “what changed and why” record under `changes/`.
- **release test**: Testing a release by hand, check by check. Until 2026-09-27 it was called the walk (project-os-dev ADR-0050).
- **release test sheet**: The generated document a release is tested from — the changed screens first, then every owed check in order with its setup, steps and expected result inline (`tools/instructions/TESTING.md`, "The release test").
- **tester**: The person doing the release test.
- **section**: A group of checks that share one setup state — one build, one account tier, one piece of hardware on the bench — tested in one go.
- **what changed**: The release test sheet's first part: the screens this release changed, one sentence per change, with the screen at the last release beside the screen now.
- **result**: What a tester records for a check: pass, fail, partial, question, blocked, N/A or excused. A ledger entry stores it under `result`.
- **test kind**: Feature, regression or automated: which of the three kinds a check is, derived from its `covers:` and `command:`.
- **procedure**: A written script for one section — the setup stated once, then numbered steps, each naming the screen it happens on. One file per section under `docs/tests/acceptance/release-test/`.
- **owed part**: One numbered step of a check this platform still owes, which is what a procedure is counted against. A check whose steps are not numbered is one part.
- **expectation tag**: A label such as `TST-0648.4` on a line of a procedure step, saying that line satisfies step 4 of that check.
- **section order**: `docs/tests/acceptance/RELEASE-TEST.md`, the one file per project that authors the order of the sections.
