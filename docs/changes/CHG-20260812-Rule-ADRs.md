---
type: "[[change]]"
id: CHG-20260812-Rule-ADRs
aliases: ["CHG-20260812-Rule-ADRs"]
title: "Rule-ADRs: a quantified rule rides inside the decision kind as `## Rule`/`## Domain`/`## Conformance`, and DECISION-RULE refuses the shape that binds nothing"
status: merged
owner: user:edwin
created: 2026-08-12
updated: 2026-08-12
source:
  - ../project-os-dev/docs/features/rule-adrs/FEAT-0023-Rule-ADRs-Carry-Their-Conformance.md
  - ../project-os-dev/docs/decisions/ADR-0023-A-Quantified-Rule-Is-A-Decision.md
  - ../project-os-dev/docs/decisions/ADR-0022-Conventions-Before-Types.md
commit: ""
pr: ""
impacts:
  - "tools/instructions/DECISIONS.md"
  - "docs/__templates__/adr.md"
  - "docs/__templates__/SCHEMAS.md"
  - "tools/skills/adr-authoring/SKILL.md"
  - "tools/skills/issue-intake/SKILL.md"
  - "tools/scripts/validate-docs.py"
  - "tools/scripts/test-decision-rule.py"
  - "tools/cockpit/src/project_os_cockpit/validate_docs_bundled.py"
issues: []
features: []
reviewed_by: ""
review_date: ""
review_verdict: ""
related: []
---

# Rule-ADRs

## Summary

project-os had nowhere to put a project-authored quantified rule — *every member of DOMAIN satisfies P*. Every note kind is singular (a requirement is a thing to build, a decision is a choice taken, a risk is a hazard), and the only quantified rules in the system were the validator's own check codes, template-owned and closed to projects. Projects reached for feature-less requirements instead, which the FEATURE-REQ gate never inspects — permitted, and gated by nothing.

Per project-os-dev ADR-0023 (the convention) under ADR-0022's constraint (a convention, not a new note kind), a rule is now recorded as an ordinary ADR carrying three additional body sections: **`## Rule`** (one testable normative sentence; the heading's presence is the marker), **`## Domain`** (the enumerable set the rule ranges over), **`## Conformance`** (the named discharge plus which side is authoritative on disagreement). The normative specification lives in one place — `tools/instructions/DECISIONS.md`, "A decision that states a rule" — and everything else links to it (REQ-0018's stated-once discipline; ISS-0006 is what restatement cost last time).

## Impact

- **`tools/instructions/DECISIONS.md`** — the single normative statement: the three sections and their semantics, the harvest provenance (the trigger is the *second* issue of a kind; up-front rules say "from principle" and land conformance the same day), the landing pattern over an existing corpus (`PROMOTIONS` + `tools/GRANDFATHERED.yaml`, ADR-0011 unweakened), and the `## Options` answer (rule-ADRs inherit "required when the decision offers a choice", unchanged).
- **`docs/__templates__/adr.md`** — the three headings as an optional block **inside an HTML comment**. Commented is structural, not stylistic: the heading's presence is the marker, so an uncommented `## Rule` would mark every template-derived ADR as a rule-ADR and arm `DECISION-RULE` against the template's own output.
- **`docs/__templates__/SCHEMAS.md`** — one sentence naming the convention and pointing at DECISIONS.md.
- **`tools/skills/adr-authoring/SKILL.md`** — the authoring branch: *name the domain first, and stop if it cannot be enumerated*; fill the template block; record provenance.
- **`tools/skills/issue-intake/SKILL.md`** — the harvest step, mandatory and positioned before ID allocation: a bounded sibling search (grep by keyword and surface, not a semantic read), a one-line recordable negative, and on the second issue of a kind, propose a rule-ADR instead of leaving a third one-off to be filed. The ADR-0016 tension (ceremony on the highest-frequency operation) is resolved in the skill text: the negative line is the entire cost in the common case, and the step stays mandatory because conditional steps get skipped even when the condition holds (ADR-0004).
- **`tools/scripts/validate-docs.py`** — the **`DECISION-RULE`** check: any note under `docs/decisions/` carrying a `## Rule` heading (outside fences and HTML comments) must carry a non-empty `## Domain` AND a non-empty `## Conformance`, at any ADR status; `TST-####` IDs under Conformance must resolve, while check codes, type names and prose there are never treated as references. **Error from day one**: censused 2026-08-12 across all 12 fleet repos (`^## Rule` over `docs/decisions/*.md`), exactly two notes carry the heading — your-health ADR-0020/0021, the pilot pair — and both conform, so there is no debt to migrate and a warning would be ADR-0011's forbidden permanent tier. No `PROMOTIONS` entry, no grandfather entries.
- **`tools/scripts/test-decision-rule.py`** — the check's fixture suite: 23 assertions covering absent/empty Domain, absent/empty Conformance, dangling and resolving TST references (note-resolved and snapshot-resolved), check-code-only and type-only Conformance, the fully-clean case, status independence, the casual `## Rule` heading (fires — ADR-0023's accepted cost), fenced and commented headings (quotation, not structure), and the shipped template both raw and with the block uncommented. Verified by inversion: four deliberate breaks of the check (empty-section detection, comment stripping, TST resolution, the marker gate) each fail the suite.

