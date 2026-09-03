---
type: "[[change]]"
id: CHG-20260903-Prompting-Guide-Contradictions
title: "Four places where the template contradicted its own decisions now state the rule once or link to it"
status: merged
owner: user:edwin
created: 2026-09-03
updated: 2026-09-03
source: ["project-os-dev docs/reference/Prompting-Guide-Review-2026-09-03.md, findings 1.1 to 1.4", "project-os-dev ISS-0041, ISS-0042, ISS-0043, ISS-0044"]
commit: "1b5956e, 685eef7, 0049206, fda2e8a"
pr: ""
impacts: ["tools/skills/independent-review/SKILL.md", "tools/skills/docs-audit/SKILL.md", "tools/adapters/claude-code/ADAPTER.md", "tools/instructions/HOOKS.md", "tools/adapters/claude-code/hooks/model-routing-hint.sh", "tools/instructions/QUALITY.md", "tools/skills/release-prep/SKILL.md", "tools/skills/release-verification/SKILL.md", "tools/skills/feature-scaffold/SKILL.md", "tools/instructions/TAXONOMY.md", "docs/__templates__/release.md", "docs/__templates__/test.md", "docs/__templates__/SCHEMAS.md", "docs/__templates__/README.md", "docs/__templates__/acceptance-tests.md", "tools/scripts/generate-adapters.py", ".claude/agents/planner.md", ".claude/agents/independent-reviewer.md", ".cursor/rules/quality.mdc"]
issues: []
features: []
related: ["[[INSTR-QUALITY]]", "[[INSTR-HOOKS]]", "[[INSTR-TAXONOMY]]"]
---

# Four contradictions removed

## Summary

An agent reading the template was told two different rules in four places, and a strong instruction-follower obeys whichever it read last. A review of the template against the Claude Fable 5.1, Fable 5 and Opus 5 prompting guides on 2026-09-03 found the four. Each is now stated once, in the file that owns it, and linked from everywhere else. The rule that makes this a rule is project-os-dev ADR-0024, accepted the same day.

1. **Review independence.** ADR-0013 decided that a reviewer is independent when it starts from a clean context, not when it runs on a different model family. The review skill's own checklist, the docs-audit skill, the Claude Code adapter and the HC-008 contract still said "different model". All four now point at `QUALITY.md` "Independent review (clean-context)". HC-008 is renamed from "model routing hint" to "delegation hint", since the model is no longer what it routes on; the script keeps its filename so existing `.claude/settings.json` files keep resolving.
2. **Grandfathering.** `QUALITY.md` said the feature-requirement gate was keyed on a note's `updated:` date and re-armed on any edit. `STATUSES.md` says grandfathering is an ID list with no date exemption, and that the date heuristic was removed for exactly that re-arming (ISS-0007). The QUALITY.md paragraph is gone and links instead.
3. **Retired vocabulary.** The release skills and two templates still instructed `CHK-*` files, Tier 1 to 3, `in-review`, `in-progress`, `staged`, `rolled-back` and `kind: manual`, none of which exist in the current taxonomy. They now say what `STATUSES.md` and `TESTING.md` say: acceptance checks are `TST-*` notes at `level: acceptance`, sections derive from `covers:` and `command:`, a release is blocked while a manual check is unsettled, a check with a `command:` is settled by CI, release statuses are `draft`, `released` and `reverted`, and feature statuses are `doing` and `review`. `tier` is removed from the test template and marked removed in the schema; `kind` moves to the taxonomy's retired list; the templates README no longer names a `check.md` that does not exist.
4. **The model pins.** The adapter called the subagent pins "the strongest available Claude model". They were `claude-opus-5`, and Fable 5.1 exists. Both pins are now `claude-fable-5-1`, the adapter describes them as a choice revisited at each model release, and it notes that review quality holds at lower effort.

## Impact

- Agents running release-prep or release-verification stop looking for files and statuses that no longer exist.
- The `planner` and `independent-reviewer` subagents run on `claude-fable-5-1` after the next `generate-adapters.py` run in each downstream repo; `reviewed_by` records `model:claude-fable-5-1` from then on.
- The delegation hint's status lists now match the current taxonomy: `review` and `declined` were missing, and `next`, `reopened`, `closed`, `in-progress`, `in-review` and `wont-fix` were listed but can never occur. A feature at `review` used to fall through to "no active focus item resolved".
- The hint's prefix changes from "project-os model routing:" to "project-os delegation hint:". Nothing parses it.
- Downstream repos pick everything up through the normal template sync plus a generator run (`tools/skills/adapter-sync/SKILL.md`).

## Documentation Coverage (All Types Considered)
Set each item to one of: `updated`, `new`, `not-applicable`, `deferred`.

- features: not-applicable
- requirements: not-applicable
- tasks: not-applicable
- issues: updated
- tests: not-applicable
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable
- changes: new
- snapshot: not-applicable

The four issues and the decision live in project-os-dev (ISS-0041 to ISS-0044, ADR-0024, REQ-0027), which tracks this template's development; this repo's snapshot is the template placeholder and carries no items.

## Follow-ups

- [ ] The release-verification skill's verdict model still predates ADR-0010 and ADR-0037: step 6 resets stale tests to `status: ready` by hand, and step 3 judges staleness from `last_run` on the note. Filed in project-os-dev as its own issue rather than fixed here, because it is a model change and not a vocabulary one.
- [ ] Sync to the downstream repos and re-run the generator in each.
