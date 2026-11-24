#!/usr/bin/env python3
"""Rebuild Issue 38 audit pages from issues/issue-038/source.

Adapted from issues/issue-037/build.py (same Markdown renderer, page shells,
chat-bubble development record and derived index count). Frozen Markdown
hashes are checked and never rewritten. Issue 38 is live: its three newsletter
companions were merged (web PR 69), its two Spotify audio companions are
linked, and its two video shorts on X are linked between each essay and its
audio companion. The source page is the author's own brain dump, all of it written
without AI, with one private link removed at the author's request.

    python3 issues/issue-038/build.py
    python3 issues/issue-038/build.py --check
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

AUTHOR_HASH = "7fb4fac57b37dc59fd13dd94ee3dba5aad6f3d26ea8054d0e70a203c7678bdb7"
AUTHOR_V1_HASH = "48d3a7271fd878c6f39eeb4e4083c68037ecb7daf3877ec9e78b0d02243554ff"
AUTHOR_V2_HASH = "3587b03b33de5eb961c6c74feb93379c73cf23e95dc2c68c4d0545aaee037270"
MACHINE_HASH = "0a62289067f3645965fccf1cdfddf35a5f97d470cc413ca53bb3ae4188f21800"
SOURCE_MATERIAL_HASH = "78c9c61cdbf7cb233c22d4a90ee39bac9845fbd052731ffa17f137aeb8935faa"
COST_TOTAL = Decimal("5.284401")
AUDIT_COST = "0.256914"

AUTHOR_WEB = "https://www.signalandnoise.email/p/the-smartest-people-in-the-room-are-the-easiest-to-fool/"
MACHINE_WEB = "https://www.signalandnoise.email/p/what-intelligence-cant-tell-you-about-your-own-life/"
SOURCE_WEB = "https://www.signalandnoise.email/p/issue-038-source-material/"
AUTHOR_AUDIO = "https://open.spotify.com/episode/5OFFH1zNdvsnvBcVFcC9MT"
MACHINE_AUDIO = "https://open.spotify.com/episode/7dHpfFFhp5RkpHi1R9QKgX"
AUTHOR_VIDEO = "https://x.com/signalnoisepub/status/2125026855271215228"
MACHINE_VIDEO = "https://x.com/signalnoisepub/status/2125027313536708685"
CSS_V = "de2cc137"
JS_V = "0c872f22"

AUTHOR_TITLE = "The Smartest People in the Room Are the Easiest to Fool"
MACHINE_TITLE = "What Intelligence Can't Tell You About Your Own Life"
MACHINE_DEK = "Brainpower is good at getting people what they want and much less good at telling them what that is."
QUESTIONS = (
    "To what extent, if any, does intelligence help people make wise life choices involving needs, wants, desires, and emotions? And what, if anything, does that imply about how highly intelligent people should approach these decisions that can have a major impact on their quality of life?",
)

RULING = (
    "Rulings confirmed November 21, 2026: a one-phrase Ruling B for finding A1 "
    "(\u201cstaffers at OpenAI\u201d became \u201cstaffers at top AI labs\u201d), and Ruling A for A2\u2013A8 and the machine essay. "
    "The author then merged the Issue 38 pull requests (this record, PR 54, at 9:33:37 PM PST; the newsletter pages, PR 69, at 9:33:53 PM PST)."
)
STATUS = RULING
WEB_MERGE = "195a0d585dcdfa4826aa35d0f141e918d3c76984"


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
        "essays/author-essay-FROZEN.md": AUTHOR_HASH,
        "essays/author-essay-FROZEN-v1.md": AUTHOR_V1_HASH,
        "essays/author-essay-FROZEN-v2.md": AUTHOR_V2_HASH,
        "development/revision-history/neon-clean-v2.md": AUTHOR_V1_HASH,
        "essays/machine-essay-FROZEN-v1.0.md": MACHINE_HASH,
        "development/machine-alternatives/01-claude-fable-5.2.md": MACHINE_HASH,
        "essays/source-material-PUBLIC.md": SOURCE_MATERIAL_HASH,
    }
    for rel, expect in checks.items():
        got = sha256(SOURCE / rel)
        if got != expect:
            raise SystemExit(f"frozen hash changed for {rel}: {got}")
    costs = json.loads(read_src("metadata/costs.json"))
    total = sum(Decimal(run["actual_api_reported_usd"]) for run in costs["runs"])
    if total != COST_TOTAL or Decimal(costs["actual_api_reported_total"]) != COST_TOTAL:
        raise SystemExit(f"cost ledger {total} != {COST_TOTAL}")
    # v3 differs from v1 by one phrase only
    v1 = read_src("essays/author-essay-FROZEN-v1.md")
    v3 = read_src("essays/author-essay-FROZEN.md")
    if v1.replace("staffers at OpenAI", "staffers at top AI labs", 1) != v3:
        raise SystemExit("author freeze v3 is not v1 with the one approved phrase change")


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
    """Companion nav. Same labels on every Issue 38 surface."""

    def item(key: str, href: str, label: str) -> str:
        if key == page:
            return f'<span class="here" aria-current="page">{label}</span>'
        return f'<a href="{href}">{label}</a>'

    rel = {
        "author-audit": {"author-audit": "", "machine-essay": "machine-version/", "machine-audit": "machine-version/audit/", "development": "development/"},
        "machine-essay": {"author-audit": "../", "machine-essay": "", "machine-audit": "audit/", "development": "../development/"},
        "machine-audit": {"author-audit": "../../", "machine-essay": "../", "machine-audit": "", "development": "../../development/"},
        "development": {"author-audit": "../", "machine-essay": "../machine-version/", "machine-audit": "../machine-version/audit/", "development": ""},
    }[page]
    sep = " &middot; "
    author = sep.join([
        item("essay", AUTHOR_WEB, "The essay"),
        f'<a href="{AUTHOR_VIDEO}">Video short</a>',
        f'<a href="{AUTHOR_AUDIO}">Audio companion</a>',
        item("author-audit", rel["author-audit"], "The audit"),
    ])
    machine = sep.join([
        item("machine-essay", rel["machine-essay"], "The essay"),
        f'<a href="{MACHINE_VIDEO}">Video short</a>',
        f'<a href="{MACHINE_AUDIO}">Audio companion</a>',
        item("machine-audit", rel["machine-audit"], "The audit"),
    ])
    source = item("source", SOURCE_WEB, "The piece")
    convo = item("development", rel["development"], "The conversation behind this")
    return (
        f'<nav class="cnav {{klass}}" aria-label="Issue 38 companions"><dl>'
        f"<dt>The author&rsquo;s</dt><dd>{author}</dd>"
        f"<dt>The machine&rsquo;s</dt><dd>{machine}</dd>"
        f"<dt>Source material</dt><dd>{source}</dd>"
        f"<dt>Both, verbatim</dt><dd>{convo}</dd>"
        f"</dl></nav>"
    )


def nav_top(page: str) -> str:
    return cnav(page).replace("{klass}", "top")


def nav_bottom(page: str) -> str:
    return cnav(page).replace("{klass}", "")


PREP_NOTE = (
    "<p><strong>The essay companions are live.</strong> "
    "Signal &amp; Noise web pull request 69 was merged November 21, 2026, 9:33:53 PM PST, "
    f"commit <code>{WEB_MERGE}</code>. "
    "Rechecked for this record at about 9:40 PM PST: each of the three pages returned HTTP 200, and the essay text on each live page "
    "rebuilds to its freeze hash. The source page reproduces the published brain dump, with the private link removed. "
    "This audit record is the inspection surface for those live pages.</p>"
)

AUDIO_NOTE = (
    "<p><strong>Audio companions are published Spotify episodes.</strong> "
    "These are plain canonical links. This record does not embed a player and does not store audio files. "
    f'Author: <a href="{AUTHOR_AUDIO}">{html.escape(AUTHOR_TITLE)}</a>. '
    "oEmbed, the canonical page, the embed, and a headless browser load each returned that title on November 21, 2026, about 10:23 PM PST. "
    "The embed duration field is 278105 ms, which rounds to 4:38. "
    f'Machine: <a href="{MACHINE_AUDIO}">{html.escape(MACHINE_TITLE)}</a>. '
    "oEmbed, the canonical page, the embed, and a headless browser load each returned that title at the same time. "
    "The embed duration field is 270007 ms, which rounds to 4:30. "
    "Both narrations are xAI eve voice at 1.5&times;: title, dek, and the full frozen text, with no added intro or outro. "
    "As in Issue 37, the machine essay&rsquo;s question-provenance note is on the page and is not spoken. "
    "The reported API total does not include text-to-speech charges, which the service did not report, and none are added here.</p>"
)
VIDEO_NOTE = (
    "<p><strong>Video shorts are published posts on X.</strong> "
    "These are plain canonical links. This record does not embed a player and does not store video files. "
    f'Author: <a href="{AUTHOR_VIDEO}">{html.escape(AUTHOR_TITLE)}</a>. '
    "A direct fetch returned HTTP 200, and an API read on November 23, 2026, about 4:50 PM PST, returned the post and a video attachment from @signalnoisepub. "
    "The post time is 4:40 PM PST. "
    "The duration field is 41280 ms, which rounds to 0:41. "
    "The post says it is a 41-second video take on the essay, made with Gemini 4 Neon. "
    "It was made with Gemini 4 Neon at high, with an eve voiceover. "
    f'Machine: <a href="{MACHINE_VIDEO}">{html.escape(MACHINE_TITLE)}</a>. '
    "A direct fetch returned HTTP 200, and an API read returned that post and a video attachment. "
    "The post time is 4:42 PM PST. "
    "The duration field is 42304 ms, which rounds to 0:42. "
    "The post says it is Gemini 4 Neon&rsquo;s video interpretation of Claude Fable 5.2&rsquo;s essay. "
    "It is Neon&rsquo;s interpretation of that essay, not Fable&rsquo;s own video.</p>"
)
LIVE_MARK = "The essay companions are live."

RULING_BLOCK = f"""<div class="callout coral" id="ruling"><p>{html.escape(STATUS)}</p>
<ul>
<li>Author freeze <code>author-essay-FROZEN.md</code> (v3), sha256 <code>{AUTHOR_HASH}</code>. It is Gemini 4 Neon&rsquo;s draft with two Muse Wonder insertions the author approved, plus one phrase the author changed after the audit: &ldquo;staffers at OpenAI&rdquo; became &ldquo;staffers at top AI labs&rdquo;. v1 (<code>{AUTHOR_V1_HASH[:12]}&hellip;</code>, the text the critics saw) and v2 (<code>{AUTHOR_V2_HASH[:12]}&hellip;</code>) are kept in the source tree.</li>
<li>Machine freeze <code>machine-essay-FROZEN-v1.0</code>, sha256 <code>{MACHINE_HASH}</code>. It is Claude Fable 5.2&rsquo;s essay, unchanged. Its bytes match machine alternative 01.</li>
<li>The fact checks the author kept out of the essay are findings A1&ndash;A10 and M1&ndash;M9 below. At the author&rsquo;s ruling they appear only in this audit; the newsletter page carries no corrective note above the essay. None is blocking under the floor definition, and none is described as a pass.</li>
<li>Video shorts are the two published X posts in the navigation, between the essay and the audio companion. This repository does not store a video file. The machine short is Gemini 4 Neon&rsquo;s video interpretation of Claude Fable 5.2&rsquo;s essay, not Fable&rsquo;s own video.</li>
<li>Audio companions are the two published Spotify episode links in the navigation. This repository does not store an audio file.</li>
<li>The dual audit, Stage C synthesis and execution method were written before publication. Their pre-publication status sentences are historical. The rulings closed those choices; they did not withdraw any finding.</li>
</ul>
<p>This is an editorial disposition. It does not certify that the essays are true.</p></div>"""


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
          <h3>Issue 38</h3>
          <a href="{AUTHOR_WEB}">Read the issue</a>
          <a href="machine-version/">The machine&rsquo;s version</a>
          <a href="{SOURCE_WEB}">The source material</a>
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


SRC_CSS = (
    ".src-legend{display:flex;flex-wrap:wrap;gap:.4rem 1.4rem;margin:0 0 1rem;padding:.7rem .9rem;border:1px solid rgba(0,0,0,.1);border-radius:8px;font-family:system-ui,sans-serif;font-size:.86rem}"
    ".src-legend p{margin:0}"
    ".src-key{display:inline-block;margin-right:.35rem;padding:.08rem .45rem;border-radius:3px;font-weight:700;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase}"
    ".src-key-h{background:#fbe9d0;color:#7a1f1f;border-left:3px solid #7a1f1f}"
    ".src-mix{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.65}"
)


def source_material_html() -> str:
    text = read_src("essays/source-material-PUBLIC.md")
    legend = (
        '<div class="src-legend" role="note" aria-label="Legend">'
        '<p><span class="src-key src-key-h">Synthia</span> Everything here was written by Synthia Cipher, without AI.</p>'
        "<p>By the author&rsquo;s own account it is intuition, not research.</p></div>"
    )
    return legend + f'<div class="src-mix">{html.escape(text, quote=False)}</div>' + (
        f"<p class=\"meta\">{words(text)} words. Verbatim, typos kept, with two changes the author approved: the private link "
        "is replaced by [private link removed], and tracking parameters are removed from the two X links. "
        f"sha256 of the published text <code>{SOURCE_MATERIAL_HASH}</code>.</p>"
    )


def provenance_aside(prefix: str) -> str:
    qs = "".join(f'<p class="provenance-question">{html.escape(q)}</p>' for q in QUESTIONS)
    return (
        '<aside class="provenance" aria-label="Origin of this machine essay">'
        '<p class="provenance-label">The question given to the AI:</p>'
        f"{qs}"
        "<p>This question, in the author&rsquo;s own words, is the substantive prompt. "
        "The same message also asked for an essay of roughly 900 to 1,300 words with a title and a one-line dek, "
        "and no section headers or bullet lists. "
        f'<a href="{prefix}development/#machine-question">Full prompt</a>. '
        "Four identical requests contained none of the author&rsquo;s brain dump, links or drafts "
        f'(<a href="{prefix}source/metadata/isolation.json">isolation record</a>). '
        "Grok Bot recommended this essay and the author approved it; it is unchanged.</p>"
        "</aside>"
    )


def author_page() -> str:
    page = ""
    audit = prose_html("audit/dual-audit.md", page)
    synthesis = prose_html("audit/stage-c-synthesis.md", page)
    method = prose_html("audit/execution-method.md", page)
    sources = prose_html("audit/sources/SOURCE-LOG.md", page)
    credits = prose_html("metadata/CREDITS.md", page)
    rulings = prose_html("RULINGS.md", page)
    leg_a = prose_html("audit/stage-c/humanai-leg-a-kimi-k3.md", page)
    leg_b = prose_html("audit/stage-c/humanai-leg-b-claude-opus-4.1.md", page)
    author_words = words(read_src("essays/author-essay-FROZEN.md"))
    machine_words = words(read_src("essays/machine-essay-FROZEN-v1.0.md"))
    return f"""<!doctype html>