## The bundled copy — applied but deliberately not committed with this change

`tools/cockpit/src/project_os_cockpit/validate_docs_bundled.py` carries the same DECISION-RULE addition **in the working tree**, verified by the same 23-assertion suite run against it, plus `--self-check`. It is **not part of this change's commit**: the file was already dirty with unrelated parallel work (the FEAT-0022 claimants fix to `compute_metric_counts`) when this change landed, and committing the file would have dragged that work into this commit. The parallel work's own close-out carries both. Until then, the bundled copy's committed state does not include DECISION-RULE — anyone rebuilding from HEAD alone should know the working tree is ahead of the commit on that one file.

## Verification

- `python3 tools/scripts/test-decision-rule.py` — 23 assertions, 0 failures, against both the canonical validator and the bundled copy.
- `python3 tools/scripts/validate-docs.py --self-check` — clean (no new status collections; the two new module-level constants are compiled regexes, outside the completeness walk's remit).
- `bash tools/scripts/validate-docs.sh` — project-os as green as before the change (one pre-existing BRIEF-PLACEHOLDER warning).
- New validator run against **your-health**: both pilot rule-ADRs pass DECISION-RULE (positively confirmed parsed — Rule seen, sections non-empty, TST-0018/TST-0019 resolved); the repo's 2 pre-existing TEST-FIELDS errors are byte-identical under the HEAD validator.
- New validator run against **all 12 fleet repos**: zero DECISION-RULE findings anywhere.
- `python3 tools/scripts/generate-adapters.py --check` — all 35 artifacts current (the generated skills are pointers, so the skill edits required no regeneration).
- The executable record is project-os-dev **TST-0004**, stamped by its runner (ADR-0010).

## Documentation Coverage (All Types Considered)

- features: not-applicable (tracked in project-os-dev FEAT-0023)
- requirements: not-applicable (project-os-dev REQ-0025)
- tasks: not-applicable (project-os-dev TASK-0086..0089)
- issues: not-applicable
- tests: new (project-os-dev TST-0004 executes `tools/scripts/test-decision-rule.py` here)
- workflows: not-applicable
- decisions: not-applicable (the deciding ADRs live in project-os-dev; the pilot rule-ADRs in your-health)
- risks: not-applicable (pure-Python addition to a script that already walks `docs/decisions/`; no new dependency, env var, path, or long-running step)
- changes: new (this note; its counterpart in project-os-dev is CHG-20260812-Rule-ADRs there)
- snapshot: not-applicable (template artifact; `changes: {}` stays empty by design)

## Follow-ups

- [ ] Fleet rollout: downstream repos pick up DECISION-RULE, the template block, DECISIONS.md and both skills on their next `sync-project-os.sh` — deliberately not run as part of this change.
- [ ] `project-os-cockpit` holds a deliberately diverged validator superset (44 codes); DECISION-RULE needs a **recorded hand-merge** there, filed in that repo now that TASK-0089 has landed.
- [ ] The bundled copy's DECISION-RULE addition rides in the working tree; the parallel FEAT-0022-claimants close-out commits the file with both changes.
