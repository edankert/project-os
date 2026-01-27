# project-os (template)

project-os is a reusable “project operating system”: a documentation system that is Obsidian-enabled (Obsidian optional) and can be maintained by an LLM and contributors.
Without Obsidian, the Markdown remains usable; Obsidian wiki-links (`[[...]]`) and `.base` files can be treated as plain text.

Start here:
- `CONTEXT.md` (LLM + contributor operating contract)
- `docs/INDEX.md` (primary docs index)
- `SNAPSHOT.yaml` (agent snapshot; canonical for LLMs)
- `tools/instructions/LIFECYCLE.md` (lifecycle rules)
- `tools/skills/README.md` (playbooks)
- `tools/skills/project-init/SKILL.md` (initialize for a new project)

Scope notes:
- Copy the core template files into your repo root:
  - `docs/`, `tools/`, `SNAPSHOT.yaml`, `CONTEXT.md`
  - Optional (adopt or merge as needed): `SECURITY.md`, `ROADMAP.md`
  - If your repo already has a root `README.md`, keep yours and treat this file as template documentation.
- After copying, run `tools/skills/project-init/SKILL.md` and replace all `REPLACE ME` placeholders.
