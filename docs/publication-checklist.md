# Public Snapshot Publication Checklist

**Status:** operational checklist v1 — published 2026-05-13  
**Snapshot date:** 2026-05-13

Use this before publishing the GitHub repository or updating a public snapshot.

## 1. Redaction check

Confirm the snapshot contains no:

- the author's real name;
- specific profession, employer, role, training, credentials, location, or workplace detail;
- family member details or family operations;
- private third-party details;
- confidential data;
- raw prompts containing private context;
- internal workspace paths;
- outreach lists, curator strategy, private metrics, or unpublished distribution tactics;
- API keys, tokens, account identifiers, or operational secrets.

## 2. Process-theater check

Confirm the snapshot does not claim:

- the process proves the work is trustworthy;
- having a constitution is itself evidence of truth;
- disclosure alone creates trust;
- AI involvement is either automatically good or automatically bad;
- Synthia Cipher is a fabricated persona, credential, or authority claim rather than a privacy pen name;
- AI tools are a personlike author, co-author, conscious entity, or signing identity;
- the author's identity or expertise is the reason to trust the publication.

Preferred framing:

> The process creates an audit surface. It does not create certainty.

Issue 26+ published-audit chrome uses “machine companion,” not “labeled.”

## 3. Link check

Verify all public links resolve:

- Signal & Noise homepage;
- public issue links;
- public process note links;
- any future `/bio` or homepage links to this repository.

## 3A. Shared-asset version check

If this change touched `assets/styles.css` or `assets/site.js`, every page that loads them
must request the current version. Run:

```bash
./sync-asset-versions.sh --check
```

Exit 0 means every page is current. Exit 1 lists the stale pages — run the script without
`--check` to fix them, then commit the result with the asset change, not separately.

Do not hand-pick a version string. It is the asset's content hash, so it is correct by
construction; choosing one by hand is the exact step that let the site drift to four
different strings across 39 pages. The failure is silent while the stylesheet is only ever
appended to, and surfaces as an inconsistent layout bug the first time a shared rule is
modified.

## 4. Version check

Before public push:

- remove “candidate” status language or explicitly publish as a draft if that is the intent;
- assign version number;
- create or update changelog if needed;
- tag the Git commit after publication approval.

## 5. Approval check

No public GitHub repository creation or push until the author explicitly approves the exact snapshot.

Approval should cover:

- repository name;
- public visibility;
- included files;
- license posture;
- whether claim IDs mirror internal IDs;
- whether the snapshot is linked from `/bio` immediately or after a second review.

## 6. Suggested GitHub repo settings

Recommended initial repository name:

`signal-noise-audit-snapshot`

Recommended description:

`Public-safe editorial constitution and corrections/change-log snapshots for Signal & Noise.`

Recommended visibility:

Public, only after approval.

Recommended license posture for v1:

All rights reserved unless the author chooses a reuse license later.
