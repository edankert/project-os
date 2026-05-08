# project-os (template)

project-os is a reusable “project operating system”: a documentation system that is Obsidian-enabled (Obsidian optional) and can be maintained by an LLM and contributors.
Without Obsidian, the Markdown remains usable; Obsidian wiki-links (`[[...]]`) and `.base` files can be treated as plain text.

Start here:

- `AGENTS.md` (agent startup contract + docs-first gate)
- `LLM_BRIEF.md` (machine-oriented project brief)
- `CONTEXT.md` (LLM + contributor operating contract)
- `docs/INDEX.md` (primary docs index)
- `SNAPSHOT.yaml` (agent snapshot; canonical for LLMs)
- `tools/instructions/LIFECYCLE.md` (lifecycle rules)
- `tools/instructions/SYNCING.md` (how to sync template updates)
- `tools/skills/README.md` (playbooks)
- `tools/adapters/codex/ADAPTER.md` (Codex adapter model)
- `tools/agents/bootstrap.sh` (quick preflight/status)
- `tools/agents/start-change.sh` (docs-first intake scaffold)
- `tools/agents/check-docs-first.sh` (docs-first enforcement)
- `tools/cockpit/README.md` (optional browser cockpit for project-os docs)
- `docs/reference/README.md` (optional non-lifecycle reference/source area)
- `tools/skills/project-init/SKILL.md` (initialize for a new project)
- `tools/skills/project-derive/SKILL.md` (initialize from an existing project)

Scope notes:

- Copy the core template files into your repo root:
  - `docs/`, `tools/`, `SNAPSHOT.yaml`, `CONTEXT.md`, `AGENTS.md`, `LLM_BRIEF.md`
  - Optional (adopt or merge as needed): `SECURITY.md`, `ROADMAP.md`
  - If your repo already has a root `README.md`, keep yours and treat this file as template documentation.
- After copying, run `tools/skills/project-init/SKILL.md` and replace all `REPLACE ME` placeholders.
- To browse the docs locally, run `tools/cockpit/run.sh docs --bind 127.0.0.1 --port 8765`.
- Use the established lifecycle directories under `docs/` for structured project-os notes, and use `docs/reference/`, `docs/research/`, or another project-specific `docs/` subdirectory for durable source/evidence/publication material that should not become active tasks, requirements, or workflow state.
- In this upstream template repo, `docs/changes/CHG-*` records project-os template history. Downstream repos should remove those notes during init unless they intentionally want to keep upstream template history, then use `docs/changes/` for their own project history.

Suggested prompts (LLM/agent)

- New project init:
  - "Initialize project-os for a new project. Use tools/skills/project-init/SKILL.md, replace all REPLACE ME placeholders, and populate SNAPSHOT.yaml."
- Existing project derive/import:
  - "Enable project-os for this existing repo. Merge the project-os structure into the root, then follow tools/skills/project-derive/SKILL.md to derive issues/features/requirements/tasks/tests/changes/workflows from existing docs, trackers, changelogs, and tests. Capture provenance in source/Evidence and populate SNAPSHOT.yaml."
- Sync existing project-os with upstream template:
  - "Sync project-os template updates from the upstream project-os clone into this repo. Use tools/scripts/sync-project-os.sh <path-to-upstream> to update only template-owned files (tools/, including tools/cockpit/, docs/\_\_templates\_\_/, tools/instructions/, docs/README.md, docs/INDEX.md, CONTEXT.md; optional SECURITY/ROADMAP). Do NOT overwrite SNAPSHOT.yaml or project-owned docs (docs/features, docs/issues, docs/requirements, docs/tests, docs/changes, docs/decisions, docs/workflows, docs/reference, docs/research). After syncing, review changes and run tools/skills/snapshot-sync/SKILL.md."
- Validation:
  - "Run tools/skills/snapshot-sync/SKILL.md to reconcile note frontmatter and SNAPSHOT.yaml counters/relationships."

Sync helper (recommended)

- Use `tools/scripts/sync-project-os.sh` to pull template updates from an upstream project-os clone into a dev repo.
