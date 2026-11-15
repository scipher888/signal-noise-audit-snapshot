#!/usr/bin/env python3
"""Rebuild Issue 37 audit pages from issues/issue-037/source.

Adapted from issues/issue-036/build.py (same Markdown renderer and page
shells). Frozen Markdown hashes are checked and never rewritten. Issue 37 has
two Spotify audio companions. Its three newsletter companions are live (web PR 51), and Ruling A
is confirmed. The written-without-AI page is replaced by a source-material
page that marks the author's own words apart from Grok Heavy research.

    python3 issues/issue-037/build.py
    python3 issues/issue-037/build.py --check
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

AUTHOR_HASH = "dd517c993bd5058218c6ef1fb243df141b2d7a0853e12b89261bad59e762babd"
MACHINE_HASH = "f6544821668c6f85880a3bd9dde5659ed1a7450617158261addd166ad85f5a64"
SOURCE_MATERIAL_HASH = "7bc92f1e095b06ec03881eef0f3b09ef6dc69e02814cca3298afccff929243ba"
COST_TOTAL = Decimal("7.0226065")
AUDIT_COST = "0.365082"

AUTHOR_WEB = "https://www.signalandnoise.email/p/what-spacex-caught-in-those-mechanical-arms-is-bigger-than-a-rocket/"
MACHINE_WEB = "https://www.signalandnoise.email/p/where-the-starship-catch-ranks-and-what-it-could-change/"
SOURCE_WEB = "https://www.signalandnoise.email/p/issue-037-source-material/"
AUTHOR_AUDIO = "https://open.spotify.com/episode/678mAUkmd2Z3YoZOYcJuNh"
MACHINE_AUDIO = "https://open.spotify.com/episode/2zg6tctAs33svf2M8ktwmO"
FLIGHT_SOURCE = "https://www.space.com/space-exploration/launches-spacecraft/spacex-chopsticks-catch-starship-upper-stage-flight-14"
CSS_V = "de2cc137"
JS_V = "0c872f22"

AUTHOR_TITLE = "What SpaceX Caught in Those Mechanical Arms Is Bigger Than a Rocket"
MACHINE_TITLE = "Where the Starship Catch Ranks, and What It Could Change"
MACHINE_DEK = (
    "Flight 15 comes sixth among history's hardest engineering feats, "
    "and its effects could reach people who never leave the ground."
)
QUESTIONS = (
    "1. Please rank in order the greatest engineering achievements of all time based solely on the magnitude of the engineering/technological challenge and assuming modern (2026-era) technology, materials, computing, simulation, and manufacturing could be applied to al of them - and keep ranking them until you can place the successful capture of Starship Fight 15 (happened today - on 11/14/2026) somewhere in this list.",
    "2. Taking on optimistic but realistic/possible view, what does this proof of concept of fully reusable large payload spaceships imply about the future for ordinary people over the next 10, 25, 50, and 100 years?",
)

RULING = (
    "Ruling A for both essays, confirmed November 14, 2026: keep both freezes unchanged and record the "
    "findings on the audit pages. The author asked to keep the fact checks in the audit, then merged the "
    "Issue 37 pull requests (this record, PR 49, at 10:39:47 PM PST; the newsletter pages, PR 51, at 10:40:15 PM PST)."
)
STATUS = RULING
WEB_MERGE = "d040e51ec8255b3ccf9f8f32c1759a81e528eb40"


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
        "essays/machine-essay-FROZEN-v1.0.md": MACHINE_HASH,
        "development/machine-alternatives/01-claude-fable-5.2.md": MACHINE_HASH,
        "essays/source-material-VERBATIM.md": SOURCE_MATERIAL_HASH,
    }
    for rel, expect in checks.items():
        got = sha256(SOURCE / rel)
        if got != expect:
            raise SystemExit(f"frozen hash changed for {rel}: {got}")
    costs = json.loads(read_src("metadata/costs.json"))
    total = sum(Decimal(run["actual_api_reported_usd"]) for run in costs["runs"])
    if total != COST_TOTAL or Decimal(costs["actual_api_reported_total"]) != COST_TOTAL:
        raise SystemExit(f"cost ledger {total} != {COST_TOTAL}")
    attribution = json.loads(read_src("essays/source-attribution.json"))
    if "".join(s["text"] for s in attribution["segments"]) != read_src("essays/source-material-VERBATIM.md"):
        raise SystemExit("source attribution segments do not reproduce the verbatim source")


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
    """Companion nav. Same labels on every Issue 37 surface."""

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
    author = sep.join([item("essay", AUTHOR_WEB, "The essay"), f'<a href="{AUTHOR_AUDIO}">Audio companion</a>', item("author-audit", rel["author-audit"], "The audit")])
    machine = sep.join([item("machine-essay", rel["machine-essay"], "The essay"), f'<a href="{MACHINE_AUDIO}">Audio companion</a>', item("machine-audit", rel["machine-audit"], "The audit")])
    source = item("source", SOURCE_WEB, "The piece")
    convo = item("development", rel["development"], "The conversation behind this")
    return (
        f'<nav class="cnav {{klass}}" aria-label="Issue 37 companions"><dl>'
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
    "Signal &amp; Noise web pull request 51 was merged November 14, 2026, 10:40:15 PM PST, "
    f"commit <code>{WEB_MERGE}</code>. "
    "Rechecked for this record at 10:41 PM PST: each of the three pages returned HTTP 200, and the essay text on each live page "
    "rebuilds to its freeze hash. The source page reproduces the verbatim source. "
    "This audit record is the inspection surface for those live pages.</p>"
)

AUDIO_NOTE = (
    "<p><strong>Audio companions are published Spotify episodes.</strong> "
    "These are plain canonical links. This record does not embed a player and does not store audio files. "
    f'Author: <a href="{AUTHOR_AUDIO}">{html.escape(AUTHOR_TITLE)}</a>. '
    "oEmbed, the canonical page, the embed, and a headless browser load each returned that title on November 15, 2026, about 7:00 AM PST. "
    "The embed duration field is 225625 ms, which rounds to 3:46. "
    f'Machine: <a href="{MACHINE_AUDIO}">{html.escape(MACHINE_TITLE)}</a>. '
    "oEmbed, the canonical page, the embed, and a headless browser load each returned that title at the same time. "
    "The embed duration field is 275127 ms, which rounds to 4:35. "
    "Both narrations are xAI eve voice at 1.5&times;: title, the machine essay&rsquo;s dek, and the full frozen text, with no added intro or outro. "
    "As in Issue 36, the machine essay&rsquo;s question note and editor&rsquo;s note are not spoken; the editor&rsquo;s note confirming the flight is on the page. "
    "The reported API total does not include text-to-speech charges, which the service did not report, and none are added here.</p>"
)
LIVE_MARK = "The essay companions are live."

FLIGHT_NOTE = (
    "<p><strong>The event both essays rest on happened.</strong> On November 14, 2026, at about 1:20 PM PST, "
    "SpaceX caught Ship 42, Starship&rsquo;s upper stage, in the Starbase tower&rsquo;s arms after it returned from orbit. "
    "The booster catch on the same flight was aborted after a low-fuel alarm, and the booster was destroyed over the Gulf of Mexico. "
    f'Sources: <a href="{FLIGHT_SOURCE}">Space.com</a>, NPR, CNBC, The Verge and SpaceX (see the source log). '
    "Two critics tagged the event FLOOR because they did not know about it. Those tags are resolved, not ignored.</p>"
)

RULING_BLOCK = f"""<div class="callout coral" id="ruling"><p>{html.escape(STATUS)}</p>
<ul>
<li>Both freezes are byte-for-byte unchanged.</li>
<li>Author freeze <code>author-essay-FROZEN.md</code>, sha256 <code>{AUTHOR_HASH}</code>. It is Claude Fable 5.2's draft, with Gemini 4 Carbon's title and three edits the author approved. The development record lists every difference.</li>
<li>Machine freeze <code>machine-essay-FROZEN-v1.0</code>, sha256 <code>{MACHINE_HASH}</code>. It is Claude Fable 5.2's essay, selected unchanged by Grok Bot. Its bytes match machine alternative 01.</li>
<li>The fact checks the author asked to keep out of the essay are findings A1–A18 and M1–M11 below. None is blocking, and none is described as a pass.</li>
<li>Audio companions are the two published Spotify episode links in the navigation. This repository does not store an audio file.</li>
<li>The dual audit, Stage C synthesis and execution method were written before publication. Their pre-publication status sentences (review draft, pending ruling, unmerged branches) are historical. The ruling closed that choice; it did not withdraw any finding.</li>
</ul>
<p>This is an editorial disposition. It does not certify that the essays are true or that their forecasts will happen.</p></div>"""


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
          <h3>Issue 37</h3>
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
    ".src-key-h{background:#fbe9d0;color:#7a1f1f;border-left:3px solid #7a1f1f}.src-key-g{background:#e6ecf3;color:#3d4a5c}"
    ".src-mix{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.65}"
    ".src-h{background:#fbe9d0;color:#7a1f1f;font-weight:600;border-left:3px solid #7a1f1f;padding:.05rem .25rem;-webkit-box-decoration-break:clone;box-decoration-break:clone}"
    ".src-h::before{content:'Synthia';font:700 .6rem/1 system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#fff;background:#7a1f1f;padding:.12rem .3rem;border-radius:2px;margin-right:.3rem;vertical-align:.15em}"
    ".src-g{background:#e6ecf3;color:#3d4a5c;font-family:system-ui,sans-serif;font-size:.93rem;-webkit-box-decoration-break:clone;box-decoration-break:clone}"
)


def source_material_html() -> str:
    data = json.loads(read_src("essays/source-attribution.json"))
    out = []
    for seg in data["segments"]:
        text = html.escape(seg["text"], quote=False)
        if seg["author"] == "HUMAN":
            out.append(f'<span class="src-h">{text}</span>')
        elif seg["author"] == "GROK HEAVY":
            out.append(f'<span class="src-g">{text}</span>')
        else:
            out.append(text)
    wc = data["word_counts"]
    legend = (
        '<div class="src-legend" role="note" aria-label="Legend">'
        '<p><span class="src-key src-key-h">Synthia</span> Written by Synthia Cipher, without AI.</p>'
        '<p><span class="src-key src-key-g">Grok Heavy</span> Research text generated with Grok Heavy and included by the author.</p></div>'
    )
    return legend + f'<div class="src-mix">{"".join(out)}</div>' + (
        f'<p class="meta">Author&rsquo;s words: {wc["HUMAN"]}. Grok Heavy: {wc["GROK HEAVY"]}. '
        f'The split follows the author&rsquo;s own designation. sha256 of the verbatim source <code>{SOURCE_MATERIAL_HASH}</code>.</p>'
    )


def provenance_aside(prefix: str) -> str:
    qs = "".join(f'<p class="provenance-question">{html.escape(q)}</p>' for q in QUESTIONS)
    return (
        '<aside class="provenance" aria-label="Origin of this machine essay">'
        '<p class="provenance-label">The questions given to the AI:</p>'
        f"{qs}"
        "<p>These two questions, in the author&rsquo;s own words with typos kept, are the substantive prompt. "
        "The same message also asked for an essay of roughly 900 to 1,300 words with a title and a one-line dek, "
        "no section headers or bullet lists, and only the top five achievements, with Flight 15&rsquo;s place stated if it fell outside them. "
        f'<a href="{prefix}development/#machine-question">Full prompt</a>. '
        "Four identical requests contained none of the author&rsquo;s source or drafts "
        f'(<a href="{prefix}source/metadata/isolation.json">isolation record</a>). '
        "Grok Bot selected this essay unchanged.</p>"
        "<p><strong>Editor&rsquo;s note.</strong> The essay says it cannot independently confirm the flight. It happened. "
        "On November 14, 2026, SpaceX caught Ship 42, Starship&rsquo;s upper stage, in the Starbase tower&rsquo;s arms "
        "after it returned from orbit; the booster&rsquo;s catch on the same flight was aborted. "
        f'<a href="{FLIGHT_SOURCE}">Space.com report</a>.</p>'
        "</aside>"
    )


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
    author_words = words(read_src("essays/author-essay-FROZEN.md"))
    machine_words = words(read_src("essays/machine-essay-FROZEN-v1.0.md"))
    return f"""<!doctype html>
