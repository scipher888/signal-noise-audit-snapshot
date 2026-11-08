#!/usr/bin/env python3
"""Exact machine-question quotes and unchanged essay bodies for Issues 34–36."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BASE = "1da8824"
MANIFEST = REPO / "issues" / "machine-question-provenance.json"


def essay_paragraphs(page: str) -> list[str]:
    stripped = re.sub(r'<aside class="provenance".*?</aside>', "", page, flags=re.S)
    stripped = re.sub(r'<div class="note[^"]*">.*?</div>', "", stripped, flags=re.S)
    paras = re.findall(r"<p(?![^>]*\bclass=)>(.*?)</p>", stripped, flags=re.S)
    out = []
    for para in paras:
        text = html.unescape(re.sub(r"<[^>]+>", "", para))
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            out.append(text)
    return out


def provenance_question(page: str) -> str:
    match = re.search(
        r'<p class="provenance-question">(.*?)</p>',
        page,
        flags=re.S,
    )
    if not match:
        raise SystemExit("missing provenance question")
    return html.unescape(re.sub(r"<[^>]+>", "", match.group(1))).strip()


def git_show(path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{BASE}:{path}"],
        cwd=REPO,
        text=True,
    )


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_issue = {item["issue"]: item for item in manifest["selected"]}
    if list(by_issue) != [34, 35, 36]:
        raise SystemExit(f"unexpected selected issues: {list(by_issue)}")
    pages = {
        34: REPO / "issues/issue-034/machine-version/index.html",
        35: REPO / "issues/issue-035/machine-version/index.html",
        36: REPO / "issues/issue-036/machine-version/index.html",
    }
    forbidden = [
        REPO / "issues/issue-034/index.html",
        REPO / "issues/issue-035/index.html",
        REPO / "issues/issue-036/index.html",
        REPO / "issues/issue-034/development/index.html",
        REPO / "issues/issue-035/development/index.html",
        REPO / "issues/issue-036/development/index.html",
    ]
    for path in forbidden:
        if 'class="provenance"' in path.read_text(encoding="utf-8"):
            raise SystemExit(f"provenance note leaked onto {path.relative_to(REPO)}")
    for issue, path in pages.items():
        current = path.read_text(encoding="utf-8")
        rel = path.relative_to(REPO).as_posix()
        previous = git_show(rel)
        if essay_paragraphs(current) != essay_paragraphs(previous):
            raise SystemExit(f"essay body changed on {rel}")
        quoted = provenance_question(current)
        if quoted != by_issue[issue]["exact_question"]:
            raise SystemExit(f"question mismatch on issue {issue}")
        if current.count('class="provenance"') != 1:
            raise SystemExit(f"provenance count on {rel}")
        if "The question given to the AI:" not in current:
            raise SystemExit(f"label missing on {rel}")
        if "Joel" in current:
            raise SystemExit(f"real name on {rel}")
    seed34 = re.search(
        r'id="machine-seed".*?<pre class="seed">(.*?)</pre>',
        (REPO / "issues/issue-034/development/index.html").read_text(encoding="utf-8"),
        flags=re.S,
    ).group(1)
    q34 = html.unescape(seed34).strip().split("\n\n", 1)[0]
    if q34 != by_issue[34]["exact_question"]:
        raise SystemExit("issue 34 question is not the seed's first paragraph")
    if "Write an essay" not in seed34:
        raise SystemExit("issue 34 full prompt lost its format line")
    seed35 = re.search(
        r'id="machine-seed".*?<pre class="seed">(.*?)</pre>',
        (REPO / "issues/issue-035/development/index.html").read_text(encoding="utf-8"),
        flags=re.S,
    ).group(1)
    q35 = html.unescape(seed35).strip().split("\n\n", 1)[0]
    if q35 != by_issue[35]["exact_question"]:
        raise SystemExit("issue 35 question is not the seed's first paragraph")
    prompt36 = (REPO / "issues/issue-036/source/development/machine-question.md").read_text(
        encoding="utf-8"
    )
    q36 = prompt36.strip().split("\n\n", 1)[0]
    if q36 != by_issue[36]["exact_question"]:
        raise SystemExit("issue 36 question is not the prompt file's first paragraph")
    if "Write an essay" not in prompt36.split("\n\n", 1)[1]:
        raise SystemExit("issue 36 format line missing from the prompt file")
    requests = sorted(
        (REPO / "issues/issue-036/source/development/records").glob("machine-*-request.json")
    )
    if len(requests) != 4:
        raise SystemExit("expected four Issue 36 machine requests")
    for path in requests:
        content = json.loads(path.read_text(encoding="utf-8"))["messages"][0]["content"]
        if content != prompt36.strip() and content != prompt36:
            # file ends with a newline; request content matches the stripped file
            if content != prompt36.rstrip("\n"):
                raise SystemExit(f"request drifted: {path.name}")
    isolation = json.loads(
        (REPO / "issues/issue-036/source/metadata/isolation.json").read_text(encoding="utf-8")
    )
    if isolation.get("machine_messages_contain_author_content") is not False:
        raise SystemExit("isolation record does not support a clean machine input")
    if isolation.get("selected_unchanged") is not True:
        raise SystemExit("isolation record does not say the selected essay was unchanged")
    print("machine provenance check ok")


if __name__ == "__main__":
    main()
