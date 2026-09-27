---
type: instruction
id: INSTR-TESTING
status: active
owner: group:maintainers
created: 2026-03-16
updated: 2026-09-27
tags: [instructions, testing]
---

# Acceptance test rules

The three kinds of acceptance test, their lifecycle, and release gating. There is no tier system: a check's test kind is derived from what it covers and who executes it.

## The three test kinds

A check is not filed into a test kind. Its test kind is computed from two fields it carries: `covers:` says what it is about, `command:` says who executes it (ADR-0034). **Precedence:** a non-empty `command:` makes it an automated test; otherwise a `covers:` naming an `ISS-*` makes it a regression test; otherwise it is a feature test.

### Feature tests — re-checked when behaviour changes
- Asserts *the system does X*, a standing claim about current behaviour; `covers:` names a `FEAT-*`.
- Never removed, and **invalidated when a change overlaps its scope**. The only test kind that is.

### Regression tests — completed once
- Asserts *this defect was fixed*, a claim about a past event; `covers:` names the `ISS-*`.
- Discharged once, by a person completing it or by a `command:` that makes it automated. A later change does not re-open it: nothing a change does can falsify a claim about the past. Without the `ISS-*` link it is read as a feature test.

### Automated tests — executed by CI
- Carries a non-empty `command:`; it is here because a machine executes it, and leaves when the command is removed.
- **Carries no verdict** (`STATUSES.md` `[[test]]`); a red run is a red build.

## Lifecycle rules

### When to create
1. **New feature implemented**: a feature test on the user-visible behaviour, naming the `FEAT-*` in `covers:`.
2. **Bug fixed**: a regression test that reproduces the bug and verifies the fix, naming the `ISS-*` in `covers:`.
3. **A check a machine can execute**: give it a `command:`. That is the whole of automating it; nothing is moved or re-filed.

### When to invalidate (mark for re-check)
- Feature tests only, and only those whose scope the change overlaps: a change to `WorkoutViewModel` invalidates workout checks, not Bluetooth checks.
- **Say which change did it, in the same action**: the invalidation is a dated event in the release ledger naming the check and the change (`TAXONOMY.md`, "Acceptance outcomes (the ledger's vocabulary)"), and it is refused without a change id; no field on the note records it (ADR-0037). Reason: clearing a tick otherwise destroys the only record the check ever passed, and the re-check never happens (measured in project-os CHG-20260903-Instruction-Weight).
- Best done at the close-out of the work that caused it, as one sweep over the areas touched.
- A regression test is not invalidated by a later change; a returned defect files a new issue.
- **A regression test that also states current behaviour is split when a change overlaps it** (project-os-dev ISS-0069, Edwin, 2026-09-18). A regression test's claim should be only that the defect stays fixed. If it also asserts how the product behaves now, a change to that behaviour leaves it ticked though it no longer holds. At the close-out sweep, split it: the regression test keeps only the defect's own assertion, and a new feature test, with `covers:` naming the `FEAT-*`, carries the behaviour, and is invalidated like any other.

### When to remove
- **Nothing removes a check.** A check whose subject is gone goes `retired`; one a machine now covers gets a `command:`. Reason: a deleted check cannot report that its covering test was renamed.

### Unit test replacement
- When unit tests cover a check's logic, give the check their `command:`. If it later stops resolving, the check reports itself as broken and returns to the manual list.

## Where the acceptance suite lives

A repo stores its suite one of two ways, never both.

**Notes (current).** One check per note: `type: [[test]]`, `level: acceptance`, id `TST-*`, stored per `LIFECYCLE.md` "Test storage", from `../../docs/__templates__/test.md`. A check a person tests by hand lives under `docs/tests/acceptance/`, where the release test and the cockpit both look for it; an automated check, one with a `command:`, may sit beside its feature (project-os-dev ISS-0063). `status:` is the lifecycle (`draft`/`active`/`retired`); the verdict is not on the note (`STATUSES.md` `[[test]]`). The test kind is derived and never written down. See `SCHEMAS.md` `test.md` ("Acceptance fields") and `STATUSES.md` `[[test]]`.