<html lang="en">
<head>
  <link rel="icon" href="../../favicon.ico">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Audit for Signal &amp; Noise Issue 37, {html.escape(AUTHOR_TITLE)}: source checks, Stage C objections, and the Flight 15 confirmation. Ruling A. Essay companions are live.">
  <title>Issue 37 Published Audit - {html.escape(AUTHOR_TITLE)}</title>
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
          <div class="issue-eyebrow"><p class="eyebrow">Issue 37 &middot; November 14, 2026 &middot; Synthia Cipher</p></div>
          <h1 class="page-title">{html.escape(AUTHOR_TITLE)}</h1>
          <p class="lede">Audit for Issue 37. Intended issue date: November 14, 2026. Byline: Synthia Cipher. Live companions: the <a href="{AUTHOR_WEB}">human/AI essay</a>, the <a href="{MACHINE_WEB}">machine essay</a>, and the <a href="{SOURCE_WEB}">source material</a>, which this issue publishes instead of a written-without-AI page. No dek on the author essay. Audio companions are linked above.</p>
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
            {AUDIO_NOTE}
            <div class="callout mint"><p><strong>Canonicality.</strong> The essay Signal &amp; Noise stands behind is Issue 37, <em>{html.escape(AUTHOR_TITLE)}</em>, by Synthia Cipher. This page is its audit, not a second edition and not a corrected essay. The fact checks live here, at the author&rsquo;s request, so the essay reads cleanly. The machine essay, <a href="{MACHINE_WEB}">{html.escape(MACHINE_TITLE)}</a>, is a companion; its inspection copy is <a href="machine-version/">on this record</a>. Author freeze sha256 <code>{AUTHOR_HASH}</code> ({author_words} whitespace-delimited words in the Markdown file, title included, no dek). Machine freeze sha256 <code>{MACHINE_HASH}</code> ({machine_words} whitespace-delimited words, title and dek included).</p></div>
            <div class="callout">{FLIGHT_NOTE}</div>
            {RULING_BLOCK}
            <div class="callout" id="attestations"><h2>Factual attestations</h2>
            {attest}
            </div>
          </section>
          <section class="content-section" id="assembly">
            <h2>How the author essay was assembled</h2>
            <p>Four models received the author&rsquo;s editorial prompt with the mixed source. The author chose Claude Fable 5.2&rsquo;s draft for how it uses the Culture novels, and Gemini 4 Carbon&rsquo;s title. The author then asked for the billionaire passage to be reconsidered. Two options were offered: A rewrote the Banks sentence, and B replaced the passage with &ldquo;to be sure&rdquo; material from other drafts. The author kept Fable&rsquo;s own sentences, with &ldquo;To some, there is&rdquo; in place of &ldquo;And there is.&rdquo; The Musk prediction became a new paragraph, and the next sentence became &ldquo;And the remaining objections strengthen the case.&rdquo; Everything else is Fable verbatim. See <a href="development/#decision">the development record</a>.</p>
            <p>The machine essay was not assembled. Four models received the same two questions and the same format instructions, with no source and no author essay. Claude Fable 5.2&rsquo;s first attempt spent its whole token budget on reasoning and returned nothing. Its second attempt is the essay, unchanged. Gemini 4 Carbon, GPT-6 Astra, and Muse Wonder are the alternatives.</p>
          </section>
          <section class="content-section" id="audit">
            <h2>Dual audit</h2>
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
            <p>Actual API-reported total <strong>${COST_TOTAL}</strong> across seventeen paid calls, including one failed machine attempt. The audit itself cost ${AUDIT_COST}. Figures are API usage reports, not a reconciled card statement.</p>
            {credits}
            <p>Per-run ledger: <a href="source/metadata/costs.json">costs.json</a>. Isolation check: <a href="source/metadata/isolation.json">isolation.json</a>.</p>
          </section>
          <section class="content-section" id="source-material">
            <h2>Source material</h2>
            <p>This issue&rsquo;s source mixes the author&rsquo;s raw brain dump with research text generated with Grok Heavy. The author asked for it to be published where the written-without-AI page usually goes, with the author&rsquo;s own words visibly marked. The newsletter page is <a href="{SOURCE_WEB}">Source material — Issue 37</a>. The verbatim file is <a href="source/essays/source-material-VERBATIM.md">source-material-VERBATIM.md</a>, and the segment map is <a href="source/essays/source-attribution.json">source-attribution.json</a>. The development record renders it with the same highlighting.</p>
          </section>
          <section class="content-section" id="closing">
            <div class="callout mint"><p>What this audit did: it kept both freezes unchanged and logged every author finding (A1–A18) and machine finding (M1–M11). It published the Stage C returns and their dispositions, including objections that land and objections that do not, along with the source log and the ${COST_TOTAL} cost. It did not certify the essays or their forecasts.</p></div>
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
<meta name="description" content="{html.escape(MACHINE_TITLE)}: the machine essay for Signal &amp; Noise Issue 37, inspection copy of freeze machine-essay-FROZEN-v1.0.">
<title>The Machine's Version - {html.escape(MACHINE_TITLE)}</title>
<meta property="og:site_name" content="Signal &amp; Noise">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(MACHINE_TITLE, quote=True)}">
<meta property="og:description" content="{dek_attr}">
<meta property="og:url" content="https://scipher888.github.io/signal-noise-audit-snapshot/issues/issue-037/machine-version/">
<meta property="og:image" content="https://www.signalandnoise.email/assets/preview.png?v=09b48f76">
<meta name="twitter:card" content="summary_large_image">
<style>{MACHINE_CSS}{PROVENANCE_CSS}</style></head><body><div class="wrap">
<p class="kicker">The World Behind the Words &middot; Issue 37 &middot; The machine&rsquo;s version &middot; a machine essay</p>
<h1>{html.escape(MACHINE_TITLE)}</h1>
<p class="dek"><em>{html.escape(MACHINE_DEK)}</em></p>
{provenance_aside("../")}
{nav_top("machine-essay")}
<div class="note"><p><strong>About this piece.</strong> This is a machine essay. It is not a second front door, and it is not a correction of the author&rsquo;s essay. Signal &amp; Noise stands behind the human/AI essay <a href="{AUTHOR_WEB}"><em>{html.escape(AUTHOR_TITLE)}</em></a>. This page is the inspection copy of freeze <code>machine-essay-FROZEN-v1.0</code>. Findings live on <a href="audit/">its audit</a>. The development record is <a href="../development/">the conversation behind this</a>. The live public page is <a href="{MACHINE_WEB}">{html.escape(MACHINE_TITLE)}</a>. The audio companion is linked above.</p></div>
<div class="note"><p>{html.escape(RULING)} The newsletter page is live and matches this freeze. The text below is the freeze, with the Markdown heading and dek markers removed and no other wording change.</p></div>
{body}
<div class="note"><p><strong>Attribution.</strong> Machine essay. Written by Claude Fable 5.2 (<code>anthropic/claude-fable-5.2</code> via OpenRouter, reasoning effort max) from the questions and format instructions alone, in one single-turn run. This was the second attempt; the first returned no essay. Grok Bot selected this essay unchanged from four isolated generations and did not edit it. Run cost $1.879704, plus $1.282784 for the failed first attempt. Freeze sha256 <code>{MACHINE_HASH}</code>. Gemini 4 Carbon, GPT-6 Astra, and Muse Wonder each wrote a separate answer; those are in <a href="../development/#alternatives">the development record</a>.</p></div>
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
<meta name="description" content="Machine audit for Signal &amp; Noise Issue 37, {html.escape(MACHINE_TITLE)}. Findings kept, including the disclosed confirmation caveat and the EUV figure.">
<title>Audit of the Machine's Version - {html.escape(MACHINE_TITLE)}</title>
<style>{AUDIT_CSS}</style></head><body><div class="wrap">
{nav_top("machine-audit")}
<div class="note mint"><p><strong>Canonicality.</strong> This page audits the machine essay. The essay Signal &amp; Noise stands behind is the human/AI Issue 37, <a href="{AUTHOR_WEB}"><em>{html.escape(AUTHOR_TITLE)}</em></a>, by Synthia Cipher. The machine landing is freeze <code>machine-essay-FROZEN-v1.0</code> (sha256 <code>{MACHINE_HASH}</code>). The inspection copy is <a href="../">on this record</a>. The author audit is <a href="../../">here</a>. The development record is <a href="../../development/">the conversation behind this</a>. The audio companion is linked above.</p></div>
<div class="note">{PREP_NOTE}</div>
<div class="note">{AUDIO_NOTE}</div>
<div class="note">{FLIGHT_NOTE}</div>
{ruling}
<h2 id="audit">Dual audit</h2>
<p>Machine findings are M1–M11. Author findings A1–A18 are in the same document, so neither set is filed only on the other page.</p>
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
<p>Actual API-reported total <strong>${COST_TOTAL}</strong>. The selected machine run cost $1.879704, and the failed first attempt cost $1.282784. The critics of this freeze cost $0.064116 (Kimi K3) and $0.097035 (Claude Opus 4.1).</p>
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
    "t292u": "only these parts \"The successful capture of Starship Fight 15 is the #1 greatest engineering achievement of all time\" and \"For context, I would rank the following to round out the top 5 achievements:\" and \"But who cares? What does proof of concept of fully reusable large payload spaceships of imply about your future? I'm so glad you asked.\" and \"In short, Elon Musk has repeatedly told audiences to read Ian Banks culture series. …\" are from my raw brain dump. Everything else is from my research with Grok Heavy",
    "t295u": "The fact checks are great, but let's keep the fact checks in the audit (for readability sake). So let's keep this: \"To some, there is an awkward fact at the center of his enthusiasm. The Culture has no billionaires. Banks himself wondered aloud how his libertarian admirers had managed to miss that his paradise abolished private property.\"  And perhaps this \"Musk, though, has not missed it. He predicts that, with enough AI and robotics, money \"will stop being relevant.\" In a civilization so rich that money has withered away, nobody is a billionaire, and nobody needs to be.\" needs to go in the following (new?) paragraph since I don't think is fits cleanly in the \"To be sure\" paragraph.",
    "t296u": "Yeah, I noticed that one small thing too. Could we say \"And the remaining objections strengthen the case\"",
    "t297u": "Excellent. Please proceed.",
    "t298u": "Merged, and Confirming you’ve marked the correct passages as mine in the source page preview.",
}

