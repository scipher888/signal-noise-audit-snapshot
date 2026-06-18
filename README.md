# Signal & Noise — Public Audit Snapshot

**Status:** public snapshot v1.1 — published 2026-06-09 (constitution v1.1; v1.0 remains archived); low-cognitive-load redesign prepared 2026-06-18
**Snapshot date:** 2026-06-09  
**Publication:** Signal & Noise — https://www.signalandnoise.email

Signal & Noise is written under the pen name **Synthia Cipher**. AI tools draft and critique; the human author owns the editorial judgment, final wording, published claims, and errors. If something is wrong, the fault is the author's, not the algorithm's.

This repository is a public-safe snapshot of the editorial audit trail. It is meant to make the process inspectable enough to support correction and accountability. The reader-facing site now uses a lighter “World Behind the Words” orientation layer: a map, not a certification of truth.

## What is included

- [`world/`](https://scipher888.github.io/signal-noise-audit-snapshot/world/) - public doorway for The World Behind the Words.
- [`issues/`](https://scipher888.github.io/signal-noise-audit-snapshot/issues/) - issue-specific Origin / Structure / Reference scaffolds.
- [`signal-noise/`](https://scipher888.github.io/signal-noise-audit-snapshot/signal-noise/) - publication-level Origin / Structure / Reference scaffold.
- [`assets/`](assets/) - shared static CSS and JavaScript for the redesigned orientation layer.
- [`docs/editorial-constitution-v1.1.md`](docs/editorial-constitution-v1.1.md) — current public-safe snapshot of the editorial / epistemic constitution (v1.1, 2026-06-09; changelog inside). Prior: [`docs/editorial-constitution-v1.0.md`](docs/editorial-constitution-v1.0.md), archived unchanged.
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

## Publication

This snapshot was first published as **v1.0** at https://github.com/scipher888/signal-noise-audit-snapshot, approved 2026-05-13 after redaction checks, link verification, and snapshot-cadence review. The constitution is now at **v1.1** (2026-06-09; one rule made public — see the changelog in the v1.1 file). Material changes follow [`docs/snapshot-cadence.md`](docs/snapshot-cadence.md).