**One document (older).** `docs/tests/ACCEPTANCE_TESTS.md`, from `../../docs/__templates__/acceptance-tests.md`: `# Feature tests`, `# Regression tests` and `# Automated tests`, grouped by area, one `- [x] **Test Name:** procedure and expected result` row per check (automated rows have no checkbox). Everything in this file applies to it. A repo that migrates to notes deletes the document in the migration commit, because two records of one thing drift and git holds the old one.

### A check is testable by a stranger

A check is written by someone holding the whole context and tested months later by someone holding none of it. So an acceptance check states four things, under four headings, and a new one is born with them in `../../docs/__templates__/test.md` (project-os-dev ADR-0027):

- **Setup** — the state the test needs, and *the cheapest way to reach it*. Name the developer toggle, the mock or the bundled fixture that produces it. This is the line that decides whether the check ever gets tested: one check went untested for months because its setup sentence asked for hardware to be unplugged, and a developer-settings switch forces the same state in fifteen seconds.
- **Steps** — numbered, one action each, in the order a person performs them.
- **Expect** — what must be observable, one line per assertion, in the words the surface uses. A code symbol may follow the observable name; it may not replace it. **Where the result differs by platform, write one line per platform**, starting with the platform's name in square brackets: `- [android] The Hub opens from the equipment icons.` and `- [ios] The Hub opens from Settings.` A line with no platform name holds on every platform. The release test prints only the lines that hold on the platform being tested, without the brackets, and refuses a platform name the repo keeps no ledger for, naming the check and the line. This is the only place a check's expected result is written: a procedure gives its tags and never its own copy (project-os-dev ADR-0050 D2, REQ-0034).
- **Not this check** — the boundary: what a reader might reasonably think this covers, and which check actually covers it.

Provenance — where the check came from, what migration moved it, which audit split it out — goes **below** the procedure under its own heading, or into frontmatter. It is about the note, not about the release test.

**Existing checks are rewritten on contact, never swept.** A check is brought to this shape when it is tested, invalidated, or otherwise edited. Rewriting a whole corpus from note text alone manufactures confident assertions nobody verified; the release test is when a person knows whether the text is true. A check missing its Setup heading prints "Setup: not stated" on the release test sheet ("The release test", rule 5), which is where a corpus comes into contact.

## Test adequacy (who verifies the tests?)

A guarding test that cannot fail does not guard, and LLM-authored tests share the blind spots of the LLM-authored fix. Every regression test, and any `TST-*` gating a terminal status, carries adequacy evidence in its note:

- **Minimum bar:** show the test fails when the fix is reverted or broken, in the note's Adequacy section or `adequacy:` field.
- **Stronger bar (when tooling exists):** mutation testing over the guarded code, score in `mutation_score:`, tool and command in the evidence (`mutmut`, Stryker, `cargo-mutants`, PIT, `muter` by stack).
- **Independence:** a test created alongside the fix it guards gets an independent review (`../skills/independent-review/SKILL.md`).
- **Cadence:** mutation scores consistently above about 80% justify checking less often; below that, check every guarded fix.

## Release gating

- A release is **blocked** while any manual check is unsettled.
- An automated test never enters the manual list; CI gates it. A **broken command** returns its check to the manual list, because nothing is verifying it.
- A check that cannot be completed (a third-party key unavailable, for example) may be a **release exception**, documented in the release note with justification.

## The release test

A release is tested by hand from a **release test sheet**. It is one generated document per release and platform. It opens with the screens the release changed, then lists every owed check in the order to test them, with each check's setup, steps and expected result printed on the page. Nobody writes it by hand: `python3 tools/scripts/release-test.py --release REL-#### --platform <platform>` prints it from the release ledger, the check notes and the project's section order. To **test** a check here is to execute it by hand.

Six more words, used on the sheet and below:

