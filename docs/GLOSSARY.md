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
- **walk**: To execute an acceptance check by hand.
- **walk sheet**: The generated document a release is walked from — the changed screens first, then every owed check in order with its setup, steps and expected result inline (`tools/instructions/TESTING.md`, "The walk").
- **sitting**: A group of checks that share one setup state — one build, one account tier, one piece of hardware on the bench — walked in one go.
- **survey**: The walk sheet's first section: the screens this release changed, one sentence per change, with the screen at the last release beside the screen now.
- **procedure**: A written script for one sitting — the setup stated once, then numbered steps, each naming the screen it happens on. One file per sitting under `docs/tests/acceptance/walk/`.
- **owed part**: One numbered step of a check this platform still owes, which is what a procedure is counted against. A check whose steps are not numbered is one part.
- **expectation tag**: A label such as `TST-0648.4` on a line of a procedure step, saying that line satisfies step 4 of that check.
- **walk order**: `docs/tests/acceptance/WALK.md`, the one file per project that authors the sitting order.