<html lang="en">
<head>
  <link rel="icon" href="../../favicon.ico">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Audit for Signal &amp; Noise Issue 38, {html.escape(AUTHOR_TITLE)}: source checks on the Huang and AI-lab reporting, Stage C objections, and a full audit of the machine essay. Rulings confirmed. Essay, video short, and audio companions are live.">
  <title>Issue 38 Published Audit - {html.escape(AUTHOR_TITLE)}</title>
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
          <div class="issue-eyebrow"><p class="eyebrow">Issue 38 &middot; November 21, 2026 &middot; Synthia Cipher</p></div>
          <h1 class="page-title">{html.escape(AUTHOR_TITLE)}</h1>
          <p class="lede">Audit for Issue 38. Intended issue date: November 21, 2026. Byline: Synthia Cipher. Companions: the <a href="{AUTHOR_WEB}">human/AI essay</a>, the <a href="{MACHINE_WEB}">machine essay</a>, and the <a href="{SOURCE_WEB}">source material</a>, which is the author&rsquo;s own brain dump, written without AI. Video shorts and audio companions are linked below.</p>
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
            {PREP_NOTE}
            {VIDEO_NOTE}
            {AUDIO_NOTE}
            <div class="callout mint"><p><strong>Canonicality.</strong> The essay Signal &amp; Noise stands behind is Issue 38, <em>{html.escape(AUTHOR_TITLE)}</em>, by Synthia Cipher. This page is its audit, not a second edition and not a corrected essay. The fact checks live here, at the author&rsquo;s request, so the essay reads as the author chose. The machine essay, <a href="{MACHINE_WEB}">{html.escape(MACHINE_TITLE)}</a>, is a companion; its inspection copy is <a href="machine-version/">on this record</a>. Author freeze sha256 <code>{AUTHOR_HASH}</code> ({author_words} whitespace-delimited words in the Markdown file, title and dek included). Machine freeze sha256 <code>{MACHINE_HASH}</code> ({machine_words} whitespace-delimited words, title and dek included).</p></div>
            {RULING_BLOCK}
          </section>
          <section class="content-section" id="assembly">
            <h2>How the author essay was assembled</h2>
            <p>Four models received the author&rsquo;s editorial prompt with the brain dump. The author chose Gemini 4 Neon&rsquo;s draft, which is the only one that kept the Huang and &ldquo;consensual non-consent&rdquo; examples, and asked what else could be folded in. A redline with five short passages from Fable, Muse and Astra followed. The author kept only two, both from Muse Wonder: the Chesterton&rsquo;s fence passage, and &ldquo;An ordinary person produces an excuse. A gifted person produces a philosophy.&rdquo; Everything else is Neon verbatim. After the audit, the author changed one phrase, &ldquo;staffers at OpenAI&rdquo;, first to &ldquo;top AI lab staffers&rdquo; and then to &ldquo;staffers at top AI labs&rdquo;. See <a href="development/#decision">the development record</a>.</p>
            <p>The machine essay was not assembled. Four models received the same question and format instructions, with no source and no author essay. Claude Fable 5.2&rsquo;s essay is published unchanged. GPT-6.2 Astra, Gemini 4 Neon and Muse Wonder are the alternatives.</p>
          </section>
          <section class="content-section" id="audit">
            <h2>Dual audit</h2>
            {audit}
          </section>
          <section class="content-section" id="rulings">
            <h2>Rulings</h2>
            {rulings}
          </section>
          <section class="content-section" id="method">
            <h2>How the audit was run</h2>
            {method}
          </section>
          <section class="content-section" id="stage-c">
            <h2>Stage C synthesis</h2>
            {synthesis}
            <h2 id="stage-c-author-kimi">Stage C raw return — author essay, Kimi K3</h2>
            <p>Critic text, not a finding that every objection landed. Dispositions are in the synthesis above. Kimi K3 (<code>moonshotai/kimi-k3</code>, reasoning high). The critics saw freeze v1, which says &ldquo;staffers at OpenAI&rdquo;.</p>
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
            <p>Actual API-reported total <strong>${COST_TOTAL}</strong> across twelve paid calls, with no retries. The audit itself cost ${AUDIT_COST}. Figures are API usage reports, not a reconciled card statement.</p>
            {credits}
            <p>Per-run ledger: <a href="source/metadata/costs.json">costs.json</a>. Isolation check: <a href="source/metadata/isolation.json">isolation.json</a>.</p>
          </section>
          <section class="content-section" id="source-material">
            <h2>Source material</h2>
            <p>This issue&rsquo;s source is the author&rsquo;s raw brain dump, written without AI. By the author&rsquo;s own account it is intuition, not research. The newsletter page is <a href="{SOURCE_WEB}">Source material — Issue 38</a>. The published file is <a href="source/essays/source-material-PUBLIC.md">source-material-PUBLIC.md</a>: verbatim, except that a private link is replaced by [private link removed] and tracking parameters are removed from the two X links. The development record renders it in full.</p>
          </section>
          <section class="content-section" id="closing">
            <div class="callout mint"><p>What this audit did: it logged every author finding (A1&ndash;A10) and machine finding (M1&ndash;M9). It published the Stage C returns and their dispositions, including objections that land and objections that do not, along with the source log and the ${COST_TOTAL} cost. It did not certify the essays.</p></div>
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

