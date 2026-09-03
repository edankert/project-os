---
type: "[[change]]"
id: CHG-20260903-Executable-Tests-No-Verdict
title: "A test with a command: records no verdict; CI is the verdict"
status: merged
owner: user:edwin
created: 2026-09-03
updated: 2026-09-03
source: ["project-os-dev ADR-0025, FEAT-0028, TASK-0106 to TASK-0109", "project-os-dev ISS-0046, ISS-0048 rows 1, 3 and 30"]
commit: "a8694f0, 3d67f11, 87b64cf, b5e8f9f, 293e5a2"
pr: ""
impacts: ["tools/scripts/run-tests.py", "tools/scripts/validate-docs.py", "tools/scripts/test-verdict-model.sh", ".github/workflows/validate-docs.yml", "docs/__templates__/test.md", "docs/__templates__/SCHEMAS.md", "tools/instructions/SNAPSHOT.md", "tools/skills/test-authoring/SKILL.md", "tools/skills/release-verification/SKILL.md", ".cursor/rules/snapshot.mdc", "docs/__bases__/CONTEXT.base"]
issues: []
features: []
reviewed_by: model:claude-fable-5-1
review_date: 2026-09-03
review_verdict: approved
related: ["[[INSTR-STATUSES]]", "[[INSTR-TESTING]]", "[[CHG-20260903-Instruction-Weight]]"]
---

# A test with a command: records no verdict

## Summary

A test note that carries a `command:` no longer holds a verdict. The runner runs it and reports; the CI seed runs the runner after the validator, so a failing command is a red build; the validator treats such a test as settled by CI in the verification gate. STATUSES.md and TESTING.md had said this since cockpit ADR-0038; the test template, SCHEMAS.md, the runner, the test-authoring skill and the release-verification skill still followed ADR-0010, under which the runner stamped `passing` or `failing`, `last_run:` and `exit_code:` onto the note. Edwin chose the no-verdict model on 2026-09-03 (project-os-dev ADR-0025), and everything follows it now.

## Impact

- `run-tests.py` has no `--write`. It prints an outcome per test and exits 1 on any failure. In CI (the `CI` variable set) an unrunnable command also fails the run, because a test CI cannot run has no verdict; `PROJECT_OS_ALLOW_UNRUNNABLE=1` accepts the gap deliberately. A repo whose CI runs it has a gate for its executable tests; a repo whose CI does not has none until it does, and a repo whose tests run a sibling checkout must clone it in CI.
- The validator: a linked test with a `command:` satisfies the gate at any status; a manual test is still held to `passing` and freshness. New check COMMAND-VERDICT warns on a `command:` test carrying `ready`, `passing`, `failing`, `last_run:` or `exit_code:`, as a warning until 2026-12-02. The independent review counted 98 such notes on the fleet's trees the day it landed, 67 of them in your-trainer carrying only an `exit_code:`; the first version of this note said 33, a count by status that was also wrong (29).
- The test template drops `last_run:`; SCHEMAS.md marks `last_run` and `exit_code` removed; test-authoring says a `command:` test is left at `active`; release-verification settles each test by its kind (CI, the ledger, or `last_verified:`) and resets nothing by hand, which closes project-os-dev ISS-0046.
- A downstream repo strips its own verdict fields before the cutover; `tools/scripts/test-verdict-model.sh` shows the gate and the runner behaving as described.

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
- snapshot: not-applicable

The decision, feature, tasks and test live in project-os-dev (ADR-0025, FEAT-0028, TASK-0106 to TASK-0109, TST-0008).

## Follow-ups

- [ ] Each downstream repo strips `last_run:`, `exit_code:` and the stamped status from its `command:` tests before 2026-12-02, and adds the run-tests step to its CI if it does not seed the workflow.
- [ ] The bundled cockpit validator is a separate fork and still carries the ADR-0010 rule (with ISS-0047's follow-up).
