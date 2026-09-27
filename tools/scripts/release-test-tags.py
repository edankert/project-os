#!/usr/bin/env python3
"""Rewrite quoted procedure expectation lines as tag-only lines (ADR-0049, ISS-0088).

A procedure step used to quote a check's `## Expect` line word for word, so
rewriting the check broke every procedure that quoted it. A line may now be only
its tags, `` - `TST-0480` ``, and `release-test.py` prints the check's current
Expect lines in its place. This script makes that change where it loses
nothing, and leaves every other line as written:

  one line whose quote is exactly what its tag would print
      -> the tags alone. That is a check with one Expect line, or `.N` on a
      check that pairs step N with Expect line N (`release-test.py`,
      `expect_for`), quoting line N
  one step quoting every Expect line of a check, all with the same tags
      -> one tag-only line where the first of them was

Any other line stays quoted: its tag-only form would print more than the
author wrote. A line whose
tags name several checks stays quoted too, for the same reason. Each kept line
is reported with its reason.

--refresh does the other half, for a line that must stay quoted. When a check's
Expect line has been reworded, every procedure quoting the old words fails. For each
such quote, it finds the check's last version in git (the working tree's edit
against HEAD, then older commits) whose Expect had the quoted line, and
rewrites the quote with the current line at the same position. It does so only
when the Expect section has as many lines as it had then; otherwise it reports
the line for a person to re-quote.

Usage:
    release-test-tags.py [--repo-root .]      # dry run: what would change, and what stays
    release-test-tags.py --apply
    release-test-tags.py --refresh [--apply]  # re-quote lines a reworded check broke
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def release_test_module():
    spec = importlib.util.spec_from_file_location("_release_test_for_tags", HERE / "release-test.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def plan(repo_root: Path):
    rt = release_test_module()
    docs = repo_root / "docs"
    checks = rt.load_checks(docs, repo_root=repo_root)
    out = []
    for procedure in rt.load_procedures(docs, repo_root):
        path = repo_root / procedure.path
        edits, kept = [], []
        for step in procedure.steps:
            quoted = [e for e in step.expectations if e.quote and e.raw != step.body[0]]
            by_check: dict[tuple, list] = {}
            for e in quoted:
                owners = {c for c, _n in e.tags}
                if len(owners) != 1:
                    kept.append((step.number, e.raw, "its tags name %d checks" % len(owners)))
                    continue
                by_check.setdefault((next(iter(owners)), tuple(e.tags)), []).append(e)
            for (cid, tags), lines in by_check.items():
                check = checks.get(cid)
                if check is None:
                    kept.append((step.number, lines[0].raw, "%s is not an acceptance check here" % cid))
                    continue
                want = []
                for _c, n in tags:
                    want += [x for x in rt.expect_for(check, n) if x not in want]
                have = [e.quote for e in lines]
                if not rt.expect_text(check):
                    for e in lines:
                        kept.append((step.number, e.raw, "%s states no Expect text to print" % cid))
                    continue
                if any(q not in rt.expect_text(check) for q in have):
                    for e in lines:
                        kept.append((step.number, e.raw, "it does not quote %s's current Expect" % cid))
                    continue
                if sorted(set(have)) != sorted(want):
                    for e in lines:
                        kept.append((step.number, e.raw, "%s has %d Expect lines and this step quotes %d"
                                     % (cid, len(want), len(set(have)))))
                    continue
                first = lines[0].raw
                m = rt._MARKER_RE.match(first)
                prefix = first[:m.end()] if m else first[:len(first) - len(first.lstrip())]
                tag_text = " ".join("`%s%s`" % (c, "." + n if n else "") for c, n in tags)
                edits.append((first, prefix + tag_text, [e.raw for e in lines[1:]]))
        if edits or kept:
            out.append({"path": path, "shown": procedure.path, "edits": edits, "kept": kept})
    return out


def _git(repo_root: Path, *args: str) -> str:
    import subprocess
    try:
        return subprocess.run(["git", *args], cwd=repo_root, capture_output=True, text=True).stdout
    except OSError:
        return ""


def refresh_plan(repo_root: Path):
    """Stale quotes, each with the current line at the position it used to quote."""
    rt = release_test_module()
    docs = repo_root / "docs"
    checks = rt.load_checks(docs, repo_root=repo_root)
    history: dict[str, list[list[str]]] = {}

    def versions(check) -> list[list[str]]:
        if check.id in history:
            return history[check.id]
        rel = str(Path(check.path)) if not Path(check.path).is_absolute() else str(Path(check.path).relative_to(repo_root))
        out = []
        for rev in [h for h in _git(repo_root, "log", "--format=%H", "--", rel).split() if h]:
            text = _git(repo_root, "show", "%s:%s" % (rev, rel))
            body = text.split("\n---", 1)[1] if text.startswith("---") and "\n---" in text[3:] else text
            lines = []
            for line in rt.under_heading(body, "Expect", "Expected results").splitlines():
                n = rt.normalise(line)
                if n and n not in lines:
                    lines.append(n)
            out.append(lines)
        history[check.id] = out
        return out

    out = []
    for procedure in rt.load_procedures(docs, repo_root):
        edits, kept = [], []
        for step in procedure.steps:
            for e in step.expectations:
                owners = {c for c, _n in e.tags}
                if not e.quote or len(owners) != 1:
                    continue
                check = checks.get(next(iter(owners)))
                now = rt.expect_text(check) if check else []
                if not now or e.quote in now:
                    continue
                found = None
                for old in versions(check):
                    if e.quote in old:
                        found = old
                        break
                if found is None:
                    kept.append((step.number, e.raw, "no earlier version of %s has these words" % check.id))
                    continue
                if len(found) != len(now):
                    kept.append((step.number, e.raw, "%s's Expect had %d lines and has %d; re-quote by hand"
                                 % (check.id, len(found), len(now))))
                    continue
                new_text = now[found.index(e.quote)]
                m = rt._MARKER_RE.match(e.raw)
                prefix = e.raw[:m.end()] if m else e.raw[:len(e.raw) - len(e.raw.lstrip())]
                tag_text = " ".join("`%s%s`" % (c, "." + n if n else "") for c, n in e.tags)
                edits.append((e.raw, prefix + new_text + " " + tag_text, []))
        if edits or kept:
            out.append({"path": repo_root / procedure.path, "shown": procedure.path, "edits": edits, "kept": kept})
    return out


def apply(item) -> None:
    lines = item["path"].read_text(encoding="utf-8").split("\n")
    for first, new, drop in item["edits"]:
        i = lines.index(first)
        lines[i] = new
        for raw in drop:
            j = lines.index(raw, i + 1)
            del lines[j]
    item["path"].write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--refresh", action="store_true",
                    help="re-quote lines whose check's Expect was reworded")
    args = ap.parse_args(argv)
    root = Path(args.repo_root).resolve()
    items = refresh_plan(root) if args.refresh else plan(root)
    if args.apply:
        #: Write first, report after: a reader that closes the pipe early
        #: (`| head`) must not stop the rewrite half way (TASK-0186).
        for item in items:
            if item["edits"]:
                apply(item)
    n_edit = sum(len(i["edits"]) for i in items)
    n_kept = sum(len(i["kept"]) for i in items)
    if args.refresh:
        print("release-test-tags: %s %d stale quote(s) from the check's current Expect; %d need a person"
              % ("re-quoted" if args.apply else "would re-quote", n_edit, n_kept))
    else:
        print("release-test-tags: %s %d line(s) to tags only; %d quoted line(s) stay quoted"
              % ("rewrote" if args.apply else "would rewrite", n_edit, n_kept))
    for item in items:
        for first, new, drop in item["edits"]:
            print("   %s: %s%s" % (item["shown"], new.strip(),
                                   " (replaces %d lines)" % (1 + len(drop)) if drop else ""))
        for number, raw, why in item["kept"]:
            print("   keep  %s step %d: %s" % (item["shown"], number, why))
    return 0


if __name__ == "__main__":
    sys.exit(main())