PROVENANCE_CSS = """
.provenance{font-family:system-ui,sans-serif;font-size:.92rem;line-height:1.45;color:#1A1917;border:1px solid #C5D4DE;border-left:4px solid #1F4E79;background:#F4F8FB;padding:.85rem 1rem;margin:.2rem 0 1.1rem;border-radius:3px}
.provenance p{margin:.4rem 0}
.provenance-label{font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;font-weight:700;color:#1F4E79;margin:0}
.provenance-question{font-family:Georgia,'Times New Roman',serif;font-size:1.02rem;line-height:1.45}
"""


def machine_essay_page() -> str:
    body = essay_body_html("essays/machine-essay-FROZEN-v1.0.md", "machine-version", True, True)
    dek_attr = html.escape(MACHINE_DEK, quote=True)
    return f"""<!doctype html>
<html lang="en"><head><link rel="icon" href="../../../favicon.ico"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(MACHINE_TITLE)}: the machine essay for Signal &amp; Noise Issue 38, inspection copy of freeze machine-essay-FROZEN-v1.0.">
<title>The Machine's Version - {html.escape(MACHINE_TITLE)}</title>
<meta property="og:site_name" content="Signal &amp; Noise">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(MACHINE_TITLE, quote=True)}">
<meta property="og:description" content="{dek_attr}">
<meta property="og:url" content="https://scipher888.github.io/signal-noise-audit-snapshot/issues/issue-038/machine-version/">
<meta property="og:image" content="https://www.signalandnoise.email/assets/preview.png?v=09b48f76">
<meta name="twitter:card" content="summary_large_image">
<style>{MACHINE_CSS}{PROVENANCE_CSS}</style></head><body><div class="wrap">
<p class="kicker">The World Behind the Words &middot; Issue 38 &middot; The machine&rsquo;s version &middot; a machine essay</p>
<h1>{html.escape(MACHINE_TITLE)}</h1>
<p class="dek"><em>{html.escape(MACHINE_DEK)}</em></p>
{provenance_aside("../")}
{nav_top("machine-essay")}
<div class="note"><p><strong>About this piece.</strong> This is a machine essay. It is not a second front door, and it is not a correction of the author&rsquo;s essay. Signal &amp; Noise stands behind the human/AI essay <a href="{AUTHOR_WEB}"><em>{html.escape(AUTHOR_TITLE)}</em></a>. This page is the inspection copy of freeze <code>machine-essay-FROZEN-v1.0</code>. Findings live on <a href="audit/">its audit</a>. The development record is <a href="../development/">the conversation behind this</a>. The live public page is <a href="{MACHINE_WEB}">{html.escape(MACHINE_TITLE)}</a>. The video short and the audio companion are linked above. The video short is Gemini 4 Neon&rsquo;s interpretation of Claude Fable 5.2&rsquo;s essay, not Fable&rsquo;s own video.</p></div>
<div class="note">{PREP_NOTE}<p>{html.escape(RULING)} The newsletter page is live and matches this freeze. The text below is the freeze, with the Markdown heading and dek markers removed and no other wording change.</p></div>
{body}
<div class="note"><p><strong>Attribution.</strong> Machine essay. Written by Claude Fable 5.2 (<code>anthropic/claude-fable-5.2</code> via OpenRouter, reasoning effort max, max_tokens 48,000) from the question and format instructions alone, in one single-turn run that finished on its first attempt. Grok Bot recommended it from four isolated generations, the author approved it, and nobody edited it. Run cost $1.656800. Freeze sha256 <code>{MACHINE_HASH}</code>. GPT-6.2 Astra, Gemini 4 Neon and Muse Wonder each wrote a separate answer; those are in <a href="../development/#alternatives">the development record</a>.</p></div>
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
    ruling = RULING_BLOCK.replace('class="callout coral"', 'class="note coral"')
    return f"""<!doctype html>
