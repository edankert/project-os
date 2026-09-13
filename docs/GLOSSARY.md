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
- **survey**: The walk sheet's first section: the surfaces this release changed, and the changes that changed them.
- **walk order**: `docs/tests/acceptance/WALK.md`, the one file per project that authors the sitting order.
