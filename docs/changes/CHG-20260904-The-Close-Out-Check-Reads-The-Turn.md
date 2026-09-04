---
type: "[[change]]"
id: CHG-20260904-The-Close-Out-Check-Reads-The-Turn
title: "The close-out hook blocks only a stop that follows a write, so a parked focus item stops charging a forced continuation to every turn"
status: merged
owner: user:edwin
created: 2026-09-04
updated: 2026-09-04
source: ["project-os-dev ISS-0056"]
commit: ""
pr: ""
impacts: ["tools/adapters/claude-code/hooks/close-out-check.sh", "tools/adapters/claude-code/hooks/session-touch.sh", "tools/adapters/claude-code/hooks/lib/session-marker.sh", "tools/adapters/claude-code/hooks.json", "tools/instructions/HOOKS.md", "tools/adapters/claude-code/ADAPTER.md", "tools/scripts/test-hooks.sh"]
issues: []
features: []
related: ["[[INSTR-HOOKS]]", "[[CHG-20260903-Hooks-Serve-State]]", "[[CHG-20260904-Hooks-Ship-Executable]]"]
---

# The close-out check reads the turn, not just the snapshot

## Summary

Every turn in `your-trainer` ended with a forced continuation. `close-out-check.sh` blocked whenever `focus.task` was set, and that repo has had `focus.task: TASK-0783` set since 2026-08-15. The hook read two things — the `focus` block of `SNAPSHOT.yaml` and `stop_hook_active` — and nothing about the turn, so a session that answered a question was treated exactly like one that implemented the focus item. Three consecutive turns were blocked: two questions and one scaffolding turn, none of which touched the task.

`focus` is durable project state. It survives sessions, which is the point — it is how the next session knows where the work stands. The hook was reading it as if it described the turn.

Two halves, now with different strictness. The HC-007 validator still blocks **every** stop: a broken docs invariant is a failure, not a reminder. The focus half blocks only a stop that follows a write. `session-touch.sh`, a new `PostToolUse` hook on `Write|Edit|NotebookEdit`, records the session's first write as a zero-byte marker in the temp directory keyed by session and project; `close-out-check.sh` consumes that marker when it blocks. So the reminder arrives once per burst of work rather than once per turn, and a question costs nothing. Both scripts read the path from `hooks/lib/session-marker.sh` rather than each spelling it out, because two copies of a formula that must agree is the drift ISS-0048 spent twelve passes counting.

Every path that cannot answer "did this session write?" blocks, exactly as before: no `session_id` in the payload, no marker helper on disk. A check that silently disables itself when its input is missing is worse than one that nags.

## Impact

- **A repo with a legitimately parked focus item stops paying a forced continuation on every turn.** That was the reported cost and it is the whole point of the change.
- **Downstream repos need `--force-hooks`, not just a sync.** `session-touch.sh` is a new registration in `hooks.json`, and `--install-hooks` leaves an existing `hooks` key alone. Without the recorder the Stop hook finds no marker helper result and falls back to blocking every stop, which is the old behaviour — safe, but not the fix.
- **A session that edits through the shell rather than the editing tools is not reminded.** Only `Write`, `Edit` and `NotebookEdit` set the marker. Guessing which shell commands write would be a string match that ages badly. Recorded as the known limit in project-os-dev ISS-0056 rather than papered over.
- `test-hooks.sh` goes from 45 to 64 assertions. Nine cover the write test, including the two-repos-one-session case; one is the executable-bit check picking up the new hook file. Nine more are new: the disk check added for ISS-0055 was not enough, because a repo with `core.fileMode = false` records a new hook as `100644` whatever its mode on disk — which is how `session-touch.sh` was added `100644` an hour after that fix landed. The harness now also asserts the **index** mode of every tracked hook, and the same mutation confirms it fails. Three mutations were run against the new logic and each was killed: dropping the write test (3 failures), not consuming the marker (4), and failing open without a `session_id` (5).

## Documentation Coverage (All Types Considered)
Set each item to one of: `updated`, `new`, `not-applicable`, `deferred`.

- features: not-applicable
- requirements: not-applicable
- tasks: not-applicable
- issues: not-applicable
- tests: updated
- workflows: not-applicable
- decisions: not-applicable
- risks: not-applicable
- changes: new
- snapshot: not-applicable

The issue lives in project-os-dev (ISS-0056); the assertions extend project-os-dev TST-0007.

## Follow-ups

- [ ] Watch whether one reminder per burst of work is too few in a long implementation session; the marker is re-armed by the next write, so the frequency is now proportional to writing rather than to turns.