<html lang="en"><head><link rel="icon" href="../../../../favicon.ico"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Machine audit for Signal &amp; Noise Issue 38, {html.escape(MACHINE_TITLE)}. Every named study checked; no floor defects.">
<title>Audit of the Machine's Version - {html.escape(MACHINE_TITLE)}</title>
<style>{AUDIT_CSS}</style></head><body><div class="wrap">
{nav_top("machine-audit")}
<div class="note mint"><p><strong>Canonicality.</strong> This page audits the machine essay. The essay Signal &amp; Noise stands behind is the human/AI Issue 38, <a href="{AUTHOR_WEB}"><em>{html.escape(AUTHOR_TITLE)}</em></a>, by Synthia Cipher. The machine landing is freeze <code>machine-essay-FROZEN-v1.0</code> (sha256 <code>{MACHINE_HASH}</code>). The inspection copy is <a href="../">on this record</a>. The author audit is <a href="../../">here</a>. The development record is <a href="../../development/">the conversation behind this</a>. The video short and the audio companion are linked above.</p></div>
<div class="note">{PREP_NOTE}</div>
<div class="note">{VIDEO_NOTE}</div>
<div class="note">{AUDIO_NOTE}</div>
{ruling}
<h2 id="audit">Dual audit</h2>
<p>Machine findings are M1&ndash;M9. Author findings A1&ndash;A10 are in the same document, so neither set is filed only on the other page.</p>
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
<p>Actual API-reported total <strong>${COST_TOTAL}</strong>. The selected machine run cost $1.656800. The critics of this freeze cost $0.040926 (Kimi K3) and $0.084315 (Claude Opus 4.1).</p>
{credits}
<p><a href="../">The machine essay on this record</a> · <a href="../../development/">the development record</a> · <a href="../../">the author audit</a>.</p>
{nav_bottom("machine-audit")}
</div></body></html>
"""


def source_index(page_dir: str) -> str:
    rows = []
    for path in sorted(p for p in SOURCE.rglob("*") if p.is_file()):
        rel = path.relative_to(SOURCE).as_posix()
        href = public_href(rel, page_dir)
        rows.append(
            f"<li><a href=\"{html.escape(href, quote=True)}\"><code>{html.escape(rel)}</code></a> "
            f"({path.stat().st_size} bytes, sha256 {sha256(path)[:16]}…)</li>"
        )
    return "<ul>" + "\n".join(rows) + "</ul>"


DECISION_QUOTES = {
    "request": "my brain dump is even more random, unorganized, and haphazard than usual, and it\u2019s based almost entirely on intuition since I haven\u2019t done the research to prove or disprove any of this.",
    "selection": "the Gemini article is the only one that includes the culturally relevant Huang and consensual non consent references that are \u201chot topics\u201d today, and although the riskiest, is also closest to what I want to say",
    "redline": "can I see a redlined version with the 5 short priced (from the other models) folded in? So I can see how they land? The other issues should probably be rolled into the audit imo.",
    "approval": "Yes",
}

AUTHOR_LABEL = "Synthia Cipher · author"
GROK = "Grok Bot · editor"


def _quote_ok() -> None:
    record = read_src("development/DECISION-RECORD.md")
    for key, quote in DECISION_QUOTES.items():
        if quote not in record:
            raise SystemExit(f"{key} quote is not verbatim in DECISION-RECORD.md")
    machine_verbatim = read_src("development/machine-question-VERBATIM.md")
    machine_prompt = read_src("development/machine-question.md")
    for q in QUESTIONS:
        if q not in machine_verbatim or q not in machine_prompt:
            raise SystemExit("machine question not verbatim in machine-question files")


def _esc_quote(text: str) -> str:
    return "<p>" + html.escape(text, quote=False) + "</p>"


def _artifact(summary: str, body: str, anchor: str | None = None, is_open: bool = False) -> str:
    aid = f' id="{anchor}"' if anchor else ""
    op = " open" if is_open else ""
    return f'<details class="artifact"{aid}{op}><summary>{summary}</summary><div class="artifact-body">{body}</div></details>'


def _human(when: str, body: str, described: bool = False, anchor: str | None = None) -> str:
    cls = "turn human described" if described else "turn human"
    aid = f' id="{anchor}"' if anchor else ""
    label = f"{AUTHOR_LABEL} · {when}"
    return f'<div class="{cls}"{aid} role="group" aria-label="{html.escape(label, quote=True)}"><div class="who">{html.escape(label)}</div><div class="bubble-text">{body}</div></div>'


def _ai(who: str, body: str, anchor: str | None = None) -> str:
    aid = f' id="{anchor}"' if anchor else ""
    return f'<div class="turn ai"{aid} role="group" aria-label="{html.escape(who, quote=True)}"><div class="who">{html.escape(who)}</div><div class="bubble-text">{body}</div></div>'


def _step(body: str, block: bool = False, anchor: str | None = None) -> str:
    aid = f' id="{anchor}"' if anchor else ""
    cls = "step block" if block else "step"
    return f'<div class="{cls}"{aid} role="note"><span class="visually-hidden">Process step: </span>{body}</div>'


def conversation_thread(page: str) -> str:
    _quote_ok()
    P = lambda rel: prose_html(rel, page)  # noqa: E731
    src = lambda rel: html.escape(public_href(rel, page), quote=True)  # noqa: E731
    parts: list[str] = []
    parts.append('<div class="day">Saturday, November 21, 2026 · times PST</div>')
    parts.append(_human(
        "issue request · about 4:24 PM",
        "<p class=\"ctx\">One message, shown here in parts. Verbatim excerpt of the author&rsquo;s note on the source:</p>"
        + "<blockquote>" + _esc_quote(DECISION_QUOTES["request"]) + "</blockquote>"
        + "<p class=\"ctx\">The same message carried the brain dump, the editorial prompt and the machine question:</p>"
        + _artifact("Source material: the author&rsquo;s brain dump, all written without AI (private link removed)",
                    "<div id=\"source-material\"></div>" + source_material_html())
        + _artifact("Editorial prompt (verbatim)", P("development/editorial-prompt.md"), "editorial-prompt")
        + _artifact("Machine-only question (verbatim)", P("development/machine-question-VERBATIM.md")),
        anchor="request",
    ))
    parts.append(_step(
        "Grok Bot preserved the source byte for byte and read the two X posts for the audit. "
        f'Four isolated single-turn requests, identical <a href="{src("development/submitted-prompt.md")}">submitted prompt</a> '
        "(editorial prompt + brain dump), no tools, no retries. max_tokens 48,000 for Claude Fable 5.2 (its Issue 37 machine run ran out at 32,000) and 32,000 for the others. "
        "The public copies of the prompt and request records carry the same two link changes as the source page.",
        block=True, anchor="submitted-prompt"))
    drafts = [
        ("author-fable", "Claude Fable 5.2 · reasoning max", "“Smart Enough to Fool Yourself” · 1,005 words · $1.169816", "development/author-alternatives/01-claude-fable-5.2.md"),
        ("author-astra", "GPT-6.2 Astra · reasoning max", "“You Can Be Right and Still Be the Wrong Person to Decide” · 840 words · $0.990544", "development/author-alternatives/02-gpt-6.2-astra.md"),
        ("author-neon", "Gemini 4 Neon · reasoning xhigh", "“The Smartest People in the Room Are the Easiest to Fool” · 1,015 words · $0.191217", "development/author-alternatives/03-gemini-4-neon.md"),
        ("author-muse", "Muse Wonder · reasoning max", "“Smart Enough to Fool Yourself” · 925 words · $0.128936", "development/author-alternatives/04-muse-wonder.md"),
    ]
    for anchor, who, meta, rel in drafts:
        parts.append(_ai(who + " · author-assist draft",
                         f'<p class="meta-line">{html.escape(meta)}</p>'
                         + _artifact("Full output: thesis, pressure-test, outline, draft", P(rel), anchor)))
    parts.append(_ai(GROK + " · comparison",
                     "<p>Side-by-side comparison of the four drafts, with factual-risk flags on the Huang and &ldquo;consensual non-consent&rdquo; claims.</p>"
                     + _artifact("Author comparison (as written, before selection)", P("development/author-comparison.md"), "author-comparison")))
    parts.append(_step(
        "Machine prompt = the author&rsquo;s question verbatim + the Issue 37 format paragraph without its ranking sentence (900–1,300 words, title and dek, no headers or lists). "
        f'One message, no system prompt, no tools, no brain dump, no links, no drafts (<a href="{src("metadata/isolation.json")}">isolation record</a>).'
        + _artifact("Full machine prompt as sent", P("development/machine-question.md"), "machine-question"),
        block=True, anchor="alternatives"))
    machine = [
        ("machine-fable", "Claude Fable 5.2 · reasoning max", "“What Intelligence Can’t Tell You About Your Own Life” · 1,209 words · $1.656800 · selected unchanged; same bytes as the freeze", "development/machine-alternatives/01-claude-fable-5.2.md"),
        ("machine-astra", "GPT-6.2 Astra · reasoning max", "“After the Congratulations” · 1,017 words · $0.553296", "development/machine-alternatives/02-gpt-6.2-astra.md"),
        ("machine-neon", "Gemini 4 Neon · reasoning xhigh", "“The Art of Not Outsmarting Yourself” · 1,155 words · $0.192954", "development/machine-alternatives/03-gemini-4-neon.md"),
        ("machine-muse", "Muse Wonder · reasoning max", "“The Amplifier Without a Compass” · 1,216 words · $0.143924", "development/machine-alternatives/04-muse-wonder.md"),
    ]
    for anchor, who, meta, rel in machine:
        parts.append(_ai(who + " · machine-only essay",
                         f'<p class="meta-line">{html.escape(meta)}</p>' + _artifact("Full essay as returned", P(rel), anchor)))
    parts.append(_ai(GROK + " · machine recommendation",
                     "<p>Recommended Claude Fable 5.2, unchanged and not combined. Muse Wonder was a close second.</p>"
                     + _artifact("Recommendation note", P("development/machine-comparison.md"), "machine-comparison")))
    parts.append(_human("selection · about 8:28 PM", "<p class=\"ctx\">Verbatim excerpt:</p><blockquote>" + _esc_quote(DECISION_QUOTES["selection"]) + "</blockquote>"
                        "<p class=\"ctx\">The author chose Gemini 4 Neon&rsquo;s draft and asked whether anything from the other drafts should be folded in.</p>", anchor="selection"))
    parts.append(_ai(GROK + " · integration memo",
                     "<p>Ranked short passages from Fable, Muse and Astra that could patch Neon&rsquo;s weak spots, and listed factual corrections.</p>"
                     + _artifact("Integration recommendations", P("development/revision-history/integration-recommendations.md"), "revisions")))
    parts.append(_human("redline request · about 8:36 PM", _esc_quote(DECISION_QUOTES["redline"]), anchor="redline-request"))
    parts.append(_ai(GROK + " · redline v1",
                     f'<p>Neon with five short passages folded in, each tagged by source. <a href="{src("development/revision-history/redline-v1-five-additions.pdf")}">Redline v1 (PDF)</a>.</p>'))
    parts.append(_human("redline review · about 8:54 PM",
                        "<p>Keep only the two Muse additions, exactly where they sit: the Chesterton&rsquo;s fence passage, and &ldquo;An ordinary person produces an excuse. A gifted person produces a philosophy.&rdquo; Revert everything else to Neon&rsquo;s text.</p>",
                        described=True))
    parts.append(_ai(GROK + " · redline v2",
                     f'<p>Only the two Muse insertions; a diff against Neon&rsquo;s draft confirms nothing else changed. <a href="{src("development/revision-history/redline-v2-two-muse-additions.pdf")}">Redline v2 (PDF)</a>.</p>'
                     + _artifact("Neon&rsquo;s draft as returned", P("development/revision-history/neon-draft-as-returned.md"), "rev-neon")
                     + _artifact("Clean v2 (two Muse insertions)", P("development/revision-history/neon-clean-v2.md"), "rev-v2")))
    parts.append(_human("approval · about 8:57 PM", _esc_quote(DECISION_QUOTES["approval"]) + "<p class=\"ctx\">Approval to freeze clean v2 as the author essay and Fable 5.2 as the machine essay, and to run the audit.</p>", anchor="approval"))
    parts.append(_step(
        f"<b>Author essay frozen (v1)</b> about 8:58 PM, 1,064 words of body, sha256 <code>{AUTHOR_V1_HASH}</code>. "
        f"<b>Machine essay frozen</b>, byte-identical to the model output, sha256 <code>{MACHINE_HASH}</code>."))
    parts.append(_step(f"Stage C critique: four calls, each critic shown one freeze (author v1); ${AUDIT_COST}, no retries. Findings stay in the audit, not the essays."))
    critics = [
        ("Kimi K3 · reasoning high · critic of the author essay", "audit/stage-c/humanai-leg-a-kimi-k3.md"),
        ("Claude Opus 4.1 · critic of the author essay", "audit/stage-c/humanai-leg-b-claude-opus-4.1.md"),
        ("Kimi K3 · reasoning high · critic of the machine essay", "audit/stage-c/machine-leg-a-kimi-k3.md"),
        ("Claude Opus 4.1 · critic of the machine essay", "audit/stage-c/machine-leg-b-claude-opus-4.1.md"),
    ]
    for who, rel in critics:
        parts.append(_ai(who, _artifact("Objections as returned", P(rel))))
    parts.append(_step("Grok Bot prepared the audit and the source page. Two HIGH findings needed a ruling: A1 (the company named in the &ldquo;consensual non-consent&rdquo; reporting) and A2 (the Post attribution)."))
    parts.append(_human("rulings · about 9:10 PM",
                        "<p>Change &ldquo;staffers at OpenAI&rdquo; to &ldquo;top AI lab staffers&rdquo; and nothing else. A2 and A3&ndash;A8 stay unmodified in the essay, with the corrections in the audit. On the source page, remove only the private link and strip tracking parameters from the X links.</p>",
                        described=True, anchor="rulings-message"))
    parts.append(_step(f"<b>Author essay refrozen (v2)</b> about 9:11 PM, sha256 <code>{AUTHOR_V2_HASH}</code>. "
                       f'<a href="{src("development/revision-history/freeze-v1-to-v2.diff")}">One-line diff</a>.'))
    parts.append(_human("follow-up approval · about 9:13 PM",
                        "<p>Approved: change &ldquo;top AI lab staffers&rdquo; to &ldquo;staffers at top AI labs&rdquo;, nothing else, which fixes the grammar seam. Then prepare the pull requests, without merging.</p>",
                        described=True))
    parts.append(_step(
        f"<b>Author essay refrozen (v3)</b> about 9:14 PM, 1,066 words of body, sha256 <code>{AUTHOR_HASH}</code>. "
        f'<a href="{src("development/revision-history/freeze-v2-to-v3.diff")}">One-line diff</a>. This is the current freeze.'
        + _artifact("Frozen author essay (v3)", P("essays/author-essay-FROZEN.md"), "freeze"),
        block=True))
    parts.append(_step("Grok Bot opened this audit record and the newsletter pages as pull requests, prepared and not merged. Publication waited for the author."))
    parts.append(_step("The author merged audit PR 54 at 9:33 PM and web PR 69 at 9:33 PM PST: Issue 38 is live. Post-publication status recorded with the audio links (audit PR 55)."))
    parts.append(_step("Grok Bot rendered both essays as local listening copies (xAI eve voice, 1.5&times;). The author listened, approved them, and published both on Spotify. Audio companions linked from both essays (audit PR 55 and web PR 70, about 10:25 PM)."))
    parts.append('<div class="day">Monday, November 23, 2026 · times PST</div>')
    parts.append(_step(
        "Video shorts published on X at @signalnoisepub. "
        f'Author short, about 4:40 PM: <a href="{AUTHOR_VIDEO}">{html.escape(AUTHOR_TITLE)}</a>, 41 seconds, made with Gemini 4 Neon at high, with an eve voiceover. '
        f'Machine short, about 4:42 PM: <a href="{MACHINE_VIDEO}">{html.escape(MACHINE_TITLE)}</a>, 42 seconds. '
        "It is Gemini 4 Neon&rsquo;s video interpretation of Claude Fable 5.2&rsquo;s essay, not Fable&rsquo;s own video. "
        "Both are linked between the essay and the audio companion."
    ))
    return '<div class="thread" aria-label="Conversation, start to finish">' + "\n".join(parts) + "</div>"


def development_page() -> str:
    page = "development"
    decision = prose_html("development/DECISION-RECORD.md", page)
    credits = prose_html("metadata/CREDITS.md", page)
    isolation = html.escape(read_src("metadata/isolation.json"))
    costs = html.escape(read_src("metadata/costs.json"))
    index = source_index(page)
    thread = conversation_thread(page)
    return f"""<!doctype html>
