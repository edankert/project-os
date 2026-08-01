---
type: "[[change]]"
id: CHG-20260801-A-local-pass-is-not-a-CI-pass
title: "A local pass is not a CI pass: clean-clone verification, an untracked-artifact guard, and a corrected claim"
status: merged
date: 2026-08-01
---

# A local pass is not a CI pass

A downstream repo (`your-health`) failed the `validate-docs` workflow on **every push for days** while `validate-docs.sh` reported `OK` locally on each one. The local result was offered as evidence that CI would pass. It never could.

## What actually happened

`generate-adapters.py` writes two trees. `.cursor/rules/**` was tracked; `.claude/skills/**` and `.claude/agents/**` were swallowed by a stock `# Claude Code` / `.claude/` line inherited from an Android scaffold's `.gitignore` on the repository's first commit — months before project-os began generating into that directory.

CI checks out a tree where half the artifacts **do not exist** and reports all 27 stale. Regenerating cannot fix it; the fix is always in `.gitignore`. Locally the same command passed, because the working tree *did* contain them — ignored by git, present on disk.

`SYNCING.md` already called these "template-owned build outputs", and project-os itself tracks 28 of them. The downstream ignore was the anomaly, and nothing detected the contradiction.

## The class, not the instance

This is the **second** time this shape has bitten. The first: an unanchored `inbox/` matched `docs/features/inbox/`, so a feature note, its plan and three task notes were absent from `main` for weeks — and the fresh clone then failed the validator with four metric errors *while the authoring machine validated clean*.

Same mechanism both times: **local checks read the working tree, CI reads the commit.** Anything ignored, untracked, or unstaged is invisible on one side and absent on the other. The local run does not merely miss it — it reports success, and the success is believed.

## Three changes

**1. `validate-docs.sh --as-committed`.** Materialises `HEAD` into a temporary tree and runs the full CI step set there — validator, `sync-snapshot --check`, `generate-adapters --check`. This is the mechanical guard for the whole class: it answers *what will a fresh clone see*, which no working-tree check can.

**2. `generate-adapters --check` fails on untracked artifacts.** The precise trap, named precisely: artifacts that exist on disk but are absent from `git ls-files` now report `UNTRACKED` with a message pointing at `.gitignore`. Verified against a reconstruction of the downstream failure — 27 untracked, exit 1; tracked, exit 0.

It returns clean when git is unavailable or the directory is not a repository. An inability to check is not evidence of a problem.

**3. The corrected claim.** `LIFECYCLE.md` step 7 said *"the same validator runs at pre-commit and in CI"*. That was false — CI runs three steps, not one — and it is what licensed treating a green local run as a green build. It now states what CI actually runs, why a working-tree check cannot stand in for it, and both historical instances. Close-out gains two steps: check as-committed before pushing, and **confirm the run went green after**. The same two lines are baked into every generated skill adapter, since that text is what an agent reads before it reaches the source playbook.

## Note on the shape of the fix

Steps 1 and 2 are mechanical; step 3 is a document. Only the first two would have caught this unaided — but the false sentence is what made the failure *reportable as a success* for days, so correcting it is not decoration. A check that fails in both places is a nuisance; one that passes locally and fails remotely for a structural reason actively manufactures false confidence.


## Follow-up: divergence triage

`DIVERGED` said only *that* a file differs, leaving the operator to hand-diff before they could act — and it covered two cases wanting opposite responses: a fix made downstream and never pushed up (forcing destroys it, silently and permanently) versus a merely older copy (forcing is correct and loses nothing).

The sync now labels each one:

| label | meaning |
|---|---|
| `SUBSET` | every downstream line exists upstream — `--force` is safe |
| `LOCAL-CONTENT` | N lines exist only downstream — `--force` discards them |
| `CONFLICT` | both sides moved since the baseline |
| `UNKNOWN` | no baseline recorded, so no claim is made |

### What it deliberately does not say

The first draft called the second case `PUSH-UPSTREAM` and told the operator to upstream those lines. Run against a real repo it immediately proved that wrong: six repos carry an older `migrate-status-vocabulary.py` whose downstream-only lines are an **outdated docstring**, and instructing anyone to push those into the template would have been confidently incorrect.

Whether downstream-only content is a valuable fix or stale prose is a judgement the tool cannot make. It now reports the fact and stops — `LOCAL-CONTENT` names what exists, and the operator reads the diff. `UNKNOWN` follows the same discipline: an inability to tell is not evidence either way.

Only `SUBSET` is a safety claim, and it is the one the tool can actually prove.
