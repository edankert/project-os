---
type: reference
id: LEDGERS-README
status: active
owner: group:maintainers
created: 2026-09-18
updated: 2026-10-21
tags: [releases, acceptance]
---

# Acceptance ledgers

This folder records the result of each acceptance check tested in a release test. A result is not written on the test note. It is a dated line in a JSON file here, saying who tested which check, on which platform, with what outcome (ADR-0037). The outcomes and what each one means are in `tools/instructions/TAXONOMY.md`, "Acceptance outcomes (the ledger's vocabulary)".

## The files

| file | what it is |
| --- | --- |
| `WORKING-<platform>.json` | The open ledger, one per platform. Every new result is added here. |
| `REL-####-<platform>.json` | A sealed ledger: the results a release was checked against. It is never edited. |

The platform is the surface a result was earned on. A project that is one application everywhere can use a single `WORKING-app.json`. Add a ledger per operating system only for checks that really differ between them: a check with no result on a platform counts as owed there.

## One file, by example

```json
{
  "platform": "app",
  "entries": [
    {"check": "TST-0001", "result": "pass", "date": "2026-09-18", "method": "manual", "by": "user:you"},
    {"check": "TST-0002", "result": "fail", "date": "2026-09-18", "method": "manual", "by": "user:you", "reason": "The save button stays grey after typing a name."}
  ]
}
```

An entry written before 2026-09-27 stores its result under `mark` instead of `result`. Every reader accepts both, and a sealed ledger is never rewritten to change it (project-os-dev ADR-0050).

Every outcome except `pass` needs a `reason`. To withdraw a result after the code changes, add an entry with `invalidated_by:` naming the change note, rather than deleting the line.

`method` says how a result arrived. It is `manual` when a person recorded it, `automated` or `migration` when a tool did, and `ride` when an app recorded it while a person ran the release test in it. `release-test.py --import-ride` writes the `ride` entries, and each one names the `build` it was earned on, such as `"2.2.0 (123)"`. The import copies the ride's evidence files into `evidence/<release>-<platform>-<started>/` in this folder. The ledger's `evidence` list names each file, with the `check` and `date` of its entry, the file's path as `ref` and the step it backs as `note`. The formats are in `docs/__templates__/SCHEMAS.md`, "The ride script and its results".

## What the validator does with them

Once this folder holds a `.json` file:
- each entry is checked for its fields, its date and its outcome word (the `LEDGER-*` codes);
- a test note may no longer carry `mark:` or the other verdict fields that moved here (`LEDGER-FIELD`);
- a finished feature's acceptance checks count as tested when a ledger clears them on at least one platform (`VERIFY-ACCEPTANCE`).

`tools/scripts/release-test.py` reads the same files to list what is still owed for a release.