<html lang="en">
<head>
  <link rel="icon" href="../../../favicon.ico">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Extended Development Record - {html.escape(AUTHOR_TITLE)}</title>
<link rel="stylesheet" href="../conversation/conversation.css">
<link rel="stylesheet" href="../../edr-chat.css">
<script src="../../edr-chat.js" defer></script>
<style>body{{max-width:900px}}.frame{{border:1px solid var(--line);border-radius:10px;padding:.95rem 1.05rem;margin:1.2rem 0 1.6rem;background:#fcfcfc}}.frame p{{margin:.45rem 0}}.frame .frame-name{{display:block;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:.35rem}}.session{{border-top:1px solid var(--line);padding-top:1.15rem;margin-top:2.1rem;color:#333}}.cnav{{font-size:.84rem;color:var(--muted);margin:2.6rem 0 0;padding-top:1.1rem;border-top:1px solid var(--line)}}.cnav.top{{margin:1.4rem 0 1.6rem;padding:0 0 1rem;border-top:0;border-bottom:1px solid var(--line)}}.cnav dl{{display:grid;grid-template-columns:max-content 1fr;gap:.4rem 1rem;margin:0;align-items:baseline}}.cnav dt{{font-size:.68rem;letter-spacing:.075em;text-transform:uppercase;font-weight:600;opacity:.85;white-space:nowrap}}.cnav dd{{margin:0}}.cnav .here{{font-weight:600;color:var(--ink)}}@media(max-width:640px){{.cnav dl{{grid-template-columns:1fr;gap:.1rem}}.cnav dt{{margin-top:.7rem}}.cnav dt:first-of-type{{margin-top:0}}}}.table-scroll{{overflow-x:auto}}table{{width:100%;border-collapse:collapse;font-size:.92rem;margin:1rem 0}}th,td{{text-align:left;padding:.4rem .5rem;border-bottom:1px solid var(--line);vertical-align:top}}hr{{border:0;border-top:1px solid var(--line);margin:1.4rem 0}}pre.seed{{white-space:pre-wrap;font-family:inherit;margin:.4rem 0}}.visually-hidden{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}@media(max-width:720px){{body{{padding-left:1rem;padding-right:1rem}}}}{SRC_CSS}</style>
</head>
<body>
<p class="kicker">The World Behind the Words &middot; Issue 38 &middot; Extended Development Record</p>
<h1>Extended Development Record — {html.escape(AUTHOR_TITLE)}</h1>
<p class="lede">Issue 38, November 21, 2026, by Synthia Cipher. The conversation behind both essays, start to finish: what the author said, what each model returned, and what the editor did. The essay companions are live. Video shorts and audio companions are linked above.</p>
{nav_top("development")}
<div class="frame"><span class="frame-name">Read first — what this record is</span>
<p>Issue 38 is two essays and a source page. The human/AI essay is Gemini 4 Neon&rsquo;s draft with two Muse Wonder insertions the author approved, plus one phrase the author changed after the audit. The machine essay is Claude Fable 5.2&rsquo;s answer to the author&rsquo;s question, unchanged; none of the machine runs saw the author&rsquo;s brain dump. The critics were Kimi K3 and Claude Opus 4.1, each shown one freeze.</p>
{PREP_NOTE}
{VIDEO_NOTE}
{AUDIO_NOTE}
<p>{html.escape(STATUS)}</p>
<p><strong>Coverage.</strong> The author&rsquo;s turns marked verbatim are quoted exactly (the issue-request and selection excerpts, the redline request, and the approval). Three author turns are marked &ldquo;described, not verbatim&rdquo; because they reached the editor as relayed instructions rather than verbatim text. Model turns are the full outputs as returned. Grok Bot&rsquo;s turns are its delivered artifacts and a one-line summary of each; its chat replies are not reproduced. Exact assistant timestamps are not available. This record shows process and constraint. It does not prove the essays.</p>
</div>
<div class="chat-legend" aria-label="Legend">
<span><i class="k-human" aria-hidden="true"></i> Right, blue: <b>Synthia Cipher (author)</b></span>
<span><i class="k-ai" aria-hidden="true"></i> Left, grey: <b>AI</b>, labeled by model (Fable, Astra, Gemini, Muse, Kimi, Opus) or Grok Bot</span>
<span><i class="k-note" aria-hidden="true"></i> Centre: process steps (runs, freezes, hashes, audits)</span>
<span>The source material is all the author&rsquo;s own text</span>
</div>
<h2 class="session" id="conversation">The conversation, start to finish</h2>
<p class="meta">Long artifacts are collapsed; open any of them to read the full text. Printing expands them all.</p>
{thread}
<h2 class="session" id="decision-record">Reference</h2>
<div class="frame" id="decision"><span class="frame-name">Decision record: decisions, runs, revisions, costs</span>
{decision}
</div>
<div class="frame" id="credits"><span class="frame-name">Credits, cost, isolation</span>
<p>Actual API-reported total <strong>${COST_TOTAL}</strong>.</p>
{credits}
<h3>costs.json</h3>
<pre class="seed">{costs}</pre>
<h3>isolation.json</h3>
<pre class="seed">{isolation}</pre>
<p>The request and result files linked below are scrubbed. They keep message text, model output, and usage. They are not byte-original API envelopes. Hashes of these public files are not hashes of the private originals.</p>
</div>
<h2 class="session" id="files">Source files</h2>
<p class="meta">Every public file for Issue 38.</p>
{index}
{nav_bottom("development")}
</body>
</html>
"""


INDEX_ROW = """          <article class="issue-row" data-issue-row data-status="complete" data-search="38 issue 38 the smartest people in the room are the easiest to fool what intelligence can't tell you about your own life intelligence wisdom haidt chesterton jensen huang source material rulings confirmed companions live audio companion spotify video short x machine companion machine-version issue-038-source-material">
            <div class="issue-index">38</div>
            <div class="issue-copy"><a href="https://scipher888.github.io/signal-noise-audit-snapshot/issues/issue-038/">The Smartest People in the Room Are the Easiest to Fool</a></div>
          </article>
"""


def sync_issue_count(text: str) -> str:
    """Set the "N issues shown" line to the number of issue rows actually listed."""
    rows = text.count("data-issue-row")
    return re.sub(r">\d+ issues shown<", f">{rows} issues shown<", text)


def index_lists_issue(index: str, number: int) -> bool:
    """True when the index links this issue once and its count matches the rows (never fewer than this issue)."""
    shown = re.search(r">(\d+) issues shown<", index)
    rows = index.count("data-issue-row")
    return (
        index.count(f"issues/issue-{number:03d}/\"") == 1
        and shown is not None
        and int(shown.group(1)) == rows
        and rows >= number
    )


def patch_index() -> None:
    text = ISSUES_INDEX.read_text(encoding="utf-8")
    # issue count is derived from the rows below (sync_issue_count)
    if "issues/issue-038/" not in text:
        needle = '          <article class="issue-row" data-issue-row data-status="complete" data-search="37 issue 37'
        if needle not in text:
            raise SystemExit("issues index anchor for issue 37 not found")
        text = text.replace(needle, INDEX_ROW + needle, 1)
    else:
        text = re.sub(
            r'          <article class="issue-row" data-issue-row data-status="complete" data-search="38 issue 38.*?</article>\n',
            lambda _m: INDEX_ROW,
            text,
            count=1,
            flags=re.S,
        )
    ISSUES_INDEX.write_text(sync_issue_count(text), encoding="utf-8")


PAGES = ["index.html", "machine-version/index.html", "machine-version/audit/index.html", "development/index.html"]


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
    blobs = {p: (ROOT / p).read_text(encoding="utf-8") for p in PAGES}
    author, machine, maudit, dev = (blobs[p] for p in PAGES)
    index = ISSUES_INDEX.read_text(encoding="utf-8")
    for name, blob in blobs.items():
        if re.search(r"\bJoel\b|\bTess\b", blob):
            raise SystemExit(f"private name in {name}")
        if "sk-or-" in blob or "OPENROUTER_API" in blob or "/Users/" in blob or "/workspace/" in blob or "/home/box" in blob:
            raise SystemExit(f"secret-like or local path in {name}")
        if "dropbox.com" in blob or "rlkey=" in blob or "&amp;s=46" in blob or "?a=" in blob:
            raise SystemExit(f"private link or tracking parameter in {name}")
        if blob.count(f'href="{AUTHOR_AUDIO}"') < 2 or blob.count(f'href="{MACHINE_AUDIO}"') < 2:
            raise SystemExit(f"audio companion links missing in {name}")
        if blob.count(">Audio companion</a>") != 4:
            raise SystemExit(f"audio nav count drifted in {name}")
        if "open.spotify.com/embed" in blob or "spotify.com/episode/" in blob.replace(AUTHOR_AUDIO, "").replace(MACHINE_AUDIO, ""):
            raise SystemExit(f"unexpected Spotify URL in {name}")
        if blob.count(f'href="{AUTHOR_VIDEO}"') < 2 or blob.count(f'href="{MACHINE_VIDEO}"') < 2:
            raise SystemExit(f"video short links missing in {name}")
        if blob.count(">Video short</a>") != 4:
            raise SystemExit(f"video nav count drifted in {name}")
        if f'<a href="{AUTHOR_VIDEO}">Video short</a> &middot; <a href="{AUTHOR_AUDIO}">Audio companion</a>' not in blob:
            raise SystemExit(f"author video short is not between the essay and the audio companion in {name}")
        if f'<a href="{MACHINE_VIDEO}">Video short</a> &middot; <a href="{MACHINE_AUDIO}">Audio companion</a>' not in blob:
            raise SystemExit(f"machine video short is not between the essay and the audio companion in {name}")
        for stale_video in ("No video has been added", "No video exists", "no video short", "Issue 38 has no video"):
            if stale_video in blob:
                raise SystemExit(f"stale no-video status {stale_video!r} in {name}")
        for stale_audio in ("No audio has been added", "No audio exists", "No audio.", "no audio companion", "Issue 38 has no audio"):
            if stale_audio in blob:
                raise SystemExit(f"stale no-audio status {stale_audio!r} in {name}")
        for stale in ("Prepared, not published", "prepared for review", "Prepared for review", "do not resolve",
                      "unmerged Signal", "The newsletter page will be", "Publication waits for the author"):
            if stale in blob:
                raise SystemExit(f"stale status wording {stale!r} in {name}")
        if LIVE_MARK not in blob or WEB_MERGE not in blob or "Rulings confirmed November 21, 2026" not in blob:
            raise SystemExit(f"live-companion status missing in {name}")
    if "278105" not in author or "270007" not in author:
        raise SystemExit("audio verification note missing from the author audit")
    if "41280" not in author or "42304" not in author:
        raise SystemExit("video verification note missing from the author audit")
    for label, blob in (("author audit", author), ("machine audit", maudit), ("development", dev), ("machine essay", machine)):
        if "not Fable" not in blob:
            raise SystemExit(f"machine video attribution missing in {label}")
        if blob.count("The conversation behind this") < 2 or blob.count("Source material") < 2:
            raise SystemExit(f"nav incomplete in {label}")
        if "Written without AI</dt>" in blob:
            raise SystemExit(f"wrong companion label in {label}")
    # machine essay: the exact question, outside and before the unchanged prose
    for q in QUESTIONS:
        if f'<p class="provenance-question">{html.escape(q)}</p>' not in machine:
            raise SystemExit("machine question not verbatim on inspection page")
    if machine.index("</aside>") > machine.index("Intelligence, in the sense that IQ tests measure"):
        raise SystemExit("provenance aside must precede the essay")
    essay = read_src("essays/machine-essay-FROZEN-v1.0.md")
    for para in [p.strip() for p in essay.split("\n\n")]:
        if para.startswith("#") or para.startswith("*"):
            continue
        if html.escape(para, quote=False) not in machine and para not in machine:
            raise SystemExit("machine essay paragraph missing from inspection page")
    author_essay = read_src("essays/author-essay-FROZEN.md")
    dev_plain = html.unescape(re.sub(r"<[^>]+>", "", dev))
    for para in [p.strip() for p in author_essay.split("\n\n") if p.strip() and not p.startswith("#")]:
        plain = re.sub(r"\*([^*]+)\*", r"\1", para)
        if plain not in dev_plain:
            raise SystemExit("author freeze paragraph missing from development record")
    if "staffers at top AI labs" not in dev_plain or "staffers at top AI labs" not in html.unescape(author):
        raise SystemExit("current freeze wording missing")
    # source material: the rendered text equals the published file
    mix = re.search(r'<div class="src-mix">(.*?)</div>', dev, re.S).group(1)
    if html.unescape(re.sub(r"<[^>]+>", "", mix)) != read_src("essays/source-material-PUBLIC.md"):
        raise SystemExit("source material on development page is not verbatim")
    if "[private link removed]" not in mix:
        raise SystemExit("private-link removal note missing")
    for token in ["A1", "A2", "A8", "A10", "M1", "M5", "M9", "Anthropic", "Megaspeed", "Chesterton", "Terman", "Ruling A"]:
        if token not in author or token not in maudit:
            raise SystemExit(f"finding {token} missing from an audit page")
    if "floor pass" in author.lower() or "floor pass" in maudit.lower():
        raise SystemExit("floor pass language slipped in")
    if "Editor&rsquo;s note: Under this newsletter" in author or "ednote" in author:
        raise SystemExit("an above-essay corrective note slipped back into the audit page")
    for blob in blobs.values():
        if re.search(r"\bt3\d\d[us]\d*\b|gen-\d{6,}", blob):
            raise SystemExit("internal message or generation id in a page")
    for anchor in ["author-fable", "author-astra", "author-neon", "author-muse", "machine-fable", "machine-astra", "machine-neon", "machine-muse", "machine-question", "revisions", "source-material", "alternatives", "decision", "freeze"]:
        if f'id="{anchor}"' not in dev:
            raise SystemExit(f"missing development section {anchor}")
    if str(COST_TOTAL) not in author or str(COST_TOTAL) not in dev or AUDIT_COST not in author:
        raise SystemExit("cost missing")
    if not index_lists_issue(index, 38) or not index_lists_issue(index, 37):
        raise SystemExit("index not updated")
    missing = []
    page_paths = {(ROOT / p).resolve(): p for p in PAGES}
    for rel in PAGES:
        html_path = ROOT / rel
        for href in re.findall(r'(?:href|src)="([^"]+)"', blobs[rel]):
            href = html.unescape(href)
            if href.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            path_only, _, frag = href.partition("#")
            path_only = path_only.split("?", 1)[0]
            target = (html_path.parent / path_only).resolve() if path_only else html_path.resolve()
            # GitHub Pages serves no folder listings: a folder link needs an index.html.
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                missing.append(f"{rel} -> {href}")
                continue
            if frag and target in page_paths and f'id="{frag}"' not in blobs[page_paths[target]]:
                missing.append(f"{rel} -> {href} (no such anchor)")
    if missing:
        raise SystemExit("missing internal links:\n" + "\n".join(missing[:30]))
    print("issue 38 check ok")


def main() -> None:
    write_pages()
    if "--check" in sys.argv:
        before = {ROOT / p: (ROOT / p).read_bytes() for p in PAGES}
        before[ISSUES_INDEX] = ISSUES_INDEX.read_bytes()
        write_pages()
        for path, data in before.items():
            if path.read_bytes() != data:
                raise SystemExit(f"build is not idempotent: {path}")
    check_pages()


if __name__ == "__main__":
    main()
