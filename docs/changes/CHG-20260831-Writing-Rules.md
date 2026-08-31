---
type: "[[change]]"
id: CHG-20260831-Writing-Rules
title: "Agents now have a rule for writing prose a reader can follow, not just prose that is correctly formatted"
status: merged
owner: user:edwin
created: 2026-08-31
updated: 2026-08-31
source: ["Edwin, 2026-08-31, reporting feedback from more than one reader: the writing is 'at a very high level of abstraction, which makes it very difficult to understand'"]
commit: ""
pr: ""
impacts: ["tools/instructions/WRITING.md (new)", "AGENTS.md startup step 6", "CLAUDE.md reference list", "docs/STYLEGUIDE.md"]
issues: []
features: []
related: ["[[INSTR-MARKDOWN]]"]
---

# Writing rules, added

## Summary

The template told agents how to **format** Markdown and never told them how to **write** it. `MARKDOWN.md` covers line wrapping and formatter settings. Nothing covered whether a human could follow the result, and the result had drifted a long way from readable.

A maintainer reported it on 2026-08-31, and said other readers had said the same: the prose sits "at a very high level of abstraction, which makes it very difficult to understand".

The diagnosis is that the failure mode is compression, not length. Real examples from one repo's commit log:

- "Two walker-facing fixes, guarded behaviourally rather than by grep" — a seven-word title carrying three terms invented for that project.
- "The platform scoping stops at the derived view" — nothing in the sentence is something a reader can point at.
- "Discriminating, not merely red" — a heading that only parses for someone who already knows the point.

## What changed

`tools/instructions/WRITING.md` is new and template-owned, so it reaches every repo through the normal sync. It carries six rules: point first, one idea per sentence, concrete subject with a real verb, gloss invented terms on first use, name what the reader sees before the code symbol, and no slogans as headings. It includes a before-and-after table and a three-question self-check.

`AGENTS.md` gains a sixth mandatory startup step pointing at it, beside the existing `MARKDOWN.md` step. Each repo's `CLAUDE.md` gains a line in its reference list; `CLAUDE.md` is project-owned, so that line was added by hand in each repo rather than synced.

## Impact

Applies to chat replies, commit messages, and the prose inside notes. It does not change any schema, validator, or script, so nothing fails if it is ignored — it is guidance, enforced by review rather than by the build.

## Not done

Cursor reads these instructions through generated rule files, and wiring `WRITING.md` in means editing `tools/scripts/generate-adapters.py` and regenerating `.cursor/rules/` everywhere. Several repos are behind on that generator, so doing it now would pull unrelated changes into them. Deferred to the next full template sync, and filed downstream as `project-os-cockpit ISS-0273`.
