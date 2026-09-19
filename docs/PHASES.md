# Phase Registry

This document explains how the project's phases work, and keeps the history of why each phase was planned. **Each phase's status lives in its own note under `docs/phases/`, and only there.** Do not keep a table of phases and statuses here once those notes exist: a hand-kept copy drifts from the notes (ADR-0009; project-os-dev ISS-0072 found one showing a finished phase as planned).

## How Phases Work

- **Property**: `phase` (`[[PHASE-####]]` link preferred; integer 1–N accepted for simple projects or migration)
- **Location**: YAML frontmatter of features, tasks, requirements, and issues
- **Purpose**: Groups related work into cohesive delivery milestones
- **Detailed notes**: `docs/phases/PHASE-####-Short-Name.md` when a phase needs scope, linked work, and exit criteria

## Phase Definitions

A phase is a `[[phase]]` note, `docs/phases/PHASE-####-Short-Name.md`, created from `docs/__templates__/phase.md`. Its status, scope, linked work and exit criteria are written there. To see all phases and their statuses, list `docs/phases/` or open the cockpit.

A small project with no phase notes may instead list its phases here, as a table of number, name and description, with no status column. It moves to phase notes as soon as one phase needs a status or exit criteria, and deletes the table in the same commit.

Use `tools/skills/phase-planning/SKILL.md` when creating or migrating first-class phase notes.

## Usage

### In Frontmatter

```yaml
---
type: "[[task]]"
id: TASK-0042
phase: "[[PHASE-0002]]"
status: doing
parent: "[[FEAT-0015]]"
---
```

### Filtering by Phase

Use the `phase` property in Obsidian bases or queries to:
- Group items by delivery milestone
- Track progress within a phase
- Identify scope creep (items without phases)

Use `order` on `[[phase]]` notes to preserve numeric roadmap sorting without overloading the `phase` relationship field.

### Phase Inheritance

- **Features** define the phase for a body of work
- **Tasks** inherit phase from their parent feature (or override explicitly)
- **Requirements** and **Issues** can specify phase when relevant to milestone planning

## Operational Rules for LLMs

The phase-alignment rules are stated once in `tools/instructions/LIFECYCLE.md`, "Phase alignment (optional gating)": verify the phase before starting, consult this registry, do not build a later phase's work early, and a task that needs a future-phase dependency is the user's decision (`tools/instructions/LIFECYCLE.md`, "When to pause for the user").

## Phase Progression

Phases are generally sequential but may overlap:
- **Active phase**: Primary focus of current development
- **Maintenance phases**: Earlier phases may receive bug fixes
- **Blocked phases**: Future phases awaiting dependencies

Track the current active phase in `SNAPSHOT.yaml` under `focus.phase` (`PHASE-*` ID preferred).

---

*This file is part of the Project OS documentation system. See [docs/README.md](README.md) for overview.*
