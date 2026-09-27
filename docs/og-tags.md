# Open Graph tags for machine companion pages

Machine companion landings live at `issues/issue-NNN/machine-version/index.html`. This repository has no page template, generator, or landing checklist that creates those files. Copy the block below into `<head>` of each new landing, after the existing title.

Author essays on [signalandnoise.email](https://www.signalandnoise.email/) already emit this card. A live example is [A Curious Machine Is Not a Kind One](https://www.signalandnoise.email/p/a-curious-machine-is-not-a-kind-one/).

Fill three values from the page itself:

- `og:title` and `twitter:title`: the machine essay title (the page `h1`).
- `og:description` and `twitter:description`: the page's existing meta description, copied verbatim.
- `og:url`: `https://scipher888.github.io/signal-noise-audit-snapshot/issues/issue-NNN/machine-version/` with a trailing slash.

`og:image` and `twitter:image` reuse the essay site's 1200×630 share image:

`https://www.signalandnoise.email/assets/preview.png?v=09b48f76`

Before reusing it, confirm that URL returns HTTP 200 with an image content type. If it does not, add a 1200×630 PNG in this repo (dark background, "Signal & Noise" and "Machine companion" text only) and point the image tags at that file's absolute GitHub Pages URL.

```html
<meta property="og:site_name" content="Signal &amp; Noise">
<meta property="og:type" content="article">
<meta property="og:title" content="ESSAY TITLE">
<meta property="og:description" content="META DESCRIPTION">
<meta property="og:url" content="https://scipher888.github.io/signal-noise-audit-snapshot/issues/issue-NNN/machine-version/">
<meta property="og:image" content="https://www.signalandnoise.email/assets/preview.png?v=09b48f76">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Signal &amp; Noise share image: a dark field, a pale arch, and a small amber square.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="ESSAY TITLE">
<meta name="twitter:description" content="META DESCRIPTION">
<meta name="twitter:image" content="https://www.signalandnoise.email/assets/preview.png?v=09b48f76">
```