- **section** — a group of checks that share one setup state, such as one build, one account tier, or one piece of hardware on the bench. They are tested in one go.
- **what changed** — the sheet's first part: the screens this release changed, and what changed on each.
- **section order** — `docs/tests/acceptance/RELEASE-TEST.md`, one file per project, authored by the person who knows the product. It lists the sections in product-state order. Its shape is `../../docs/__templates__/release-test.md` and its keys are in `SCHEMAS.md`, "`release-test.md` — the section order (`RELEASE-TEST.md`)".
- **tester** — the person doing the release test.
- **result** — what the tester records for a check: pass, fail, partial, question, blocked, N/A or excused (`TAXONOMY.md`, "Acceptance outcomes (the ledger's vocabulary)").
- **procedure** — a written script for one whole section: the setup stated once, then numbered steps. One file per section, under `docs/tests/acceptance/release-test/`. Rule 9.

Two words that rule 9 uses:

- **owed part** — the unit a procedure is counted against: one numbered step of a check this platform still owes. A check whose steps are not numbered is one part.
- **expectation tag** — a label such as `TST-0648.4` on a line of a procedure step, saying that the line satisfies step 4 of check TST-0648.

Nine rules. They are stated here and nowhere else; the template, the generator, the skills and the cockpit link to this section and restate none of it (project-os-dev ADR-0029, ADR-0045 as amended by ADR-0046, ADR-0024; the names are project-os-dev ADR-0050's).

**1. The sheet is derived, never stored.** Its rows are exactly the checks the ledger says this platform still owes, restricted to the two manual test kinds, feature and regression ("The three test kinds"). No second list of "the checks for this release" exists anywhere. A generated sheet may be committed as a record of what was tested; it is never edited by hand and never read back by tooling. Reason: a maintained list of what a release owes rots, and a computed one cannot.

**2. What changed comes first, and it is built from the change notes.** Before any scripted check, the tester is told which screens this release changed. That list is computed: take every change note added since the last release tag, read its `## Impact` list, and group the `SUR-*` ids those lines name. Under each screen the list prints the one sentence each change wrote for it, and the picture of the screen at the last release tag beside the picture of the build being tested. A child surface — one whose note carries `parent:` — prints under its top-level screen: its parent, or for a screen nested deeper, the screen at the top of its `parent:` chain. It does so even when only the child has a change note. In that case the top-level screen is named to show where to open the child; it does not claim that screen changed. **What changed names no check and prints no `TST-` id**: it is a list of places to open and look at, not a list of things to run.

Where the pictures are: `docs/tests/acceptance/gallery/<tag>/<key>.<ext>` holds the screens as they were at the release tagged `<tag>`, and `docs/tests/acceptance/gallery/candidate/<key>.<ext>` holds the build being tested. `<key>` is one of the keys on the surface note's `gallery:` list (`TAXONOMY.md`, "`gallery` (surfaces)"), and `gallery:` in RELEASE-TEST.md is the command that regenerates them. A screen with an after picture and no before one is marked **new**. A screen with neither prints its sentence alone.

Without a reachable release tag — a shallow clone, or a project that has released nothing yet — the what-changed list says so in one line, and the rest of the sheet still prints. It never prints an empty list silently.

The list reads what git says was **added** since the tag, so an uncommitted change note is not in it, and neither is an Impact list back-filled onto a note that already existed at the tag. `release-test.py --check` reads every change note in the repo whatever the tag says, which is where a missing Impact list is reported.

Reason: looking at what changed is the first thing a person would do. This rule read the ledger's invalidation events until 2026-09-14, and an invalidation names a check, never a screen — so the list showed test categories such as "Hardware", which spans five screens, and a change that altered a screen without reopening a check was invisible (project-os-dev ADR-0045 decision 1, amending ADR-0029 rule 2).

**3. The order is authored once, in RELEASE-TEST.md, and never inferred.** Sections appear on the sheet in the order the file lists them. A check joins the first section whose `surfaces:` names its `area:`; a section may also name check ids in `checks:` to pull them in regardless of area. A section with nothing owed is omitted. Checks no section claims go to a final section labelled "Unplaced", which is the author's worklist. A project with no RELEASE-TEST.md gets one section per area in id order, and the sheet says its order is unauthored. Reason: the one previous attempt to order a release test read setup cost out of prose and produced six false positives out of six.

**4. Inside a section, `after:` first, then id.** An acceptance check may carry `after: [TST-####]`, the checks that should have passed before this one is tested. The sheet sorts by it. Nothing gates on it, and a cycle prints a warning naming the checks rather than failing the sheet.

**5. Each row can be tested without leaving the sheet.** A row prints the check's id, its title, and its Setup, Steps and Expect sections ("A check is testable by a stranger"). This is what a section with no procedure prints; a section that has one prints that instead (rule 9). Where a heading is missing the row says so and prints what the note does have, so the sheet doubles as the worklist for bringing old checks to that shape:

- no `## Setup` prints **"Setup: not stated"**. There is no fallback, and that is the point of the label.
- no `## Steps` falls back to `## Procedure`, and then to the note's own unheaded description — the prose between its title and its first sub-heading — printed under **"Steps: no heading"**. A corpus written before these headings existed keeps its whole procedure there, so printing nothing would make the sheet useless on the repos large enough to need it.
- only the Expect lines that hold on this platform print ("A check is testable by a stranger"). No `## Expect` falls back to `## Expected results`, and then says the note states no expected result. There is no prose fallback: a check that never said what should happen has nothing to fall back to, which is the finding, not the sheet's failure.

An unscripted acceptance check may declare `readiness_for:` in its frontmatter, the same key a procedure uses. On a check, the map names a platform and gives `kind: preparation` or `kind: decision`, a plain `reason`, and an optional `issue`. The generated fallback row prints that reason before the check's instructions. The declaration does not change which platforms owe the check or record a result. The cockpit asks for preparation to be confirmed before it offers the normal result control; a decision row offers only the existing release-decision outcomes. The generator rejects malformed declarations.

**6. A result goes to the ledger, from the sheet.** The sheet is never the store. A tester records each result as a ledger event through the cockpit's result dialog or the ledger write path, with `method: manual`. A new entry stores it under the key `result`. An entry written before 2026-09-27 stores it under `mark`, and every reader accepts both for good, because a sealed ledger is never rewritten (project-os-dev ADR-0050).

**7. One implementation.** `tools/scripts/release-test.py` is the only code that computes a release test. The cockpit bundles that module the way it bundles the validator, so a badge and a sheet cannot disagree about one corpus.

**8. No schedule, and no new obligation.** The generator writes no duration of its own: counts of rows are the only number it produces, and there is no minutes field, no estimate and no burden tag anywhere in the release test. Text it quotes from a note prints verbatim, so a check whose own title says "a 40-minute ride" still reads that way on the sheet — that is the author's sentence, not a schedule the generator invented. And the release test asks one thing at close-out, and one only: **a change note's `## Impact` list names the screens that change altered**, one sentence each, drafted by an LLM from the diff. That single obligation buys the what-changed list its only input, which is written down nowhere else — measured on the corpus that has the problem (ADR-0045 decision 2, narrowing this rule). Nothing else is added: no sweep over the suite, no per-release run plan, no duration. Reason: both are ways an earlier attempt died. Ordering by inferred setup cost was cancelled for inventing a schedule out of prose, and a close-out acceptance sweep was withdrawn because its common case was "nothing to do, say so".

**9. A section may be tested from a written procedure.** A procedure is a script for one whole section: the setup stated once, then numbered steps. It removes repetition that per-check rows cannot — on your-trainer's REL-0017 sheet the same "fake a connected trainer" setup printed four times inside one section, and the same comparison against a drivable trainer printed in four checks. Where a section has a procedure the sheet prints it; where it has none the sheet prints rows, exactly as rule 5 says.

- **Where it lives.** One file per section, `docs/tests/acceptance/release-test/<name>.md`, from `../../docs/__templates__/procedure.md`. Its `section:` field repeats the `### ` heading in RELEASE-TEST.md word for word, and that is the whole of the link: nothing in RELEASE-TEST.md points back, because a pointer written in two files is a pointer that can disagree. A procedure is written once for the whole product, not once per release, and it aims to cover every live check in its section.
- **What a step is.** One numbered item under `## Steps`. Its first line names the screen the step happens on, by `SUR-####` id or by the surface's exact title. Under that line, one line per thing the tester should observe. **A step's number is its position in the list, not the digit written** — markdown renumbers an ordered list and so does the generator, so a procedure written `1.` on every item has steps 1, 2, 3, and that is what a tag names and what the sheet prints. A tag inside a fenced block is an example, not a citation.
- **What an expectation line is.** Its tags alone, `` - `TST-0480.1` ``. The sheet and the cockpit print the check's current Expect text in its place: of the Expect lines that hold on the platform being tested, line N for `.N` when there is exactly one such line per numbered step, otherwise every one of them. So rewording a check changes what the next sheet prints and breaks nothing (project-os-dev ADR-0049, ADR-0050 D2). A tick recorded from a procedure step stands as a result on the check itself only because the tester read the check's own words (project-os-cockpit ADR-0041). **A quoted line, the older form, is reported as a warning**: a line that quotes one line of the check's `## Expect` followed by its tags, or an action line that carries tags. `release-test.py --check` lists each one, and under `--quiet` prints how many there are. It becomes an error once the consumers have moved to tags alone (`QUOTED_EXPECTATIONS_REFUSED` in `release-test.py`), and then such a procedure is refused. Until then a quoted line is still compared against the note's lines for the platform, and only whitespace may differ (project-os-dev ISS-0066). `python3 tools/scripts/release-test-tags.py --all --apply` rewrites every quoted line as its tags and moves tags off action lines; without `--all` it rewrites only the lines whose tags print exactly the quoted words on every platform the step runs on, and `--refresh` re-quotes a line whose check was reworded.
- **What a tag is.** `TST-####.N`, in backticks, meaning the line satisfies step N of that check: `` `TST-0648.4` ``. ASCII only. A check whose steps are not numbered is cited by its bare id, `` `TST-0648` ``. A line may carry several tags where several checks expect the same thing in the same words.
- **What an owed part is.** One numbered item under a check's `## Steps` (or `## Procedure` where `Steps` is absent), for a check the ledger says this platform still owes, counted by position for the same reason. A check with no numbered steps is one part. Renumbering a check's steps changes what its parts are, and the validator then reports the procedure as no longer covering them; the fix is to regenerate it (`../skills/release-test-procedure/SKILL.md`). An agent writing a section's procedure numbers a prose-only check's steps in the check note first, and that check then has one part per step.
- **What is checked.** `python3 tools/scripts/release-test.py --check --platform <platform>` fails, naming the check and the step, when an owed part is cited by no step, when an owed part is cited by two different steps, when a backticked `TST-` token is malformed, when a tag names a check at `status: retired`, when a tag names a step number the check does not have, when a tag names a check that another section claims, or when a quoted expectation does not match the check's `## Expect` text (a tag-only line has no quote to mismatch). A valid tag on the same line does not excuse a malformed one. It also fails a procedure whose declarations contradict each other: one step or setup id declared twice in the same map, where the parser would keep one instruction and drop the other; a setup item limited to platforms none of its steps runs on; a `readiness_for` or `action_for` platform on a step that does not run there; or a platform name the repo keeps no ledger for. Whether two steps' prose disagrees is for the author to settle, or to mark with `readiness_for: {kind: decision}`; the generator does not read prose (ADR-0046). Covering the owed parts is the requirement; covering every live check is the aim, and the shortfall is reported as a count rather than failed. `validate-docs.sh` runs it for every platform that has a ledger.
- **Declared preparation.** A procedure may add `requires:` in frontmatter, mapping a step's position to earlier step positions it needs. The generator keeps those prerequisite actions transitively and in authored order when a later step is owed. A prerequisite whose own checks have passed is labelled preparation and creates no result. An absent, future or cyclic reference fails validation and the section falls back to its per-check rows. No dependency is inferred from action prose.
- **Scoped setup.** A procedure may name each `## Setup` bullet as `- [trainer] Connect the trainer.` and map each id to step positions in frontmatter `setup_for:`. A value of `all` means every step; a list such as `[1, 5]` names only those positions. Only items needed by retained steps and their prerequisites print. `setup_platforms:` may limit an item to named platforms. Unannotated procedures keep their full setup. An item with an invalid id, step or platform declaration fails validation. Resolve conflicting setup and section state in the authored notes; the generator cannot guess which instruction is right.
- **Platform and state.** `step_platforms:` maps step positions to platform lists such as `[android]` or `[ios]`. `state_for:` maps step positions to a plain statement of the app and equipment state to confirm before that action. The declaration continues through later steps on that platform until another declaration replaces it, including when the declaring step is omitted from the current owed release test. A step unavailable on the selected platform cannot change that platform's state reminder. A platform's release test keeps only its applicable steps and checks their owed coverage. A step may depend only on an action available on that platform. Required state is an instruction, not proof that the live app is in that state.
- **Platform action wording.** `action_for:` maps a step position to platform-specific action prose, for example `3: {android: "Open Profile — Connected.", ios: "Open Settings — Integrations."}`. The variant replaces only that step's action after its unchanged bold surface heading; it may not contain a test tag. The validator rejects a variant on a step without a bold surface heading or with tags on its first line. The check's exact expectation lines and owed coverage remain unchanged.
- **Later comparisons and waits.** `capture_for:` maps an earlier step position to the evidence to record there, and `use_capture:` maps a later step position to earlier evidence source positions. The later step must also name each source in `requires:`. The prompt appears only when the later comparison survives filtering. `timer_for:` maps a step position to a positive duration in seconds for an optional user-started timer. Neither capturing evidence nor ending a timer records a result. Missing, future or undeclared evidence sources fail validation.
- **Known readiness problems.** `readiness_for:` maps a step position to `{kind: preparation, reason: "...", issue: "ISS-..."}` or `{kind: decision, reason: "..."}`. An optional `platforms: [android]` limits the problem to the named platforms. Use it for a concrete missing fixture, device, developer control or unresolved product decision. The generator prints the reason before the affected action and the cockpit can list it in the session introduction. This label creates no result and never drops the step or its owed checks. An absent step or malformed declaration fails validation.
- **What prints.** For a section with a procedure the sheet prints relevant setup once, then each owed step and its declared prerequisites, and says how many steps it left out. Each step prints under its number in the procedure, so the procedure's own references, such as "for step 21", still point at it; the numbers skip where steps are left out, and the sheet says so. The cockpit shows the same number and counts progress separately (project-os-dev ISS-0086). A settled expectation in a retained preparation action does not print or create a result. A tag on an owed step whose part is not owed is marked as already passed. A procedure the validator refuses prints that message at the top of its section and then per-check rows, so a stale procedure never hides an owed check.

**The old names are refused.** Until 2026-09-27 this was called the walk: a section was a sitting, what changed was the survey, and the section order lived in `WALK.md` (project-os-dev ADR-0050). A repo that still uses an old file name or key gets an OLD-NAME error from the validator that names the new one, and `python3 tools/scripts/migrate-release-test-names.py --apply` moves its files once.

## Relationship to TST-* notes

- `TST-*` notes, stored per `LIFECYCLE.md` "Test storage", are individual test specifications with frontmatter, procedure and evidence.
- **An acceptance check is a `TST-*` note at `level: acceptance`** (ADR-0031; the retired `check` type is `TAXONOMY.md`, "`check` — retired").
- `level:` is a spectrum: a `unit` test is a pytest module, an `acceptance` test is a thing a person does, and a `command:` moves a note along it.
- An acceptance test rests at `active` (`STATUSES.md` `[[test]]`) and owes no separate review (`QUALITY.md`, "Independent review (clean-context)").