AUTHOR_LABEL = "Synthia Cipher · author"
GROK = "Grok Bot · editor"


def _quote_ok() -> None:
    record = read_src("development/DECISION-RECORD.md")
    for key, quote in DECISION_QUOTES.items():
        if quote not in record:
            raise SystemExit(f"{key} quote is not verbatim in DECISION-RECORD.md")
    machine_verbatim = read_src("development/machine-questions-VERBATIM.md")
    for q in QUESTIONS:
        if q not in machine_verbatim:
            raise SystemExit("machine question not verbatim in machine-questions-VERBATIM.md")


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
    parts.append('<div class="day">Saturday, November 14, 2026 · times PST</div>')
    # 1. the author's source message (t292u)
    parts.append(_human(
        "t292u · about 8:20 PM",
        "<p class=\"ctx\">One message, shown here in parts. Verbatim excerpt of the author&rsquo;s attribution note:</p>"
        + "<blockquote>" + _esc_quote(DECISION_QUOTES["t292u"]) + "</blockquote>"
        + "<p class=\"ctx\">The same message carried the source material, the editorial prompt and the two machine questions:</p>"
        + _artifact("Source material, verbatim (author&rsquo;s passages marked; the rest is Grok Heavy research the author pasted)",
                    "<div id=\"source-material\"></div>" + source_material_html())
        + _artifact("Editorial prompt (verbatim)", P("development/editorial-prompt.md"), "editorial-prompt")
        + _artifact("Machine-only questions (verbatim, typos kept)", P("development/machine-questions-VERBATIM.md")),
        anchor="t292u",
    ))
    parts.append(_step(
        "Grok Bot filed this as <b>Issue 37</b> (the message said &ldquo;Issue 36&rdquo;, which was already published) and preserved the source byte for byte. "
        f'Four isolated single-turn requests, identical <a href="{src("development/submitted-prompt.md")}">submitted prompt</a> '
        "(editorial prompt + mixed source), no tools, max_tokens 32,000, no retries.",
        block=True, anchor="submitted-prompt"))
    # 2. four author-assist drafts
    drafts = [
        ("author-fable", "Claude Fable 5.2 · reasoning max", "“Musk’s Blueprint Is Shelved Under Science Fiction” · 929 words · $1.270520", "development/author-alternatives/01-claude-fable-5.2-full.md"),
        ("author-astra", "GPT-6 Astra · reasoning max", "“Starship’s Real Test Isn’t the Catch” · 903 words · $0.984643", "development/author-alternatives/02-gpt-6-astra-full.md"),
        ("author-carbon", "Gemini 4 Carbon · reasoning high", "“What SpaceX Caught in Those Mechanical Arms Is Bigger Than a Rocket” · 980 words · $0.085188", "development/author-alternatives/03-gemini-4-carbon-full.md"),
        ("author-muse", "Muse Wonder · reasoning max", "“Catching a Rocket Is the First Step Toward a Post-Scarcity World” · 899 words · $0.109564", "development/author-alternatives/04-muse-wonder-full.md"),
    ]
    for anchor, who, meta, rel in drafts:
        parts.append(_ai(who + " · author-assist draft",
                         f'<p class="meta-line">{html.escape(meta)}</p>'
                         + _artifact("Full output: thesis, pressure-test, outline, draft", P(rel), anchor)))
    parts.append(_ai(GROK + " · comparison",
                     "<p>Side-by-side comparison of the four drafts, with cautions: Muse&rsquo;s lede describes a booster catch; Gemini claims full two-stage reuse; Fable opens by saying it cannot confirm the flight.</p>"
                     + _artifact("Author comparison (as written, before the machine runs)", P("development/author-comparison.md"), "author-comparison")))
    # 3. machine runs
    parts.append(_human(
        "t293u",
        "<p>The author added constraints for the machine essay (rank only the top five; state Flight 15&rsquo;s rank if it falls outside them) and left the choice of machine essay to the editor.</p>",
        described=True))
    parts.append(_step(
        "Machine prompt = the author&rsquo;s two questions verbatim + a format paragraph (900–1,300 words, title and dek, top five only). "
        f'One message, no system prompt, no tools, no source, no drafts (<a href="{src("metadata/isolation.json")}">isolation record</a>).'
        + _artifact("Full machine prompt as sent", P("development/machine-question.md"), "machine-question"),
        block=True, anchor="alternatives"))
    parts.append(_step(
        "<b>Claude Fable 5.2, attempt 1 failed</b>: <code>finish_reason: length</code>, all 32,000 tokens spent on reasoning, no essay ($1.282784). "
        f'Retried once with the identical message and max_tokens 64,000 (<a href="{src("development/records/machine-01-claude-fable-5.2-attempt1-length-result-scrubbed.json")}">record</a>).'))
    machine = [
        ("machine-fable", "Claude Fable 5.2 · reasoning max · attempt 2", "“Where the Starship Catch Ranks, and What It Could Change” · ranks Flight 15 6th · 1,192 words · $1.879704 · selected unchanged; same bytes as the freeze", "development/machine-alternatives/01-claude-fable-5.2.md"),
        ("machine-carbon", "Gemini 4 Carbon · reasoning high", "“Catching Fire, Opening the Sky” · 7th (lists five) · 1,143 words · $0.159456", "development/machine-alternatives/02-gemini-4-carbon.md"),
        ("machine-astra", "GPT-6 Astra · reasoning max", "“What a Starship Catch Could Change” · 6th · 1,073 words · $0.718110", "development/machine-alternatives/03-gpt-6-astra.md"),
        ("machine-muse", "Muse Wonder · reasoning max", "“Catching the Future” · 6th · 1,112 words · $0.167556", "development/machine-alternatives/04-muse-wonder.md"),
    ]
    for anchor, who, meta, rel in machine:
        parts.append(_ai(who + " · machine-only essay",
                         f'<p class="meta-line">{html.escape(meta)}</p>' + _artifact("Full essay as returned", P(rel), anchor)))
    parts.append(_ai(GROK + " · machine selection (delegated)",
                     "<p>Chose Claude Fable 5.2, attempt 2, unchanged and not combined. Muse Wonder was a close second.</p>"
                     + _artifact("Selection note", P("development/machine-comparison.md"), "machine-comparison")))
    # 4. author choice and revisions
    parts.append(_human(
        "Fable-selection message",
        "<p>The author picked Claude Fable 5.2 for the human/AI essay (Muse second), because it &ldquo;brilliantly incorporates parts of the culture series&rdquo;. Use Gemini 4 Carbon&rsquo;s title. Fix or replace the &ldquo;awkward fact … libertarian admirers&rdquo; passage, since Musk aims for a post-monetary society.</p>",
        described=True))
    parts.append(_ai(GROK + " · revision options",
                     '<p>Offered Option A (rewrite with a verified Musk quote) and Option B (replace with &ldquo;to be sure&rdquo; material from other drafts), plus a fact check of the rest of the essay. '
                     f'<a href="{src("development/revision-history/ISSUE-037-revision-options-tracked.pdf")}">Tracked PDF</a>.</p>'
                     + _artifact("Fable 5.2 draft as returned", P("development/revision-history/original-fable-essay.md"), "rev-original")
                     + _artifact("Option A (offered, not chosen)", P("development/revision-history/option-A.md"), "rev-a")
                     + _artifact("Option B (offered, not chosen)", P("development/revision-history/option-B.md"), "rev-b"),
                     anchor="revisions"))
    parts.append(_human("t295u", _esc_quote(DECISION_QUOTES["t295u"]), anchor="t295u"))
    parts.append(_ai(GROK + " · Option C",
                     "<p>Applied as Option C: Fable&rsquo;s sentences kept, &ldquo;And there is&rdquo; became &ldquo;To some, there is&rdquo;, and the Musk lines moved to a new paragraph after &ldquo;To be sure&rdquo;.</p>"
                     + _artifact("Option C (before the last tweak)", P("development/revision-history/option-C.md"), "rev-c")))
    parts.append(_human("t296u", _esc_quote(DECISION_QUOTES["t296u"]), anchor="t296u"))
    parts.append(_step(
        f"<b>Author essay frozen</b>, 970 words, sha256 <code>{AUTHOR_HASH}</code>. Differences from Fable&rsquo;s draft: the title, &ldquo;To some, there is&rdquo;, the new Musk paragraph, and &ldquo;And the remaining objections strengthen the case.&rdquo;"
        + _artifact("Frozen author essay", P("essays/author-essay-FROZEN.md"), "freeze"),
        block=True))
    parts.append(_step(f"<b>Machine essay frozen</b> about 10:25 PM, byte-identical to the model output, sha256 <code>{MACHINE_HASH}</code>."))
    parts.append(_human("t297u", _esc_quote(DECISION_QUOTES["t297u"]), anchor="t297u"))
    parts.append(_step("Stage C critique: four calls, each critic shown one freeze; $0.365082, no retries. Findings stay in the audit, not the essays."))
    critics = [
        ("Kimi K3 · reasoning high · critic of the author essay", "audit/stage-c/humanai-leg-a-kimi-k3.md"),
        ("Claude Opus 4.1 · critic of the author essay", "audit/stage-c/humanai-leg-b-claude-opus-4.1.md"),
        ("Kimi K3 · reasoning high · critic of the machine essay", "audit/stage-c/machine-leg-a-kimi-k3.md"),
        ("Claude Opus 4.1 · critic of the machine essay", "audit/stage-c/machine-leg-b-claude-opus-4.1.md"),
    ]
    for who, rel in critics:
        parts.append(_ai(who, _artifact("Objections as returned", P(rel))))
    parts.append(_step("Grok Bot prepared the audit, source page and editorial note. Audit PR 49 merged 10:39 PM and web PR 51 merged 10:40 PM: Issue 37 is live."))
    parts.append(_human("t298u · after the 10:40 PM merges", _esc_quote(DECISION_QUOTES["t298u"]), anchor="t298u"))
    parts.append(_step("Post-publication status and Ruling A for both essays recorded (audit PR 50, 10:48 PM)."))
    parts.append('<div class="day">Sunday, November 15, 2026 · times PST</div>')
    parts.append(_step("Audio companions linked from both essays (audit PR 51 and web PR 52, 7:02 AM)."))
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
<p class="kicker">The World Behind the Words &middot; Issue 37 &middot; Extended Development Record</p>
<h1>Extended Development Record — {html.escape(AUTHOR_TITLE)}</h1>
<p class="lede">Issue 37, November 14, 2026, by Synthia Cipher. The conversation behind both essays, start to finish: what the author said, what each model returned, and what the editor did. The essay companions are live. Audio companions are linked above.</p>
{nav_top("development")}
<div class="frame"><span class="frame-name">Read first — what this record is</span>
<p>Issue 37 is two essays and a source page. The human/AI essay starts from Claude Fable 5.2&rsquo;s draft, with Gemini 4 Carbon&rsquo;s title and three edits the author approved. The machine essay is Claude Fable 5.2&rsquo;s answer to the author&rsquo;s two questions, selected unchanged by Grok Bot; none of the machine runs saw the author&rsquo;s source. The critics were Kimi K3 and Claude Opus 4.1, each shown one freeze.</p>
{PREP_NOTE}
{AUDIO_NOTE}
<p>{html.escape(STATUS)}</p>
<p><strong>Coverage.</strong> The author&rsquo;s turns marked verbatim are quoted exactly from the session (t292u excerpt, t295u, t296u, t297u, t298u). Two author turns are marked &ldquo;described, not verbatim&rdquo; because their exact text is not in the record. Model turns are the full outputs as returned. Grok Bot&rsquo;s turns are its delivered artifacts and a one-line summary of each; its chat replies are not reproduced. Exact assistant timestamps are not available. This record shows process and constraint. It does not prove the essays or their forecasts.</p>
</div>
<div class="chat-legend" aria-label="Legend">
<span><i class="k-human" aria-hidden="true"></i> Right, blue: <b>Synthia Cipher (author)</b></span>
<span><i class="k-ai" aria-hidden="true"></i> Left, grey: <b>AI</b>, labeled by model (Fable, Astra, Gemini, Muse, Kimi, Opus) or Grok Bot</span>
<span><i class="k-note" aria-hidden="true"></i> Centre: process steps (runs, freezes, hashes, audits)</span>
<span>Inside the source material: highlighted text is the author&rsquo;s; plain text is Grok Heavy research</span>
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
<p class="meta">Every public file for Issue 37.</p>
{index}
{nav_bottom("development")}
</body>
</html>
"""


INDEX_ROW = """          <article class="issue-row" data-issue-row data-status="complete" data-search="37 issue 37 what spacex caught in those mechanical arms is bigger than a rocket where the starship catch ranks and what it could change starship flight 15 culture iain banks musk source material grok heavy ruling a findings recorded companions live audio companion spotify machine companion machine-version issue-037-source-material">
            <div class="issue-index">37</div>
            <div class="issue-copy"><a href="https://scipher888.github.io/signal-noise-audit-snapshot/issues/issue-037/">What SpaceX Caught in Those Mechanical Arms Is Bigger Than a Rocket</a></div>
          </article>
