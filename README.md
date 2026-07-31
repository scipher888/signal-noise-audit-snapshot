# Signal & Noise — Public Audit Snapshot

**Status:** public snapshot v1.2 — published 2026-07-31 (v1.1 and v1.0 remain archived); low-cognitive-load redesign prepared 2026-06-18
**Snapshot date:** 2026-07-31
**Publication:** Signal & Noise — https://www.signalandnoise.email

Signal & Noise is written under the pen name **Synthia Cipher**. AI tools draft and critique; the human author owns the editorial judgment, final wording, published claims, and errors. If something is wrong, the fault is the author's, not the algorithm's.

This repository is a public-safe snapshot of the editorial audit trail. It is meant to make the process inspectable enough to support correction and accountability. The reader-facing site now uses a lighter “World Behind the Words” orientation layer: a map, not a certification of truth.

## What is included

- [`world/`](https://scipher888.github.io/signal-noise-audit-snapshot/world/) - public doorway for The World Behind the Words.
- [`issues/`](https://scipher888.github.io/signal-noise-audit-snapshot/issues/) - issue-specific Origin / Structure / Reference scaffolds.
- [`signal-noise/`](https://scipher888.github.io/signal-noise-audit-snapshot/signal-noise/) - publication-level Origin / Structure / Reference scaffold.
- [`assets/`](assets/) - shared static CSS and JavaScript for the redesigned orientation layer.
- [`docs/editorial-constitution-v1.2.md`](docs/editorial-constitution-v1.2.md) — current public-safe snapshot of the editorial / epistemic constitution (v1.2, 2026-07-31; changelog inside). Prior snapshots remain accessible and unchanged: [`v1.1`](docs/editorial-constitution-v1.1.md) and [`v1.0`](docs/editorial-constitution-v1.0.md).
- [`docs/corrections-and-changes-v1.md`](docs/corrections-and-changes-v1.md) — public-safe corrections, changes, and tracked claims surface.
- [`docs/snapshot-cadence.md`](docs/snapshot-cadence.md) — versioning and milestone snapshot rules.
- [`docs/publication-checklist.md`](docs/publication-checklist.md) — what must be checked before publishing or updating this snapshot.

## What is intentionally not included

- Raw drafts, raw prompts, private notes, or internal workspace paths.
- Private operational strategy, outreach lists, metrics, or unpublished experiments.
- Family, personal, professional, location, employer, or identifying biographical details.
- Any confidential data or third-party private material.

## Design principle

This is a map, not a certification of truth.

The standard is: **can a reader see what the process claims to require, where outside references can press on the work, and where future corrections would appear?**

If not, the process is theater.

## Run locally

From this repository:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.

## Shared assets and cache-busting

Every page hard-codes a cache-busting query on the shared stylesheet and script —
`assets/styles.css?v=…`. **Do not choose that string by hand.** It is derived from the
asset's own content hash, so it cannot disagree with the file it names:

```bash
./sync-asset-versions.sh          # rewrite every page to match current asset content
./sync-asset-versions.sh --check  # report drift, change nothing, exit 1 if stale
```

**Run it after any change to `assets/styles.css` or `assets/site.js`, before committing.**

This exists because of a real failure. Pages were bumped one at a time by whoever was
editing them, and the site drifted to four different version strings across 39 pages.
Nothing looked broken, because the stylesheet had only ever been *appended* to — a page
holding a stale string still got every rule it needed. The damage would have arrived the
first time someone *modified* a shared rule: pages on old strings would keep serving the
old CSS to returning visitors, and it would present as a layout bug on some pages and not
others, which is a genuinely nasty thing to debug.

Deriving the version from content removes the human step that was failing. Forgetting to
run the script is recoverable — run it later and every page is fixed at once — and running
it twice does nothing, so it is safe in any hook, script, or habit.

## Publication

This snapshot was first published as **v1.0** at https://github.com/scipher888/signal-noise-audit-snapshot, approved 2026-05-13 after redaction checks, link verification, and snapshot-cadence review. **v1.1** followed on 2026-06-09, making the pre-draft anchor admission rule public. The current constitution is **v1.2** (2026-07-31), carrying the Landing Slate and Opinion Piece amendments. Material changes follow [`docs/snapshot-cadence.md`](docs/snapshot-cadence.md).
