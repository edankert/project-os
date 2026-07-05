---
type: "[[change]]"
id: CHG-20260705-Extend-status-taxonomy
aliases: ["CHG-20260705-Extend-status-taxonomy"]
title: "Extend status taxonomy with states in real downstream use"
status: merged
owner: unassigned
created: 2026-07-05
updated: 2026-07-05
source:
  - docs/changes/CHG-20260705-Mechanical-verification-and-independent-review.md
commit: ""
pr: ""
impacts:
  - "tools/instructions/STATUSES.md"
  - "tools/scripts/validate-docs.py"
issues: []
features: []
related: []
---

# Extend Status Taxonomy

## Summary
The fleet-wide validator rollout showed three downstream repos systematically using statuses the taxonomy never defined (~197 occurrences): requirement `implemented`/`fulfilled`/`met`, task/feature/issue `deferred`/`cancelled`, issue `reopened`/`wont-fix`, feature/requirement `superseded`. These are semantically real states, not drift, so the template taxonomy now includes them; pure synonyms are normalized downstream instead (fulfilled/met/done→implemented, proposed→draft, issue backlog→open, accepted→wont-fix).

## Impact
- STATUSES.md: task +`deferred`,`cancelled`; issue +`reopened`,`wont-fix`,`deferred`; feature +`deferred`,`cancelled`,`superseded`; requirement +`implemented`,`deferred`,`cancelled`,`superseded`. `implemented` is explicitly pre-verification: `verified` still requires passing linked tests per QUALITY.md.
- validate-docs.py hardcoded defaults updated to match; per-repo STATUSES.md overrides continue to take precedence.

## Documentation Coverage (All Types Considered)
Set each item to one of: `updated`, `new`, `not-applicable`, `deferred`.

- features: not-applicable
- requirements: not-applicable
- tasks: not-applicable
- issues: not-applicable
- tests: not-applicable
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable
- changes: new
- snapshot: updated

## Follow-ups
- [ ] Downstream repos: re-sync STATUSES.md + validate-docs.py; normalize synonym statuses.
