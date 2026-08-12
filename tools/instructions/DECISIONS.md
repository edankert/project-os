---
type: instruction
id: INSTR-DECISIONS
status: active
owner: group:maintainers
created: 2026-01-27
updated: 2026-01-27
tags: [instructions, decisions]
---

# Decision records (ADRs)

Use ADRs (`../../docs/decisions/ADR-####-*.md`) for durable decisions that affect multiple files/flows.

## When to create an ADR
- A convention/contract changes (schemas, status models, directory layout).
- There are real alternatives with tradeoffs.
- A choice impacts more than one workflow or team.

## How to record ADRs
1. Create the ADR note from `../../docs/__templates__/adr.md`.
2. Add/update the entry in `../../SNAPSHOT.yaml` under `items.decisions`.
3. Link the ADR to impacted items via `related`.

## Superseding
- If ADR B replaces ADR A:
  - ADR B sets `supersedes: [[ADR-A]]`
  - ADR A sets `superseded: [[ADR-B]]` and status becomes `superseded`

## A decision that is not a yes/no

Some ADRs propose an option and leave threads open inside their own consequences. Accepting one of those stamps every thread at once, which is how a decision sits `proposed` for months: the reader can see what they cannot answer.

**Give the note an `## Acceptance` section and put each open thread in it as a criterion.** They are then tickable one at a time, with evidence, through the same machinery a feature's criteria use — no new mechanism, and the unticked ones are the honest residue.

```markdown
## Acceptance

- [ ] **The read-only digest:** decided, or deferred with a home and a reason.
- [ ] **`Recent`:** kept in both surfaces or dropped from both. Say which.
```

**Accepting with a criterion still open is allowed.** A person may take a decision while a thread stands, and the record should show that rather than prevent it. Blocking the verb would trade an honest record for a tidy one.

Most ADRs are a genuine yes/no and need none of this. The section is available, not required.

## Recording why, not only what

Every human verb — accept, approve, decline, supersede, triage — may carry a **note**, and it is appended to the note being decided under a single `## Decision record` heading:

```markdown
## Decision record

> [!note] Accept — 2026-08-12 (user:edwin)
> Option 3, but consequence 3 needs the digest question settled first.
```

Three properties, each deliberate:

- **It is an Obsidian callout.** One syntax, two readers: Obsidian renders it natively and so does the cockpit. A tool-only marker would make the record legible in one place.
- **It appends.** A second decision adds a second callout; the first is never edited. A decision record that can be rewritten is not one.
- **The prose is quoted line by line**, so a note containing `---`, a heading, or its own callout cannot alter the file it lands in.

Without this a project can record *that* a human decided and never *why* — measured in one repo across six write paths, exactly one carried the person's own words, and only onto a checkbox.

## A decision that offers options

If the decision is a choice between paths, put them under `## Options` so a person can be offered them and their answer can be recorded. **Either form**, both readable:

```markdown
## Options

1. **Deprecate mode 1.** Honest about where the effort goes; loses the tablet reader.
2. **Full parity.** Requires the write endpoints on a LAN-reachable surface. Refused: …
3. **Mode 1 is the reading surface.** Every view that answers a question without …
```

```markdown
## Options

### 1. The human publishes, on cadence (status quo)

The worker commits; a person pushes when they look…
```

Then **name the one you propose in the `## Decision` section** — "Option 3" — so a surface can default to it rather than guessing.

**This is checked.** `DECISION-OPTIONS` is an error when an `## Options` section yields fewer than two readable options, or when they do not number `1..N`. That is deliberate: a control can only offer what a document declares, and a convention nobody validates drifts per author until the control silently stops appearing. It is an error rather than a dated warning because the convention is new and there is no debt to grandfather (ADR-0011).

Recording a choice writes `decided_option:` in the frontmatter and names it in the decision-record callout. **Accepting without choosing stays legal** — a decision may be taken as proposed, and demanding a choice would turn an offer into a gate.
