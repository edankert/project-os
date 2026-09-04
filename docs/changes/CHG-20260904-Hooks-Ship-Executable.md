---
type: "[[change]]"
id: CHG-20260904-Hooks-Ship-Executable
title: "The hook scripts are recorded executable in git, the installer sets the bit on every install, and the harness asserts it"
status: merged
owner: user:edwin
created: 2026-09-04
updated: 2026-09-04
source: ["project-os-dev ISS-0055"]
commit: ""
pr: ""
impacts: ["tools/adapters/claude-code/hooks/", "tools/scripts/generate-adapters.py", "tools/scripts/test-hooks.sh", "tools/adapters/claude-code/ADAPTER.md"]
issues: []
features: []
related: ["[[INSTR-HOOKS]]", "[[CHG-20260903-Hooks-Serve-State]]"]
---

# The hooks ship executable

## Summary

The delegation hint failed on every prompt in every repo that had it, and the reason was a file permission. `.claude/settings.json` registers each hook by bare path with no interpreter in front, so a hook script without the executable bit produces `/bin/sh: .../model-routing-hint.sh: Permission denied` on each event it is registered for. Twelve repos were printing that instead of the hint.

The bit was never travelling with the file. This repo recorded all eight hook scripts as mode `100644` and sets `core.fileMode = false`, so a local `chmod +x` here was invisible to git and reached nobody. `sync-project-os.py` copies with `shutil.copy2`, which carries the source file's mode, and the source file's mode was `644`. The seven older hooks worked downstream only because `ADAPTER.md` gave `chmod +x .../hooks/*.sh` as an install step and someone ran it once — before `model-routing-hint.sh` existed. Every hook this template adds after an install has the same fate.

Three changes, so that the next new hook does not repeat it:

1. All eight hook scripts are now `100755` in this repo's index. A clone and a sync both carry the bit.
2. `generate-adapters.py --install-hooks` sets the executable bit on every file in `hooks/`, and does it on the path where an existing `hooks` key is left alone — which is the common case, a repo whose settings are already right and whose newest hook script is not. `SYNCING.md` step 5 already tells you to re-run that command after a sync, so the post-sync flow now repairs the bit on its own.
3. `test-hooks.sh` asserts every file in `hooks/` is executable, eight new assertions, 37 to 45. The harness could never have caught this before: it invokes each hook as `bash "$HOOKS/<name>"`, which runs a file whatever its mode.

`ADAPTER.md` drops the manual `chmod` line from the preferred install, since the installer does it, and says what to do in a repo with `core.fileMode = false`, where the bit you set is ignored by git and lost at the next clone.

## Impact

- **Downstream repos need the sync plus a generator run.** After `sync-project-os.sh`, the hook files arrive executable on disk. In a repo with `core.fileMode = false` git will not record that, so run `git update-index --chmod=+x tools/adapters/claude-code/hooks/*` once and commit, or the next clone is broken again.
- The delegation hint starts printing its line where it has been silent.
- Nothing about hook behaviour changes. No hook logic was touched.

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

The issue lives in project-os-dev (ISS-0055); the harness assertions extend project-os-dev TST-0007.

## Follow-ups

- [ ] Record the mode in each downstream repo's index; six of them carry all eight hooks as `100644` and are one clean clone from every hook failing.
