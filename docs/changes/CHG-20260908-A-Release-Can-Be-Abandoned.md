---
type: "[[change]]"
id: CHG-20260908-A-Release-Can-Be-Abandoned
title: "A release that was prepared and will not ship gets a status of its own — `abandoned` joins the release vocabulary, so the note stays as the record of why a version number was skipped"
status: merged
owner: user:edwin
created: 2026-09-08
updated: 2026-09-08
source: ["project-os-cockpit FEAT-0145 — Edwin, 2026-09-08: 'Create Release (Update and delete release should also be possible)'"]
commit: ""
pr: ""
impacts: ["tools/instructions/STATUSES.md", "tools/scripts/validate-docs.py"]
issues: []
features: []
related: ["[[INSTR-STATUSES]]"]
---

# A release can be abandoned

## Summary

`abandoned` is now a legal status for a `[[release]]`. A release that was prepared and will not ship had nowhere to go: the vocabulary was `draft`, `released`, `reverted`, so a dropped release stayed `draft` forever and every count of what is in flight kept counting it.

The state already existed and had no word. `your-trainer`'s REL-0013 held v2.1.7 at `draft` for eleven weeks with `superseded_by:` naming its successor — and every reader had to work out from that link that the release was over.

## Why the note is kept rather than deleted

**A release that was prepared and abandoned is a fact about the project.** Deleting the file erases the only answer to *why was that version number skipped* — and the number stays taken, which is what makes the record worth having. `abandoned` is terminal: the transition is `draft → abandoned`, it requires a reason, and `superseded_by:` names the release that overtook it when one exists.

## What changed

- `tools/instructions/STATUSES.md`, `## [[release]]`: `abandoned` added to the allowed set, and `draft → abandoned` documented beside `draft → released` with the reason and the two obligations (a reason; `superseded_by:` when there is a successor).
- `tools/scripts/validate-docs.py`, `ALLOWED_STATUS["release"]`: the same value, with a comment recording the state that existed before the word did.

Nothing else moves. `released → reverted` is unchanged, and no existing note's status becomes invalid.

## Who has to do anything

**Nobody.** A repo that never abandons a release sees no difference. A downstream repo picks this up on its next `sync-project-os.sh`, and until then writing `abandoned` fails its local validator — which is the ordinary consequence of a template change and the reason this one lands here first.

Downstream note: a repo that carries the cockpit sidecar also carries `src/project_os_cockpit/validate_docs_bundled.py`, which is **not** covered by `sync-project-os.sh` (that script copies `tools/`). `project-os-cockpit` mirrors it there by hand; any other repo embedding the sidecar has the same obligation.

## Where it is used

`project-os-cockpit` [[FEAT-0145]] — `POST /api/notes/release-abandon`, and an **Abandon** control on the release page that takes a reason and keeps the note. That is what asked for the word.
