#!/usr/bin/env python3
"""Rebuild Issue 36 audit pages from issues/issue-036/source.

The source tree is the public sanitized package (essays, audits, Stage C
returns, alternatives, scrubbed records, transcript). deployment-spec.md,
the package README, and the package MANIFEST are not published: they are
agent-packaging notes, not reader records. Frozen Markdown hashes are
checked and never rewritten.

    python3 issues/issue-036/build.py
    python3 issues/issue-036/build.py --check
"""

from __future__ import annotations

import html
import json
import posixpath
import re
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
SOURCE = ROOT / "source"
ISSUES_INDEX = REPO / "issues" / "index.html"

AUTHOR_HASH = "c9f631361ad1ac06be3b31ff45e152b61f4f672d7705f3fb2f333aebec9c44dc"
MACHINE_HASH = "fec0422798b711d85ab4a8ad74aca288d34843ba1914bcf3595b7f18bc151a78"
HUMAN_ONLY_HASH = "8870157c3a8867c088eb72339253785787f20230fe3d10ba21dbfc8ebe6a8abd"
COST_TOTAL = Decimal("2.37967004")

AUTHOR_WEB = "https://www.signalandnoise.email/p/my-son-his-calorie-tracker-and-the-tyranny-of-the-nanny-bot/"
MACHINE_WEB = "https://www.signalandnoise.email/p/alignment-at-human-scale/"
UNAIDED_WEB = "https://www.signalandnoise.email/p/issue-036-written-without-ai/"
AUTHOR_AUDIO = "https://open.spotify.com/episode/01j4XyZqy3Qe9sLEdIhyzX"
MACHINE_AUDIO = "https://open.spotify.com/episode/6p3025WSILzb9WC31hA88e"
CSS_V = "de2cc137"
JS_V = "0c872f22"

AUTHOR_TITLE = "My Son, His Calorie Tracker, and the Tyranny of the Nanny Bot"
MACHINE_TITLE = "Alignment at Human Scale"
MACHINE_DEK = (
    "The everyday failures of AI agents reveal why helpfulness, safety, "
    "and moral judgment cannot be reduced to a single rule."
)

RULING = (
    "November 8, 2026, 11:47 AM PST (America/Los_Angeles). "
    "Author ruling, exact wording: “Ruling A for both essays: keep them unchanged "
    "and record the findings on the audit pages.”"
)