"""


def patch_index() -> None:
    text = ISSUES_INDEX.read_text(encoding="utf-8")
    text = text.replace(">36 issues shown<", ">37 issues shown<")
    if "issues/issue-037/" not in text:
        needle = '          <article class="issue-row" data-issue-row data-status="complete" data-search="36 issue 36'
        if needle not in text:
            raise SystemExit("issues index anchor for issue 36 not found")
        text = text.replace(needle, INDEX_ROW + needle, 1)
    else:
        text = re.sub(
            r'          <article class="issue-row" data-issue-row data-status="complete" data-search="37 issue 37.*?</article>\n',
            INDEX_ROW,
            text,
            count=1,
            flags=re.S,
        )
    ISSUES_INDEX.write_text(text, encoding="utf-8")


# Written before publication; rendered unchanged, with a page note that their status lines are historical.
HISTORICAL = ("audit/dual-audit.md", "audit/execution-method.md", "audit/stage-c-synthesis.md", "development/DECISION-RECORD.md", "development/machine-comparison.md", "development/author-comparison.md")

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
        if blob.count(f'href="{AUTHOR_AUDIO}"') < 2 or blob.count(f'href="{MACHINE_AUDIO}"') < 2:
            raise SystemExit(f"audio companion links missing in {name}")
        if blob.count(">Audio companion</a>") != 4:
            raise SystemExit(f"audio nav count drifted in {name}")
        if "open.spotify.com/embed" in blob or "spotify.com/episode/" in blob.replace(AUTHOR_AUDIO, "").replace(MACHINE_AUDIO, ""):
            raise SystemExit(f"unexpected Spotify URL in {name}")
        for stale_audio in ("No audio has been added", "No audio exists", "No audio.", "no audio companion", "Issue 37 has no audio"):
            if stale_audio in blob:
                raise SystemExit(f"stale no-audio status {stale_audio!r} in {name}")
        current = blob
        for hist in HISTORICAL:
            for page_dir in ("", "machine-version/audit", "development"):
                current = current.replace(prose_html(hist, page_dir), "")
        for stale in (
            "Prepared, not published",
            "prepared for review",
            "Prepared for review",
            "do not resolve",
            "unmerged Signal",
            "awaits confirmation",
            "recorded provisionally",
            "Rulings pending",
            "The newsletter page will be",
        ):
            if stale in current:
                raise SystemExit(f"stale status wording {stale!r} in {name}")
        if "Ruling A for both essays, confirmed November 14, 2026" not in blob:
            raise SystemExit(f"confirmed ruling missing in {name}")
        if blob.count("The conversation behind this") < 2 or blob.count("Source material") < 2:
            raise SystemExit(f"nav incomplete in {name}")
        if "Written without AI</dt>" in blob:
            raise SystemExit(f"wrong companion label in {name}")
    for name, blob in (("author", author), ("maudit", maudit), ("dev", dev)):
        if LIVE_MARK not in blob or WEB_MERGE not in blob:
            raise SystemExit(f"live-companion status missing in {name}")
    if "225625" not in author or "275127" not in author:
        raise SystemExit("audio verification note missing from the author audit")
    if "The newsletter page is live" not in machine or "The live public page is" not in machine:
        raise SystemExit("machine inspection page still describes the companion as unpublished")
    if "prepared for review" in index.split("data-search=\"37 issue 37", 1)[-1].split("</article>", 1)[0]:
        raise SystemExit("index keywords still say prepared for review")
    # machine essay: two exact questions, editor's note, unchanged paragraphs
    for q in QUESTIONS:
        if f'<p class="provenance-question">{html.escape(q)}</p>' not in machine:
            raise SystemExit("machine question not verbatim on inspection page")
    if "Editor&rsquo;s note." not in machine or FLIGHT_SOURCE not in machine:
        raise SystemExit("editor's note missing on machine inspection page")
    if machine.index("</aside>") > machine.index("Judged purely by difficulty"):
        raise SystemExit("provenance aside must precede the essay")
    essay = read_src("essays/machine-essay-FROZEN-v1.0.md")
    for para in [p.strip() for p in essay.split("\n\n")]:
        if para.startswith("#") or para.startswith("*"):
            continue
        if html.escape(para, quote=False) not in machine and para not in machine:
            raise SystemExit("machine essay paragraph missing from inspection page")
    author_essay = read_src("essays/author-essay-FROZEN.md")
    for para in [p.strip() for p in author_essay.split("\n\n") if p.strip() and not p.startswith("**")]:
        plain = re.sub(r"\*([^*]+)\*", r"\1", para)
        dev_plain = html.unescape(re.sub(r"<[^>]+>", "", dev))
        if plain not in dev_plain:
            raise SystemExit("author freeze paragraph missing from development record")
    # source material: concatenated highlighted text equals the verbatim file
    mix = re.search(r'<div class="src-mix">(.*?)</div>', dev, re.S).group(1)
    if html.unescape(re.sub(r"<[^>]+>", "", mix)) != read_src("essays/source-material-VERBATIM.md"):
        raise SystemExit("source material on development page is not verbatim")
    if dev.count('<span class="src-h">') != 5:
        raise SystemExit("author passages are not all marked")
    for token in ["A1", "A6", "A11", "A12", "A18", "M1", "M5", "M11", "FLOOR", "Strange Horizons", "0.1 mm", "Ship 42"]:
        if token not in author or token not in maudit:
            raise SystemExit(f"finding {token} missing from an audit page")
    if "floor pass" in author.lower() or "floor pass" in maudit.lower():
        raise SystemExit("floor pass language slipped in")
    for anchor in ["author-fable", "author-astra", "author-carbon", "author-muse", "machine-fable", "machine-carbon", "machine-astra", "machine-muse", "machine-question", "revisions", "source-material"]:
        if f'id="{anchor}"' not in dev:
            raise SystemExit(f"missing development section {anchor}")
    if str(COST_TOTAL) not in author or str(COST_TOTAL) not in dev or AUDIT_COST not in author:
        raise SystemExit("cost missing")
    if "issue-037/" not in index or ">37 issues shown<" not in index or "issues/issue-036/" not in index:
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
    print("issue 37 check ok")


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
