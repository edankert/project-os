# Project: project-os (documentation framework template)

Read SNAPSHOT.yaml at session start to understand current project state and focus.
Read CONTEXT.md for the full project-os contract, edit policy, and invariants.

## Role of this repo

This is the canonical project-os template. Changes to files under tools/instructions/
and tools/skills/ propagate to all downstream repos via the sync mechanism
(see tools/instructions/SYNCING.md).

When editing instruction or skill files:
- Ensure changes are broadly applicable (not project-specific)
- Update any templates/dashboards that rely on changed rules
- Consider impact on all 6 downstream repos

## project-os documentation system (core rules -- always active)

@tools/instructions/LIFECYCLE.md

## Reference instructions (read when relevant)

These files contain detailed rules. Read them when performing the related operation:
- Status taxonomies and transitions: tools/instructions/STATUSES.md
- Quality, close-out, and verification gating: tools/instructions/QUALITY.md
- Snapshot structure and update rules: tools/instructions/SNAPSHOT.md
- Allowed taxonomy values: tools/instructions/TAXONOMY.md
- Required link graphs: tools/instructions/TRACEABILITY.md
- ADR conventions: tools/instructions/DECISIONS.md
- Ownership rules: tools/instructions/OWNERSHIP.md
- Obsidian conventions: tools/instructions/OBSIDIAN.md
- Handoff/recovery: tools/instructions/HANDOFF.md
- Importing from existing projects: tools/instructions/IMPORTING.md
- Acceptance test tiers and lifecycle: tools/instructions/TESTING.md
- Hook contracts: tools/instructions/HOOKS.md
- Syncing template updates: tools/instructions/SYNCING.md

## Skill playbooks (read before performing these operations)

- Issue intake: tools/skills/issue-intake/SKILL.md
- Feature scaffold: tools/skills/feature-scaffold/SKILL.md
- Task breakdown: tools/skills/task-breakdown/SKILL.md
- Close-out: tools/skills/close-out/SKILL.md
- Change note: tools/skills/change-note/SKILL.md
- Status transition: tools/skills/status-transition/SKILL.md
- Snapshot sync: tools/skills/snapshot-sync/SKILL.md
- Test authoring: tools/skills/test-authoring/SKILL.md
- ADR authoring: tools/skills/adr-authoring/SKILL.md
- Risk scan: tools/skills/risk-scan/SKILL.md
- Ad-hoc intake: tools/skills/ad-hoc-intake/SKILL.md
- Workflow authoring: tools/skills/workflow-authoring/SKILL.md
- Backlog grooming: tools/skills/backlog-grooming/SKILL.md
- Risk mitigation: tools/skills/risk-mitigation-planning/SKILL.md
- Impact analysis: tools/skills/impact-analysis/SKILL.md
- Release preparation: tools/skills/release-prep/SKILL.md
- Release verification: tools/skills/release-verification/SKILL.md
- Adapter sync: tools/skills/adapter-sync/SKILL.md
- Project init: tools/skills/project-init/SKILL.md
- Project derive: tools/skills/project-derive/SKILL.md

## Project-specific notes

This repo contains the template itself. Documentation under docs/ tracks
the development of the project-os framework. Template files under
docs/__templates__/ and docs/__bases__/ are synced to downstream repos.