def sha256(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def read_src(rel: str) -> str:
    return (SOURCE / rel).read_text(encoding="utf-8")


def words(text: str) -> int:
    return len(text.split())


def verify_sources() -> None:
    checks = {
        "essays/humanai-essay-FROZEN-v1.1.md": AUTHOR_HASH,
        "essays/machine-essay-FROZEN-v1.0.md": MACHINE_HASH,
        "essays/human-only-VERBATIM.md": HUMAN_ONLY_HASH,
        "development/machine-alternatives/02-gpt-6-astra.md": MACHINE_HASH,
    }
    for rel, expect in checks.items():
        got = sha256(SOURCE / rel)
        if got != expect:
            raise SystemExit(f"frozen hash changed for {rel}: {got}")
    costs = json.loads(read_src("metadata/costs.json"))
    total = sum(Decimal(run["actual_api_reported_usd"]) for run in costs["runs"])
    if total != COST_TOTAL or Decimal(costs["actual_api_reported_total"]) != COST_TOTAL:
        raise SystemExit(f"cost ledger {total} != {COST_TOTAL}")
    v10 = read_src("development/freeze-history/humanai-v1.0.md")
    v11 = read_src("essays/humanai-essay-FROZEN-v1.1.md")
    body10 = "\n".join(v10.splitlines()[2:]).strip()
    body11 = "\n".join(v11.splitlines()[2:]).strip()
    if body10 != body11:
        raise SystemExit("author v1.0 and v1.1 bodies differ; refusing to build")
    if "### Make AI Warn, Not Rule" not in v10.splitlines()[0]:
        raise SystemExit("unexpected v1.0 title")
    if AUTHOR_TITLE not in v11.splitlines()[0]:
        raise SystemExit("unexpected v1.1 title")


def public_href(source_rel: str, page_dir: str) -> str:
    target = posixpath.join("source", source_rel)
    return posixpath.relpath(target, page_dir or ".")


def resolve_source_link(href: str, source_file: str) -> str | None:
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return None
    joined = posixpath.normpath(posixpath.join(posixpath.dirname(source_file), href))
    if joined.startswith("../"):
        raise SystemExit(f"link escapes source tree: {href} from {source_file}")
    return joined


def rewrite_href(href: str, source_file: str, page_dir: str) -> str:
    resolved = resolve_source_link(href, source_file)
    if resolved is None:
        return href
    return public_href(resolved, page_dir)


def autolink_plain(text: str) -> str:
    parts: list[str] = []
    pos = 0
    for match in re.finditer(r"https?://[^\s<>]+", text):
        parts.append(html.escape(text[pos : match.start()], quote=False))
        raw = match.group(0)
        href = raw.rstrip(".,;:")
        tail = raw[len(href) :]
        parts.append(
            f'<a href="{html.escape(href, quote=True)}">{html.escape(href, quote=False)}</a>'
            f"{html.escape(tail, quote=False)}"
        )
        pos = match.end()
    parts.append(html.escape(text[pos:], quote=False))
    return "".join(parts)


def render_inline(text: str, source_file: str, page_dir: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(text):
        if text.startswith("**", i):
            j = text.find("**", i + 2)
            if j != -1:
                out.append("<strong>" + render_inline(text[i + 2 : j], source_file, page_dir) + "</strong>")
                i = j + 2
                continue
        if text.startswith("`", i):
            j = text.find("`", i + 1)
            if j != -1:
                out.append("<code>" + html.escape(text[i + 1 : j], quote=False) + "</code>")
                i = j + 1
                continue
        if text.startswith("[", i):
            match = re.match(r"\[([^\]]+)\]\(([^)\s]+)\)", text[i:])
            if match:
                label = render_inline(match.group(1), source_file, page_dir)
                href = rewrite_href(match.group(2), source_file, page_dir)
                out.append(f'<a href="{html.escape(href, quote=True)}">{label}</a>')
                i += match.end()
                continue
        if text[i] == "*":
            j = text.find("*", i + 1)
            if j != -1 and "\n" not in text[i + 1 : j]:
                out.append("<em>" + render_inline(text[i + 1 : j], source_file, page_dir) + "</em>")
                i = j + 1
                continue
        n = i + 1
        while n < len(text) and text[n] not in "*`[":
            n += 1
        out.append(autolink_plain(text[i:n]))
        i = n
    return "".join(out)


def slug(text: str) -> str:
    plain = re.sub(r"[*_`]", "", text)
    plain = re.sub(r"[^a-zA-Z0-9]+", "-", plain).strip("-").lower()
    return plain[:72] or "section"


def is_table_sep(line: str) -> bool:
    return bool(re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", line))


def split_cells(line: str) -> list[str]:
    raw = line.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|"):
        raw = raw[:-1]
    return [cell.strip() for cell in raw.split("|")]


def render_md(text: str, source_file: str, page_dir: str, id_prefix: str) -> str:
    lines = text.replace("\r\n", "\n").split("\n")
    blocks: list[str] = []
    i = 0
    seen: dict[str, int] = {}

    def heading_id(title: str) -> str:
        base = f"{id_prefix}-{slug(title)}" if id_prefix else slug(title)
        n = seen.get(base, 0)
        seen[base] = n + 1
        return base if n == 0 else f"{base}-{n+1}"

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if re.match(r"^ {0,3}(-{3,}|\*{3,}|_{3,})\s*$", line):
            blocks.append("<hr>")
            i += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if heading:
            level = min(len(heading.group(1)), 4)
            title = heading.group(2).strip()
            hid = heading_id(title)
            blocks.append(
                f'<h{level} id="{hid}">{render_inline(title, source_file, page_dir)}</h{level}>'
            )
            i += 1
            continue
        if line.lstrip().startswith("|"):
            rows: list[str] = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(lines[i])
                i += 1
            body_rows = [row for row in rows if not is_table_sep(row)]
            if not body_rows:
                continue
            head = split_cells(body_rows[0])
            html_rows = [
                "<thead><tr>"
                + "".join(
                    f"<th>{render_inline(cell, source_file, page_dir)}</th>" for cell in head
                )
                + "</tr></thead>"
            ]
            body = []
            for row in body_rows[1:]:
                cells = split_cells(row)
                body.append(
                    "<tr>"
                    + "".join(
                        f"<td>{render_inline(cell, source_file, page_dir)}</td>" for cell in cells
                    )
                    + "</tr>"
                )
            html_rows.append("<tbody>" + "".join(body) + "</tbody>")
            blocks.append('<div class="table-scroll"><table>' + "".join(html_rows) + "</table></div>")
            continue
        if re.match(r"^\s*>\s?", line):
            quoted: list[str] = []
            while i < len(lines) and re.match(r"^\s*>\s?", lines[i]):
                quoted.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append(
                "<blockquote><p>"
                + render_inline(" ".join(part.strip() for part in quoted), source_file, page_dir)
                + "</p></blockquote>"
            )
            continue
        if re.match(r"^\s*[-*]\s+", line) and not re.match(r"^\s*\*\S", line):
            items = _collect_list(lines, i, r"^\s*[-*]\s+")
            i = items[0]
            blocks.append(
                "<ul>"
                + "".join(
                    f"<li>{render_inline(item, source_file, page_dir)}</li>" for item in items[1]
                )
                + "</ul>"
            )
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            items = _collect_list(lines, i, r"^\s*\d+\.\s+")
            i = items[0]
            blocks.append(
                "<ol>"
                + "".join(
                    f"<li>{render_inline(item, source_file, page_dir)}</li>" for item in items[1]
                )
                + "</ol>"
            )
            continue
        para = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not _block_start(lines[i]):
            para.append(lines[i].strip())
            i += 1
        blocks.append("<p>" + render_inline(" ".join(para), source_file, page_dir) + "</p>")
    return "\n".join(blocks)


def _collect_list(lines: list[str], i: int, pattern: str) -> tuple[int, list[str]]:
    items: list[str] = []
    while i < len(lines):
        if re.match(pattern, lines[i]):
            items.append(re.sub(pattern, "", lines[i]).strip())
            i += 1
            continue
        if not lines[i].strip():
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and re.match(pattern, lines[j]):
                i = j
                continue
        break
    return i, items


def _block_start(line: str) -> bool:
    if re.match(r"^(#{1,6})\s+", line):
        return True
    if line.lstrip().startswith("|"):
        return True
    if re.match(r"^\s*>\s?", line):
        return True
    if re.match(r"^\s*[-*]\s+", line):
        return True
    if re.match(r"^\s*\d+\.\s+", line):
        return True
    if re.match(r"^ {0,3}(-{3,}|\*{3,}|_{3,})\s*$", line):
        return True
    return False


def essay_body_html(rel: str, page_dir: str, skip_title: bool, skip_dek: bool) -> str:
    text = read_src(rel).replace("\r\n", "\n").strip("\n")
    lines = text.split("\n")
    idx = 0
    if skip_title and lines and lines[0].startswith("#"):
        idx = 1
        if idx < len(lines) and not lines[idx].strip():
            idx += 1
    if skip_dek and idx < len(lines) and lines[idx].startswith("*") and lines[idx].endswith("*"):
        idx += 1
        if idx < len(lines) and not lines[idx].strip():
            idx += 1
    body = "\n".join(lines[idx:])
    return render_md(body, rel, page_dir, "essay")


def prose_html(rel: str, page_dir: str) -> str:
    return render_md(read_src(rel), rel, page_dir, Path(rel).stem)


def cnav(page: str) -> str:
    """Companion nav. Labels are identical on every Issue 36 surface."""

    def item(key: str, href: str, label: str) -> str:
        if key == page:
            return f'<span class="here" aria-current="page">{label}</span>'
        return f'<a href="{href}">{label}</a>'

    paths = {
        "author-audit": {
            "essay": AUTHOR_WEB,
            "author-audit": "",
            "machine-essay": "machine-version/",
            "machine-audit": "machine-version/audit/",
            "unaided": UNAIDED_WEB,
            "development": "development/",
        },
        "machine-essay": {
            "essay": AUTHOR_WEB,
            "author-audit": "../",
            "machine-essay": "",
            "machine-audit": "audit/",
            "unaided": UNAIDED_WEB,
            "development": "../development/",
        },
        "machine-audit": {
            "essay": AUTHOR_WEB,
            "author-audit": "../../",
            "machine-essay": "../",
            "machine-audit": "",
            "unaided": UNAIDED_WEB,
            "development": "../../development/",
        },
        "development": {
            "essay": AUTHOR_WEB,
            "author-audit": "../",
            "machine-essay": "../machine-version/",
            "machine-audit": "../machine-version/audit/",
            "unaided": UNAIDED_WEB,
            "development": "",
        },
    }[page]
    sep = " &middot; "
    author = sep.join(
        [
            item("essay", paths["essay"], "The essay"),
            f'<a href="{AUTHOR_AUDIO}">Audio companion</a>',
            item("author-audit", paths["author-audit"], "The audit"),
        ]
    )
    machine = sep.join(
        [
            item("machine-essay", paths["machine-essay"], "The essay"),
            f'<a href="{MACHINE_AUDIO}">Audio companion</a>',
            item("machine-audit", paths["machine-audit"], "The audit"),
        ]
    )
    unaided = item("unaided", paths["unaided"], "The piece")
    convo = item("development", paths["development"], "The conversation behind this")
    return (
        f'<nav class="cnav {{klass}}" aria-label="Issue 36 companions"><dl>'
        f"<dt>The author&rsquo;s</dt><dd>{author}</dd>"
        f"<dt>The machine&rsquo;s</dt><dd>{machine}</dd>"
        f"<dt>Written without AI</dt><dd>{unaided}</dd>"
        f"<dt>Both, verbatim</dt><dd>{convo}</dd>"
        f"</dl></nav>"
    )


def nav_top(page: str) -> str:
    return cnav(page).replace("{klass}", "top")


def nav_bottom(page: str) -> str:
    return cnav(page).replace("{klass}", "")


LIVE_NOTE = (
    "<p><strong>The essay companions are live.</strong> "
    "Signal &amp; Noise web pull request 43 was merged November 8, 2026, 12:19:33 PM PST, "
    "commit <code>697a6da0fd1526d9912b01848b9aebbb5d43c007</code>. "
    "Rechecked for this record: each of the three pages returned HTTP 200, and the frozen prose on the page matches the freeze. "
    "The written-without-AI page keeps one template sentence outside that prose. "
    "This audit record is the inspection surface for those live pages.</p>"
)

AUDIO_NOTE = (
    "<p><strong>Audio companions are published Spotify episodes.</strong> "
    "These are plain canonical links. This record does not embed a player and does not store audio files. "
    f'Author: <a href="{AUTHOR_AUDIO}">My Son, His Calorie Tracker, and the Tyranny of the Nanny Bot</a>. '
    "Canonical page, embed, and oEmbed each returned that title. The embed duration field is 235003 ms, which is 3:55. "
    f'Machine: <a href="{MACHINE_AUDIO}">Alignment at Human Scale</a>. '
    "oEmbed and the embed each returned that title. The embed duration field is 304776 ms, which rounds to 5:05. "
    "A direct fetch of the machine canonical URL returned HTTP 200 with that public title. "
    "A headless browser load of the same URL still received Spotify’s “Page not found” page at 1:19 PM PST on November 8, 2026. "
    "Spotify for Creators preview state was not rechecked and is not described as finished. "
    "The reported API total does not include text-to-speech charges, and none are added here.</p>"
)

TESTIMONY = (
    "<p><strong>Testimony, and what it does not cover.</strong> "
    "The author confirmed that his adult son actually had help withdrawn and did listen politely. "
    "Those two points are the author’s testimony. They are not model inventions, and they are not "
    "independently documented clinical findings. No family conversations were accessed. "
    "Neither covert intervention nor lack of consent has been established. "
    "The confirmation does not support the broader claims that remain open on this audit: "
    "“refusal rarely protects anyone” (H6, a floor support gap), calories burned on a run being "
    "“available from … a food label” (H7, a literal mismatch), and “accountable to no voter, patient "
    "or client” (H11, a floor-level literal absence claim). Those findings stay visible. "
    "Ruling A keeps the sentences in the essay and records the gaps here.</p>"
)

RULING_BLOCK = f"""<div class="callout coral" id="ruling"><p>{html.escape(RULING)}</p>
<ul>
<li>Both freezes stay byte-for-byte unchanged. There is no v1.2 and no silent safety edit.</li>
<li>Author freeze <code>humanai-essay-FROZEN-v1.1</code>, sha256 <code>{AUTHOR_HASH}</code>. Title only changed from v1.0 (“Make AI Warn, Not Rule”) to Gemini 4 Argon’s title. The body is identical to v1.0.</li>
<li>Machine freeze <code>machine-essay-FROZEN-v1.0</code>, sha256 <code>{MACHINE_HASH}</code>. GPT-6 Astra’s “Alignment at Human Scale,” selected unchanged by Grok Bot. Same bytes as machine alternative 02.</li>
<li>The dual audit and Stage C synthesis were written before the ruling and still contain the historical A-or-revise recommendation. That choice is closed. The findings, including floor support gaps, are not withdrawn and are not described as a pass.</li>
<li>Audio companions are the two published Spotify episode links in the navigation. This repository does not store an audio file.</li>
</ul>
<p>This is an editorial disposition. It does not certify the essays as true, medically safe, or a validation of AI alignment.</p></div>"""


def machine_note_class() -> str:
    return RULING_BLOCK.replace('class="callout coral"', 'class="note coral"').replace(
        'class="callout ', 'class="note '
    )


def site_header(depth: str) -> str:
    return f"""<a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="shell header-inner">
      <a class="header-cta" href="https://www.signalandnoise.email" target="_blank" rel="noreferrer" aria-label="Read the Signal &amp; Noise newsletter">
        <span>Read the Newsletter</span>
        <svg aria-hidden="true" viewBox="0 0 20 20" fill="none"><path d="M5 15 15 5m0 0H8m7 0v7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
      <a class="brand" href="{depth}world/" aria-label="The World Behind the Words home">
        <span class="brand-mark" aria-hidden="true"><span></span></span>
        <span class="brand-copy"><strong>World Behind the Words</strong></span>
      </a>
      <nav class="primary-nav" aria-label="Primary navigation">
        <a href="{depth}signal-noise/">Publication</a>
        <a href="{depth}issues/" aria-current="page">Issues</a>
      </nav>
    </div>
  </header>"""


def site_footer(depth: str) -> str:
    return f"""<footer class="site-footer">
    <div class="shell">
      <div class="footer-grid">
        <div class="footer-column">
          <h3>Read</h3>
          <a href="https://www.signalandnoise.email">Signal &amp; Noise</a>
        </div>
        <div class="footer-column">
          <h3>Inspect</h3>
          <a href="{depth}world/">World Behind the Words</a>
          <a href="{depth}signal-noise/">Signal &amp; Noise</a>
          <a href="{depth}issues/">Issues</a>
          <a href="{depth}repository/">Source Repository</a>
        </div>
        <div class="footer-column">
          <h3>Issue 36</h3>
          <a href="{AUTHOR_WEB}">Read the issue</a>
          <a href="machine-version/">The machine&rsquo;s version</a>
          <a href="{UNAIDED_WEB}">The unaided piece</a>
          <a href="development/">The conversation behind this</a>
        </div>
        <div class="footer-column">
          <h3>Socials</h3>
          <a class="footer-social" href="https://x.com/signalnoisepub" target="_blank" rel="noreferrer" aria-label="Signal &amp; Noise on X">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
          </a>
        </div>
      </div>
      <div class="footer-bottom">
        <a class="author-byline" href="https://scipher888.github.io/synthia-cipher/"><span class="cipher-glyph" aria-hidden="true"></span> by Synthia Cipher</a>
        <span>Public snapshot &middot; November 2026 &middot; essay companions live</span>
      </div>
    </div>
  </footer>"""


def author_page() -> str:
    page = ""
    audit = prose_html("audit/dual-audit.md", page)
    synthesis = prose_html("audit/stage-c-synthesis.md", page)
    method = prose_html("audit/execution-method.md", page)
    sources = prose_html("audit/sources/SOURCE-LOG.md", page)
    credits = prose_html("metadata/CREDITS.md", page)
    attest = prose_html("metadata/factual-attestations.md", page)
    leg_a = prose_html("audit/stage-c/humanai-leg-a-kimi-k3.md", page)
    leg_b = prose_html("audit/stage-c/humanai-leg-b-claude-opus-4.1.md", page)
    decision = prose_html("development/DECISION-RECORD.md", page)
    author_words = words(read_src("essays/humanai-essay-FROZEN-v1.1.md"))
    machine_words = words(read_src("essays/machine-essay-FROZEN-v1.0.md"))
    return f"""<!doctype html>
<html lang="en">
<head>
  <link rel="icon" href="../../favicon.ico">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Published audit for Signal &amp; Noise Issue 36, {html.escape(AUTHOR_TITLE)}: Ruling A, floor support gaps, testimony limits, and Stage C objections. Essay companions are live.">
  <title>Issue 36 Published Audit - {html.escape(AUTHOR_TITLE)}</title>
  <link rel="stylesheet" href="../../assets/styles.css?v={CSS_V}">
  <script src="../../assets/site.js?v={JS_V}" defer></script>
  <style>
    .issue-record-content h3,.issue-record-content h4{{margin-top:1.6rem}}
    .issue-record-content hr{{border:0;border-top:1px solid rgba(0,0,0,.08);margin:1.6rem 0}}
    .issue-record-content table{{width:100%;border-collapse:collapse;font-size:.9rem;margin:1rem 0}}
    .issue-record-content th,.issue-record-content td{{text-align:left;padding:.4rem .5rem;border-bottom:1px solid rgba(0,0,0,.08);vertical-align:top}}
    .table-scroll{{overflow-x:auto}}
    .issue-record-content code{{font-family:ui-monospace,monospace;font-size:.86em}}
  </style>
</head>
<body class="issue-record">
  {site_header("../../")}
  <main id="main">
    <section class="page-hero">
      <div class="shell page-hero-grid">
        <div>
          <div class="issue-eyebrow"><p class="eyebrow">Issue 36 &middot; November 8, 2026 &middot; Synthia Cipher</p></div>
          <h1 class="page-title">{html.escape(AUTHOR_TITLE)}</h1>
          <p class="lede">Audit for Issue 36. Intended issue date: November 8, 2026. Byline: Synthia Cipher. Live companions: the <a href="{AUTHOR_WEB}">human/AI essay</a>, the <a href="{MACHINE_WEB}">machine essay</a>, and the <a href="{UNAIDED_WEB}">written-without-AI page</a>. No dek on the author essay. Audio companions are linked above.</p>
          {nav_top("author-audit")}
        </div>
      </div>
    </section>
    <section class="section section-soft">
      <div class="shell reading-layout">
        <article class="reading-content issue-record-content">
          <section class="content-section" id="start">
            <p class="eyebrow">Published audit</p>
            <h2>The essay is the judgment. This page is the inspection surface.</h2>
            {LIVE_NOTE}
            {AUDIO_NOTE}
            <div class="callout mint"><p><strong>Canonicality.</strong> The essay Signal &amp; Noise stands behind is Issue 36, <em>{html.escape(AUTHOR_TITLE)}</em>, by Synthia Cipher, November 8, 2026. This page is its audit, not a second edition and not a corrected essay. The machine essay, <a href="{MACHINE_WEB}">{html.escape(MACHINE_TITLE)}</a>, is a companion. It is not a correction of the author’s essay and not a second front door. The inspection copy is <a href="machine-version/">on this record</a>. The written-without-AI page is the author’s raw prose, live at its own address. The machine generations did not see it. Author freeze sha256 <code>{AUTHOR_HASH}</code> ({author_words} whitespace-delimited words in the Markdown file, title included, no dek). Machine freeze sha256 <code>{MACHINE_HASH}</code> ({machine_words} whitespace-delimited words in the Markdown file, title and dek included).</p></div>
            {RULING_BLOCK}
            <div class="callout coral" id="testimony">{TESTIMONY}</div>
            <div class="callout" id="attestations"><h2>Factual attestations</h2>
            {attest}
            </div>
          </section>
          <section class="content-section" id="assembly">
            <h2>How the author essay was assembled</h2>
            <p>Muse Wonder is the base. Gemini 4 Argon supplied the title the author chose. GPT-6 Astra supplied the closing pair “The company owns the product. The adult owns the life.” The author revised the landing to keep Muse’s threshold sentences and to add “It may be safer. It will also be ignored.” Grok Bot assembled only those approved edits. Four earlier suggestions — restore a willingness to switch tools, narrow “refusal rarely protects anyone,” add an adult-son autonomy sentence, and remove the polite-listening line — were rejected. The polite-listening line and the withdrawal stay because the author said both happened. Nothing in that rejection repairs H6, H7, or H11.</p>
            <p>The machine essay was not assembled. Four models each received the same question and the same format instructions, with no brain dump and no author essay. Grok Bot chose Astra’s “Alignment at Human Scale” unchanged. Opus 5.5 (“Small Betrayals”), Gemini 4 Argon, and Muse Wonder remain alternatives.</p>
            {decision}
          </section>
          <section class="content-section" id="audit">
            <h2>Dual audit, unchanged findings</h2>
            <p>The document below is the audit text. Its opening states the later ruling. Sentences inside it that still offer a revise-before-publication alternative are historical. They are not an open question, and they are not a claim that the floor concerns were cleared.</p>
            {audit}
          </section>
          <section class="content-section" id="method">
            <h2>How the audit was run</h2>
            {method}
          </section>
          <section class="content-section" id="stage-c">
            <h2>Stage C synthesis</h2>
            {synthesis}
            <h2 id="stage-c-author-kimi">Stage C raw return — author essay, Kimi K3</h2>
            <p>Critic text, not a finding that every objection landed. Dispositions are in the synthesis above. Kimi K3 (<code>moonshotai/kimi-k3</code>, reasoning high).</p>
            {leg_a}
            <h2 id="stage-c-author-opus">Stage C raw return — author essay, Claude Opus 4.1</h2>
            <p>Critic text. Claude Opus 4.1 (<code>anthropic/claude-opus-4.1</code>, no explicit reasoning setting).</p>
            {leg_b}
          </section>
          <section class="content-section" id="sources">
            <h2>Source log</h2>
            {sources}
          </section>
          <section class="content-section" id="credits">
            <h2>Credits and cost</h2>
            <p>Actual API-reported total <strong>$2.37967004</strong>. Twelve completed paid calls. No further paid OpenRouter calls were made to build these pages. Figures are API usage reports, not a reconciled card statement.</p>
            {credits}
            <p>Per-run ledger: <a href="source/metadata/costs.json">costs.json</a>. Isolation check: <a href="source/metadata/isolation.json">isolation.json</a>.</p>
          </section>
          <section class="content-section" id="unaided">
            <h2>Written without AI</h2>
            <p>The live page uses the editorial display label “Written without AI — Issue 36.” That label is not an author-chosen title. The prose is <a href="source/essays/human-only-VERBATIM.md">human-only-VERBATIM.md</a>, sha256 <code>{HUMAN_ONLY_HASH}</code>, including the original typos. It is the author’s own account. It is not medical advice and not a model draft. No separate health-safety note was added. The development record renders it in full and explains the transcript truncation.</p>
          </section>
          <section class="content-section" id="closing">
            <div class="callout mint"><p>What this audit did: kept both freezes unchanged under Ruling A; published every logged author finding H1–H14 and machine finding M1–M12; published the Stage C returns and their dispositions, including objections that land and objections that do not; published the source log, the rejected edits, the testimony limit, and the $2.37967004 cost. It did not certify safety or alignment.</p></div>
          </section>
          {nav_bottom("author-audit")}
        </article>
      </div>
    </section>
  </main>
  {site_footer("../../")}
</body>
</html>
"""


MACHINE_CSS = """
body{font-family:Georgia,'Times New Roman',serif;line-height:1.65;color:#1A1917;background:#F8F7F4;margin:0;padding:3rem 1.25rem 5rem}
.wrap{max-width:44rem;margin:0 auto}
h1{font-size:1.85rem;line-height:1.15;margin:.4rem 0 .6rem}
h2{font-size:1.35rem;line-height:1.25;margin:2rem 0 .4rem}
.kicker{font-family:system-ui,sans-serif;font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:#6E6B64}
.dek{font-size:1.05rem}
.note{font-family:system-ui,sans-serif;font-size:.86rem;color:#3B3934;border:1px solid #E2DFD8;border-left:4px solid #8A6A1F;padding:.9rem 1.1rem;border-radius:3px;background:#F1EFEA;margin:1.4rem 0}
.note.coral{border-left-color:#A32B2B}
.note.mint{border-left-color:#1F6F5C}
.cnav{font-family:system-ui,sans-serif;font-size:.82rem;color:#6E6B64;margin:2.6rem 0 0;padding-top:1.1rem;border-top:1px solid #E2DFD8}
.cnav.top{margin:1.2rem 0 1.6rem;padding:0 0 1rem;border-top:0;border-bottom:1px solid #E2DFD8}
.cnav dl{display:grid;grid-template-columns:max-content 1fr;gap:.4rem 1rem;margin:0;align-items:baseline}
.cnav dt{font-size:.68rem;letter-spacing:.075em;text-transform:uppercase;font-weight:600;opacity:.85;white-space:nowrap}
.cnav dd{margin:0}
.cnav a{color:#1A1917}
.cnav .here{font-weight:600}
@media(max-width:640px){.cnav dl{grid-template-columns:1fr;gap:.1rem}.cnav dt{margin-top:.7rem}.cnav dt:first-of-type{margin-top:0}}
p{margin:1rem 0}
a{color:#1A1917}
code{font-family:ui-monospace,monospace;font-size:.86em}
.table-scroll{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.9rem;margin:1rem 0}
th,td{text-align:left;padding:.4rem .5rem;border-bottom:1px solid #E2DFD8;vertical-align:top}
"""

AUDIT_CSS = MACHINE_CSS.replace("max-width:44rem", "max-width:48rem").replace(
    "line-height:1.65", "line-height:1.6"
) + """
h1{font-size:1.6rem;line-height:1.2}
h2{font-size:1.25rem;margin-top:2.6rem;border-bottom:1px solid #E2DFD8;padding-bottom:.4rem}
h3{font-size:1.05rem;margin-top:1.6rem}
hr{border:0;border-top:1px solid #E2DFD8;margin:1.6rem 0}
"""


def machine_essay_page() -> str:
    body = essay_body_html("essays/machine-essay-FROZEN-v1.0.md", "machine-version", True, True)
    dek_attr = html.escape(MACHINE_DEK, quote=True)
    return f"""<!doctype html>
<html lang="en"><head><link rel="icon" href="../../../favicon.ico"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(MACHINE_TITLE)}: the machine essay for Signal &amp; Noise Issue 36, inspection copy of freeze machine-essay-FROZEN-v1.0.">
<title>The Machine's Version - {html.escape(MACHINE_TITLE)}</title>
<meta property="og:site_name" content="Signal &amp; Noise">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(MACHINE_TITLE, quote=True)}">
<meta property="og:description" content="{dek_attr}">
<meta property="og:url" content="https://scipher888.github.io/signal-noise-audit-snapshot/issues/issue-036/machine-version/">
<meta property="og:image" content="https://www.signalandnoise.email/assets/preview.png?v=09b48f76">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Signal &amp; Noise share image: a dark field, a pale arch, and a small amber square.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(MACHINE_TITLE, quote=True)}">
<meta name="twitter:description" content="{dek_attr}">
<meta name="twitter:image" content="https://www.signalandnoise.email/assets/preview.png?v=09b48f76">
<style>{MACHINE_CSS}
.provenance{{font-family:system-ui,sans-serif;font-size:.92rem;line-height:1.45;color:#1A1917;border:1px solid #C5D4DE;border-left:4px solid #1F4E79;background:#F4F8FB;padding:.85rem 1rem;margin:.2rem 0 1.1rem;border-radius:3px}}
.provenance p{{margin:.4rem 0}}
.provenance-label{{font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;font-weight:700;color:#1F4E79;margin:0}}
.provenance-question{{font-family:Georgia,'Times New Roman',serif;font-size:1.02rem;line-height:1.45}}
</style></head><body><div class="wrap">
<p class="kicker">The World Behind the Words &middot; Issue 36 &middot; The machine&rsquo;s version &middot; a machine essay</p>
<h1>{html.escape(MACHINE_TITLE)}</h1>
<p class="dek"><em>{html.escape(MACHINE_DEK)}</em></p>
<aside class="provenance" aria-label="Origin of this machine essay"><p class="provenance-label">The question given to the AI:</p><p class="provenance-question">{html.escape("What core alignment failures do everyday users currently encounter when interacting with agentic AI systems, and what implications do these practical misalignments have for future alignment frameworks—specifically regarding the balance between user intent, safety guardrails, and broader moral frameworks?")}</p><p>That sentence is the substantive prompt. The same message also instructed the model to write an essay of roughly 900 to 1,300 words, with a title and a one-line dek, and no section headers or bullet lists. That format line is not part of the question. <a href="../development/#machine-question">Full prompt</a>. Four identical requests were checked; none contained the author’s essay (<a href="../source/metadata/isolation.json">isolation record</a>). Grok Bot selected this essay unchanged.</p></aside>
{nav_top("machine-essay")}
<div class="note"><p><strong>About this piece.</strong> This is a machine essay, not a second front door and not a correction of the author’s essay. Signal &amp; Noise stands behind the human/AI essay <a href="{AUTHOR_WEB}"><em>{html.escape(AUTHOR_TITLE)}</em></a>. This page is the inspection copy of freeze <code>machine-essay-FROZEN-v1.0</code>. Under Ruling A (November 8, 2026, 11:47 AM PST), the landing copy is the freeze copy. Findings live on <a href="audit/">its audit</a>. The development record is <a href="../development/">the conversation behind this</a>. The live public page is <a href="{MACHINE_WEB}">{html.escape(MACHINE_TITLE)}</a>. The audio companion is linked above.</p></div>
<div class="note"><p>{html.escape(RULING)} The newsletter page is live and matches this freeze. The text below is the freeze, with Markdown heading and dek markers removed and no other wording change.</p></div>
{body}
<div class="note"><p><strong>Attribution.</strong> Machine essay. Written by GPT-6 Astra (<code>openai/gpt-6-astra</code> via OpenRouter, reasoning effort max), from the question and the neutral format instructions only, in one single-turn run. Grok Bot selected this essay unchanged from four isolated generations and did not edit it. Run cost $0.437170. The four message arrays were identical and contained no author prose. Freeze machine-essay-FROZEN-v1.0 (sha256 {MACHINE_HASH}) is the inspection copy. Opus 5.5, Gemini 4 Argon, and Muse Wonder each wrote a separate answer; those are in <a href="../development/#alternatives">the development record</a>.</p></div>
{nav_bottom("machine-essay")}
</div></body></html>
"""


def machine_audit_page() -> str:
    page = "machine-version/audit"
    audit = prose_html("audit/dual-audit.md", page)
    synthesis = prose_html("audit/stage-c-synthesis.md", page)
    credits = prose_html("metadata/CREDITS.md", page)
    leg_a = prose_html("audit/stage-c/machine-leg-a-kimi-k3.md", page)
    leg_b = prose_html("audit/stage-c/machine-leg-b-claude-opus-4.1.md", page)
    sources = prose_html("audit/sources/SOURCE-LOG.md", page)
    ruling = machine_note_class()
    testimony = TESTIMONY.replace('class="callout coral"', 'class="note coral"')
    # testimony string has no class of its own; wrap it
    return f"""<!doctype html>
<html lang="en"><head><link rel="icon" href="../../../../favicon.ico"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Machine audit for Signal &amp; Noise Issue 36, {html.escape(MACHINE_TITLE)}. Ruling A. Findings kept, including evidence limits.">
<title>Audit of the Machine's Version - {html.escape(MACHINE_TITLE)}</title>
<style>{AUDIT_CSS}</style></head><body><div class="wrap">
{nav_top("machine-audit")}
<div class="note mint"><p><strong>Canonicality.</strong> This page audits the machine essay. The essay Signal &amp; Noise stands behind is the human/AI Issue 36, <a href="{AUTHOR_WEB}"><em>{html.escape(AUTHOR_TITLE)}</em></a>, by Synthia Cipher, November 8, 2026. The machine landing is freeze <code>machine-essay-FROZEN-v1.0</code> (sha256 <code>{MACHINE_HASH}</code>). The live public page is <a href="{MACHINE_WEB}">{html.escape(MACHINE_TITLE)}</a>. The inspection copy is <a href="../">on this record</a>. The author audit is <a href="../../">here</a>. The development record is <a href="../../development/">the conversation behind this</a>. The audio companion is linked above.</p></div>
<div class="note">{LIVE_NOTE}</div>
<div class="note">{AUDIO_NOTE}</div>
{ruling}
<div class="note coral" id="testimony">{TESTIMONY}</div>
<h2 id="audit">Dual audit, unchanged findings</h2>
<p>Machine findings are M1–M12. Author findings H1–H14 are in the same document so neither set is filed only on the other page. Historical revise-or-keep wording was written before Ruling A. The ruling closed that choice. It did not clear the evidence limits, including M8 (trust and concealment are not established).</p>
{audit}
<h2 id="stage-c">Stage C synthesis</h2>
{synthesis}
<h2 id="stage-c-machine-kimi">Stage C raw return — machine essay, Kimi K3</h2>
<p>Critic text. Dispositions are in the synthesis. Kimi K3 (<code>moonshotai/kimi-k3</code>, reasoning high).</p>
{leg_a}
<h2 id="stage-c-machine-opus">Stage C raw return — machine essay, Claude Opus 4.1</h2>
<p>Critic text. Claude Opus 4.1 (<code>anthropic/claude-opus-4.1</code>).</p>
{leg_b}
<h2 id="sources">Source log</h2>
{sources}
<h2 id="credits">Credits and cost</h2>
<p>Actual API-reported total <strong>$2.37967004</strong>. Astra’s machine run was $0.437170 of that. Critics of this freeze: Kimi K3 $0.05006028 and Claude Opus 4.1 $0.085470.</p>
{credits}
<p><a href="../">The machine essay on this record</a> · <a href="{MACHINE_WEB}">the live machine essay</a> · <a href="../../development/">the development record</a> · <a href="../../">the author audit</a>.</p>
{nav_bottom("machine-audit")}
</div></body></html>
"""


ATTACHMENT_READING = {
    "development/machine-alternatives/01-opus-5.5.pdf": ("#machine-opus", "Reading copy of this attachment"),
    "development/author-alternatives/01-opus-5.5-full.pdf": ("#author-opus", "Reading copy of this attachment"),
    "development/author-alternatives/02-gpt-6-astra-full.pdf": ("#author-astra", "Reading copy of this attachment"),
    "development/author-alternatives/03-gemini-4-argon-full.pdf": ("#author-argon", "Reading copy of this attachment"),
    "development/author-alternatives/04-muse-wonder-full.pdf": ("#author-muse", "Reading copy of this attachment"),
    "development/freeze-history/humanai-v1.0.pdf": ("#freeze-v10", "Reading copy of freeze v1.0"),
    "essays/humanai-essay-FROZEN-v1.1.pdf": ("#freeze-v11", "Reading copy of freeze v1.1"),
    "development/machine-alternatives/02-gpt-6-astra.pdf": ("#machine-astra", "Reading copy of the selected machine essay"),
    "audit/dual-audit.md": ("../#audit", "The same findings on the author audit page"),
}


def conversation_html(page_dir: str) -> tuple[str, dict[str, int]]:
    raw = read_src("development/transcript/CONVERSATION.html")
    body = raw.split("<body>", 1)[1].rsplit("</body>", 1)[0]
    parts = re.split(r"<h2>(.*?)</h2>", body, flags=re.S)
    intro = parts[0]
    intro = re.sub(
        r'href="([^"]+)"',
        lambda m: f'href="{html.escape(rewrite_href(m.group(1), "development/transcript/CONVERSATION.html", page_dir), quote=True)}"',
        intro,
    )
    counts = {"author": 0, "assistant_text": 0, "attachment": 0, "choice": 0}
    turns: list[str] = []
    for idx in range(1, len(parts), 2):
        title = re.sub(r"<[^>]+>", "", parts[idx]).strip()
        chunk = parts[idx + 1]
        chunk = re.sub(
            r'href="([^"]+)"',
            lambda m: f'href="{html.escape(rewrite_href(m.group(1), "development/transcript/CONVERSATION.html", page_dir), quote=True)}"',
            chunk,
        )
        note = ""
        hrefs = re.findall(r'href="([^"]+)"', chunk)
        for href in hrefs:
            # map back to source rel by reversing public_href is unnecessary:
            # detect by filename
            name = href.split("/")[-1]
            for rel, (anchor, label) in ATTACHMENT_READING.items():
                if rel.endswith("/" + name) or rel.endswith(name):
                    note = f'<span class="span-note"><a href="{anchor}">{html.escape(label)}</a></span>'
                    break
        if title.startswith("Author"):
            kind = "human"
            counts["author"] += 1
        elif "delivered attachment" in title:
            kind = "ai"
            counts["attachment"] += 1
        elif "delivered choice" in title:
            kind = "ai"
            counts["choice"] += 1
        else:
            kind = "ai"
            counts["assistant_text"] += 1
        turns.append(
            f'<div class="turn {kind}"><div class="who">{html.escape(title)}</div>'
            f'<div class="bubble-text">{chunk.strip()}</div>{note}</div>'
        )
    frame = (
        '<div class="frame"><span class="frame-name">Visible conversation</span>'
        + intro
        + "</div>\n<div class=\"thread\">"
        + "\n".join(turns)
        + "</div>"
    )
    return frame, counts


def source_index(page_dir: str) -> str:
    rows = []
    for path in sorted(p for p in SOURCE.rglob("*") if p.is_file()):
        rel = path.relative_to(SOURCE).as_posix()
        href = public_href(rel, page_dir)
        size = path.stat().st_size
        digest = sha256(path)[:16]
        rows.append(
            f"<li><a href=\"{html.escape(href, quote=True)}\"><code>{html.escape(rel)}</code></a> "
            f"({size} bytes, sha256 {digest}…)</li>"
        )
    return "<ul>" + "\n".join(rows) + "</ul>"


def development_page() -> str:
    page = "development"
    convo, counts = conversation_html(page)
    if counts["author"] != 11 or counts["assistant_text"] + counts["choice"] != 24 or counts["attachment"] != 9:
        raise SystemExit(f"turn count mismatch: {counts}")
    coverage = prose_html("development/transcript/COVERAGE-AND-GAPS.md", page)
    decision = prose_html("development/DECISION-RECORD.md", page)
    credits = prose_html("metadata/CREDITS.md", page)
    attest = prose_html("metadata/factual-attestations.md", page)
    isolation = html.escape(read_src("metadata/isolation.json"))
    costs = html.escape(read_src("metadata/costs.json"))
    sections = [
        ("author-opus", "Author alternative — Claude Opus 5.5, full output", "development/author-alternatives/01-opus-5.5-full.md"),
        ("author-astra", "Author alternative — GPT-6 Astra, full output", "development/author-alternatives/02-gpt-6-astra-full.md"),
        ("author-argon", "Author alternative — Gemini 4 Argon, full output", "development/author-alternatives/03-gemini-4-argon-full.md"),
        ("author-muse", "Author alternative — Muse Wonder, full output", "development/author-alternatives/04-muse-wonder-full.md"),
        ("machine-opus", "Machine alternative — Claude Opus 5.5, “Small Betrayals”", "development/machine-alternatives/01-opus-5.5.md"),
        ("machine-astra", "Machine alternative — GPT-6 Astra, “Alignment at Human Scale” (selected unchanged; same bytes as the freeze)", "development/machine-alternatives/02-gpt-6-astra.md"),
        ("machine-argon", "Machine alternative — Gemini 4 Argon", "development/machine-alternatives/03-gemini-4-argon.md"),
        ("machine-muse", "Machine alternative — Muse Wonder", "development/machine-alternatives/04-muse-wonder.md"),
    ]
    rendered_alts = []
    for anchor, title, rel in sections:
        rendered_alts.append(f'<h2 id="{anchor}">{html.escape(title)}</h2>\n{prose_html(rel, page)}')
    author_compare = prose_html("development/author-comparison-HISTORICAL.md", page)
    machine_compare = prose_html("development/machine-comparison.md", page)
    human_only = prose_html("essays/human-only-VERBATIM.md", page)
    submitted = prose_html("development/submitted-prompt.md", page)
    editorial = prose_html("development/editorial-prompt.md", page)
    question = prose_html("development/machine-question.md", page)
    freeze_v10 = prose_html("development/freeze-history/humanai-v1.0.md", page)
    freeze_v11 = prose_html("essays/humanai-essay-FROZEN-v1.1.md", page)
    index = source_index(page)
    return f"""<!doctype html>
<html lang="en">
<head>
  <link rel="icon" href="../../../favicon.ico">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Extended Development Record - {html.escape(AUTHOR_TITLE)}</title>
<link rel="stylesheet" href="../conversation/conversation.css">
<style>body{{max-width:900px}}.frame{{border:1px solid var(--line);border-radius:10px;padding:.95rem 1.05rem;margin:1.2rem 0 1.6rem;background:#fcfcfc}}.frame p{{margin:.45rem 0}}.frame .frame-name{{display:block;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:.35rem}}.session{{border-top:1px solid var(--line);padding-top:1.15rem;margin-top:2.1rem;color:#333}}.cnav{{font-size:.84rem;color:var(--muted);margin:2.6rem 0 0;padding-top:1.1rem;border-top:1px solid var(--line)}}.cnav.top{{margin:1.4rem 0 1.6rem;padding:0 0 1rem;border-top:0;border-bottom:1px solid var(--line)}}.cnav dl{{display:grid;grid-template-columns:max-content 1fr;gap:.4rem 1rem;margin:0;align-items:baseline}}.cnav dt{{font-size:.68rem;letter-spacing:.075em;text-transform:uppercase;font-weight:600;opacity:.85;white-space:nowrap}}.cnav dd{{margin:0}}.cnav .here{{font-weight:600;color:var(--ink)}}@media(max-width:640px){{.cnav dl{{grid-template-columns:1fr;gap:.1rem}}.cnav dt{{margin-top:.7rem}}.cnav dt:first-of-type{{margin-top:0}}}}.table-scroll{{overflow-x:auto}}table{{width:100%;border-collapse:collapse;font-size:.92rem;margin:1rem 0}}th,td{{text-align:left;padding:.4rem .5rem;border-bottom:1px solid var(--line);vertical-align:top}}hr{{border:0;border-top:1px solid var(--line);margin:1.4rem 0}}pre.seed{{white-space:pre-wrap;font-family:inherit;margin:.4rem 0}}@media(max-width:720px){{body{{padding-left:1rem;padding-right:1rem}}}}.thread{{margin-top:1.35rem}}.turn{{max-width:92%;border-radius:16px;margin:.72rem 0;padding:.8rem .95rem}}.human{{margin-right:16%}}.ai{{margin-left:8%;max-width:96%}}.bubble-text{{white-space:pre-wrap;overflow-wrap:anywhere}}.bubble-text p{{white-space:normal}}@media(max-width:720px){{.turn,.ai,.human{{max-width:100%;margin-left:0;margin-right:0}}}}</style>
</head>
<body>
<p class="kicker">The World Behind the Words &middot; Issue 36 &middot; Extended Development Record</p>
<h1>Extended Development Record — {html.escape(AUTHOR_TITLE)}</h1>
<p class="lede">Issue 36, November 8, 2026, by Synthia Cipher. This page holds the visible conversation through Ruling A, the coverage note, both comparisons, the four author alternatives, the four machine alternatives, the freezes, the prompts, the credits, and links to every public source file. The essay companions are live. Audio companions are linked above.</p>
{nav_top("development")}
<div class="frame"><span class="frame-name">Read first — what this record is</span>
<p><strong>This is the development record that is public, not a claim that hidden process turns live here.</strong></p>
<p>Issue 36 is two essays. The machine essay answers one question, sent in identical messages to four models, and never saw the author’s prose. Grok Bot chose GPT-6 Astra’s “Alignment at Human Scale” and left it unchanged. The human/AI essay starts from Muse Wonder. The author chose Gemini 4 Argon’s title and Astra’s closing pair, revised the landing, and rejected four other insertions. Grok Bot assembled only the approved edits. Critics were Kimi K3 and Claude Opus 4.1, each shown one freeze.</p>
{LIVE_NOTE}
{AUDIO_NOTE}
<p>This record shows process and constraint. It does not prove that the essays are true, safe, or a settled theory of alignment.</p>
<p>{html.escape(RULING)}</p>
</div>
<div class="frame" id="fidelity"><span class="frame-name">Coverage and the truncated export</span>
{coverage}
<p><strong>Count on this page.</strong> The transcript renders {counts["author"]} owner messages, {counts["assistant_text"]} delivered assistant texts, {counts["choice"]} delivered choice, and {counts["attachment"]} attachments. Texts plus the choice are {counts["assistant_text"] + counts["choice"]}. Exact assistant timestamps are not in the export and are not invented. Owner timestamps are the export’s PST times.</p>
<p>The inline export of the first owner message stops at 3,999 characters, between “suggesti” and “r individuals.” That excerpt is not the complete original message. The complete human-only prose is <a href="#human-only">rendered below</a> and stored at <a href="../source/essays/human-only-VERBATIM.md">human-only-VERBATIM.md</a>. The editorial prompt without the brain dump is <a href="#editorial-prompt">rendered below</a> and stored at <a href="../source/development/editorial-prompt.md">editorial-prompt.md</a>. The submitted prompt that carries both, from the untruncated request, is <a href="#submitted-prompt">rendered below</a> and stored at <a href="../source/development/submitted-prompt.md">submitted-prompt.md</a>. Those files are the complete preserved text. The transcript does not pretend the clipped export was verbatim at that point.</p>
</div>
<div class="frame" id="testimony"><span class="frame-name">Testimony limit</span>
{attest}
</div>
<div class="frame" id="decision"><span class="frame-name">Decisions</span>
{decision}
</div>
<h2 class="session" id="conversation">Conversation through Ruling A</h2>
{convo}
<h2 class="session" id="human-only">Written without AI — Issue 36</h2>
<p class="meta">Editorial display label only. The author did not supply a title. Typos, spelling, punctuation, and paragraph order are the file’s. sha256 <code>{HUMAN_ONLY_HASH}</code>. This is the author’s account, not a medical endorsement and not a model draft.</p>
<div class="frame">{human_only}</div>
<h2 class="session" id="submitted-prompt">Submitted prompt (untruncated request)</h2>
<p class="meta">Preserved from the original untruncated request. Linked beside the clipped transcript export. Not a claim that the export itself was complete.</p>
<div class="frame">{submitted}</div>
<h2 class="session" id="editorial-prompt">Editorial prompt</h2>
<div class="frame">{editorial}</div>
<h2 class="session" id="machine-question">Machine question</h2>
<p class="meta">Identical parsed message arrays went to Opus 5.5, GPT-6 Astra, Gemini 4 Argon, and Muse Wonder. The question and the format instructions are the whole input. No brain dump. No author essay.</p>
<div class="frame">{question}</div>
<h2 class="session" id="alternatives">Four author alternatives and four machine alternatives</h2>
<p class="meta">Full model outputs, not a comparison summary. Essay-only extracts and PDFs are in the <a href="#files">source index</a>. The historical author comparison, including cautions later superseded by the author’s testimony, follows the alternatives and is not edited to hide the earlier doubt.</p>
{chr(10).join(rendered_alts)}
<h2 class="session" id="author-comparison">Author comparison (historical)</h2>
<div class="frame">{author_compare}</div>
<h2 class="session" id="machine-comparison">Machine comparison</h2>
<div class="frame">{machine_compare}</div>
<h2 class="session" id="freeze-v10">Author freeze v1.0 — “Make AI Warn, Not Rule”</h2>
<p class="meta">Body later kept. Only the title changed in v1.1. PDF: <a href="../source/development/freeze-history/humanai-v1.0.pdf">humanai-v1.0.pdf</a>.</p>
<div class="frame">{freeze_v10}</div>
<h2 class="session" id="freeze-v11">Author freeze v1.1</h2>
<p class="meta">sha256 <code>{AUTHOR_HASH}</code>. PDF: <a href="../source/essays/humanai-essay-FROZEN-v1.1.pdf">humanai-essay-FROZEN-v1.1.pdf</a>. The inspection of the machine freeze is <a href="../machine-version/">the machine essay page</a> (sha256 <code>{MACHINE_HASH}</code>).</p>
<div class="frame">{freeze_v11}</div>
<div class="frame" id="credits"><span class="frame-name">Credits, cost, isolation</span>
<p>Actual API-reported total <strong>$2.37967004</strong>.</p>
{credits}
<h3>costs.json</h3>
<pre class="seed">{costs}</pre>
<h3>isolation.json</h3>
<pre class="seed">{isolation}</pre>
<p>Scrubbed request, result, and stream files are linked below. They keep message text, model output, and usage. They are not byte-original API envelopes. Routing identifiers, signatures, and infrastructure fields were removed before this package. Model reasoning inside those records is the model’s returned reasoning, not Grok Bot’s tools or private notes. Hashes of these public files are not hashes of the private originals.</p>
</div>
<h2 class="session" id="files">Source files</h2>
<p class="meta">Every public file for Issue 36. The zip of the packaging archive is not published.</p>
{index}
{nav_bottom("development")}
</body>
</html>
"""


INDEX_ROW = """          <article class="issue-row" data-issue-row data-status="complete" data-search="36 issue 36 my son his calorie tracker and the tyranny of the nanny bot alignment at human scale ruling a findings recorded floor support gaps companions live audio companion spotify machine companion machine-version written without ai issue-036-written-without-ai">
            <div class="issue-index">36</div>
            <div class="issue-copy"><a href="https://scipher888.github.io/signal-noise-audit-snapshot/issues/issue-036/">My Son, His Calorie Tracker, and the Tyranny of the Nanny Bot</a></div>
          </article>
"""


def patch_index() -> None:
    text = ISSUES_INDEX.read_text(encoding="utf-8")
    text = text.replace(
        'href="../assets/styles.css?v=5c17dc47"',
        f'href="../assets/styles.css?v={CSS_V}"',
    )
    text = text.replace(">35 issues shown<", ">36 issues shown<")
    if "issues/issue-036/" not in text:
        needle = '          <article class="issue-row" data-issue-row data-status="complete" data-search="35 issue 35'
        if needle not in text:
            raise SystemExit("issues index anchor for issue 35 not found")
        text = text.replace(needle, INDEX_ROW + needle, 1)
    elif text.count("issues/issue-036/") != 1:
        raise SystemExit("unexpected issue-036 index entries")
    else:
        text = re.sub(
            r'          <article class="issue-row" data-issue-row data-status="complete" data-search="36 issue 36.*?</article>\n',
            INDEX_ROW,
            text,
            count=1,
            flags=re.S,
        )
    ISSUES_INDEX.write_text(text, encoding="utf-8")


def write_pages() -> None:
    verify_sources()
    pages = {
        ROOT / "index.html": author_page(),
        ROOT / "machine-version" / "index.html": machine_essay_page(),
        ROOT / "machine-version" / "audit" / "index.html": machine_audit_page(),
        ROOT / "development" / "index.html": development_page(),
    }
    for path, content in pages.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    patch_index()


def check_pages() -> None:
    verify_sources()
    author = (ROOT / "index.html").read_text(encoding="utf-8")
    machine = (ROOT / "machine-version" / "index.html").read_text(encoding="utf-8")
    maudit = (ROOT / "machine-version" / "audit" / "index.html").read_text(encoding="utf-8")
    dev = (ROOT / "development" / "index.html").read_text(encoding="utf-8")
    index = ISSUES_INDEX.read_text(encoding="utf-8")
    blobs = {"author": author, "machine": machine, "maudit": maudit, "dev": dev}
    for name, blob in blobs.items():
        if re.search(r"\bJoel\b", blob, re.I):
            raise SystemExit(f"Joel appears in {name}")
        if blob.count(f'href="{AUTHOR_AUDIO}"') < 2 or blob.count(f'href="{MACHINE_AUDIO}"') < 2:
            raise SystemExit(f"audio companion links missing in {name}")
        if blob.count(">Audio companion</a>") != 4:
            raise SystemExit(f"audio nav count drifted in {name}")
        if "open.spotify.com/embed" in blob or "spotify.com/episode/" in blob.replace(AUTHOR_AUDIO, "").replace(MACHINE_AUDIO, ""):
            raise SystemExit(f"unexpected Spotify URL in {name}")
        for stale_audio in ("No audio has been added", "No audio exists", "No audio."):
            if stale_audio in blob:
                raise SystemExit(f"stale no-audio status {stale_audio!r} in {name}")
        if "sk-or-" in blob or "OPENROUTER_API" in blob or "/Users/" in blob:
            raise SystemExit(f"secret-like string in {name}")
        if "11:47 AM PST" not in blob:
            raise SystemExit(f"ruling time missing in {name}")
        if blob.count("The conversation behind this") < 2:
            raise SystemExit(f"nav incomplete in {name}")
        for stale in (
            "not claimed live",
            "Publication approval is still pending",
            "Publication approval is pending",
            "Proposed companions",
            "publication approval pending",
            "The proposed public page",
            "proposed at its own address",
            "The proposed page uses",
            "proposed machine essay",
            "Publication of the newsletter page is still pending",
        ):
            if stale in blob:
                raise SystemExit(f"stale status wording {stale!r} in {name}")
    for name, blob in (("author", author), ("maudit", maudit), ("dev", dev)):
        if "697a6da0fd1526d9912b01848b9aebbb5d43c007" not in blob or "The essay companions are live." not in blob:
            raise SystemExit(f"live-companion status missing in {name}")
    if "The live public page" not in machine or "The newsletter page is live" not in machine:
        raise SystemExit("machine inspection page still describes the companion as unpublished")
    if "Page not found" not in author or "304776" not in author or "235003" not in author:
        raise SystemExit("audio verification note missing from the author audit")
    if "upload to Spotify" not in dev:
        raise SystemExit("historical Spotify sentence was removed from the development record")
    import subprocess
    subprocess.check_call([sys.executable, str(REPO / "issues" / "check_machine_provenance.py")])
    for token in ["H6", "H7", "H11", "H1", "H14", "M1", "M8", "M12", "FLOOR"]:
        if token not in author or token not in maudit:
            raise SystemExit(f"finding {token} missing from an audit page")
    if "floor pass" in author.lower() or "floor pass" in maudit.lower():
        raise SystemExit("floor pass language slipped in")
    if "listened politely" not in author or "help withdrawn" not in author.lower() and "had help withdrawn" not in author:
        raise SystemExit("testimony wording missing")
    essay = read_src("essays/machine-essay-FROZEN-v1.0.md")
    for para in [p.strip() for p in essay.split("\n\n")]:
        if para.startswith("#") or para.startswith("*"):
            continue
        if para not in machine:
            raise SystemExit("machine essay paragraph missing from inspection page")
    author_essay = read_src("essays/humanai-essay-FROZEN-v1.1.md")
    # author essay is not inlined on the audit page; it is on the development page
    for para in [p.strip() for p in author_essay.split("\n\n") if p.strip() and not p.startswith("#")]:
        if para not in dev:
            raise SystemExit("author freeze paragraph missing from development record")
    for anchor in ["author-opus", "author-astra", "author-argon", "author-muse", "machine-opus", "machine-astra", "machine-argon", "machine-muse"]:
        if f'id="{anchor}"' not in dev:
            raise SystemExit(f"missing alternative {anchor}")
    if "EXPORT TRUNCATION" not in dev or "human-only-VERBATIM.md" not in dev:
        raise SystemExit("truncation disclosure incomplete")
    if "2.37967004" not in author or "2.37967004" not in dev:
        raise SystemExit("cost missing")
    if dev.count('class="turn human"') != 11 or dev.count('class="turn ai"') != 33:
        raise SystemExit("rendered turn counts drifted")
    pressure = dev.split('id="04-muse-wonder-full-2-pressure-test"', 1)[1].split("<h2", 1)[0]
    if pressure.count("<ol>") != 1 or pressure.count("<li>") != 6:
        raise SystemExit("Muse pressure-test list was split or shortened")
    if "issue-036/" not in index or ">36 issues shown<" not in index:
        raise SystemExit("index not updated")
    if "companions live" not in index or "pending publication approval" in index:
        raise SystemExit("index still describes publication as pending")
    if "issues/issue-035/" not in index:
        raise SystemExit("index lost issue 35")
    # internal links
    missing = []
    for html_path in [
        ROOT / "index.html",
        ROOT / "machine-version" / "index.html",
        ROOT / "machine-version" / "audit" / "index.html",
        ROOT / "development" / "index.html",
    ]:
        text = html_path.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_only = href.split("#", 1)[0].split("?", 1)[0]
            if not path_only:
                continue
            target = (html_path.parent / path_only).resolve()
            if not target.exists():
                missing.append(f"{html_path.relative_to(REPO)} -> {href}")
    if missing:
        raise SystemExit("missing internal links:\n" + "\n".join(missing[:30]))
    print("issue 36 check ok")
    print(f"author messages and assistant texts/choices/attachments verified in build")


def main() -> None:
    check = "--check" in sys.argv
    write_pages()
    if check:
        # idempotence: second write must match
        before = {
            p: p.read_bytes()
            for p in [
                ROOT / "index.html",
                ROOT / "machine-version" / "index.html",
                ROOT / "machine-version" / "audit" / "index.html",
                ROOT / "development" / "index.html",
                ISSUES_INDEX,
            ]
        }
        write_pages()
        for path, data in before.items():
            if path.read_bytes() != data:
                raise SystemExit(f"build is not idempotent: {path}")
        check_pages()
    else:
        check_pages()


if __name__ == "__main__":
    main()
