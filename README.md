# project-os (template)

project-os is a reusable “project operating system”: a documentation system that is Obsidian-enabled (Obsidian optional) and can be maintained by an LLM and contributors.
Without Obsidian, the Markdown remains usable; Obsidian wiki-links (`[[...]]`) and `.base` files can be treated as plain text.

Start here:
- `CONTEXT.md` (LLM + contributor operating contract)
- `docs/INDEX.md` (primary docs index)
- `SNAPSHOT.yaml` (agent snapshot; canonical for LLMs)
- `tools/instructions/LIFECYCLE.md` (lifecycle rules)
- `tools/instructions/SYNCING.md` (how to sync template updates)
- `tools/skills/README.md` (playbooks)
- `tools/skills/project-init/SKILL.md` (initialize for a new project)
- `tools/skills/project-derive/SKILL.md` (initialize from an existing project)

Scope notes:
- Copy the core template files into your repo root:
  - `docs/`, `tools/`, `SNAPSHOT.yaml`, `CONTEXT.md`
  - Optional (adopt or merge as needed): `SECURITY.md`, `ROADMAP.md`
  - If your repo already has a root `README.md`, keep yours and treat this file as template documentation.
- After copying, run `tools/skills/project-init/SKILL.md` and replace all `REPLACE ME` placeholders.

Suggested prompts (LLM/agent)
- New project init:
  - "Initialize project-os for a new project. Use tools/skills/project-init/SKILL.md, replace all REPLACE ME placeholders, and populate SNAPSHOT.yaml."
- Existing project derive/import:
  - "Enable project-os for this existing repo. Merge the project-os structure into the root, then follow tools/skills/project-derive/SKILL.md to derive issues/features/requirements/tasks/tests/changes/workflows from existing docs, trackers, changelogs, and tests. Capture provenance in source/Evidence and populate SNAPSHOT.yaml."
- Sync existing project-os with upstream template:
  - "Sync project-os template updates from the upstream project-os clone into this repo. Use tools/scripts/sync-project-os.sh <path-to-upstream> to update only template-owned files (tools/, docs/__templates__/, tools/instructions/, docs/README.md, docs/INDEX.md, CONTEXT.md; optional SECURITY/ROADMAP). Do NOT overwrite SNAPSHOT.yaml or project-owned docs (features/issues/requirements/tests/changes/decisions/workflows). After syncing, review changes and run tools/skills/snapshot-sync/SKILL.md."
- Validation:
  - "Run tools/skills/snapshot-sync/SKILL.md to reconcile note frontmatter and SNAPSHOT.yaml counters/relationships."

Sync helper (recommended)
- Use `tools/scripts/sync-project-os.sh` to pull template updates from an upstream project-os clone into a dev repo.
