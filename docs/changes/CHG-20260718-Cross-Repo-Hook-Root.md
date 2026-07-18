---
type: "[[change]]"
id: CHG-20260718-Cross-Repo-Hook-Root
aliases: ["CHG-20260718-Cross-Repo-Hook-Root"]
title: "Gate hooks resolve the repo root from the target file's path (cross-repo edits gated against the right SNAPSHOT)"
status: merged
owner: user:edwin
created: 2026-07-18
updated: 2026-07-18
source:
  - docs/changes/CHG-20260717-Consistency-Debt-Pass.md
commit: ""
pr: ""
impacts:
  - "tools/adapters/claude-code/hooks/document-first-gate.sh"
  - "tools/adapters/claude-code/hooks/verification-gate.py"
issues: []
features: []
related: []
---

# Cross-Repo Hook Root Resolution

## Summary

During the FEAT-0018 delegation, the cockpit implementation agent (editing `../project-os-cockpit` files from a session rooted in the template repo) was gated against the template's SNAPSHOT instead of the cockpit's — HC-001 denied edits that were fully documented in the target repo, and the agent had to fall back to shell writes for those files. Root cause: both blocking gates resolved the repo root from `$CLAUDE_PROJECT_DIR`/cwd only.

## Impact

- `document-first-gate.sh` (HC-001) and `verification-gate.py` (HC-003) now walk up from the **edited file's path** to the nearest `SNAPSHOT.yaml`, falling back to cwd / `$CLAUDE_PROJECT_DIR`. Cross-repo edits are gated against the target repo's focus, statuses, and tests — the repo the edit actually lands in.
- Verified: with the session rooted in the template (empty placeholder focus), an edit targeting the cockpit repo (active focus set there) is allowed by HC-001 and HC-003 checks run against the cockpit snapshot.
- Advisory hooks (HC-004 phase alignment, HC-005 risk scan) still use `$CLAUDE_PROJECT_DIR`; acceptable for reminders, noted here in case cross-repo advisories ever matter.

## Documentation Coverage (All Types Considered)

- features: not-applicable
- requirements: not-applicable
- tasks: not-applicable (project-os-dev TASK-0043 caveat trail)
- issues: not-applicable
- tests: not-applicable
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable
- changes: new
- snapshot: not-applicable (template placeholder)

## Follow-ups

- [ ] Fleet rollout carries this fix with the rest of the 2026-07-17 change set.
