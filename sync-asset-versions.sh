#!/bin/sh
#
# Sync the cache-busting ?v= string on every page to the CONTENT of the shared assets.
#
# Why this exists
# ---------------
# Pages hard-code `assets/styles.css?v=SOMETHING`. When someone edits the shared
# stylesheet and bumps that string on only the page they were working on, every
# other page keeps requesting the old string — so returning visitors keep the old
# cached CSS. That is invisible until someone edits a *shared* rule rather than
# appending a new one, and then it looks like a page bug rather than a caching one.
#
# The fix is to stop choosing the version. Here the version IS the file's content
# hash, so it cannot disagree with the file it names. Edit the CSS, run this, and
# every page is correct by construction.
#
# Usage
# -----
#   ./sync-asset-versions.sh          # rewrite pages to match current asset content
#   ./sync-asset-versions.sh --check  # report drift and exit 1; changes nothing
#
# Run it after ANY change to assets/styles.css or assets/site.js, before committing.
# Forgetting is recoverable: running it later fixes every page at once.
#
set -eu

cd "$(dirname "$0")"

CHECK=0
[ "${1:-}" = "--check" ] && CHECK=1

drift=0

for asset in styles.css site.js; do
  path="assets/$asset"
  if [ ! -f "$path" ]; then
    echo "error: missing $path" >&2
    exit 1
  fi

  # Version = first 8 hex chars of the asset's own sha256. Derived, never chosen.
  hash=$(shasum -a 256 "$path" | cut -c1-8)

  # Escape dots so the regex matches literally (styles.css, not stylesXcss).
  esc=$(printf '%s' "$asset" | sed 's/\./\\./g')

  # A page is stale if it references the asset with a ?v= that is not the current hash.
  # (macOS grep has no -P, so this compares against the desired string rather than
  # using a negative lookahead.)
  stale=$(grep -rl -E "assets/$esc\?v=[A-Za-z0-9]+" --include='*.html' . 2>/dev/null \
          | while read -r f; do
              if grep -q -E "assets/$esc\?v=[A-Za-z0-9]+" "$f" && \
                 ! grep -q "assets/$esc?v=$hash" "$f"; then printf '%s\n' "$f"; fi
            done)

  n=$(printf '%s' "$stale" | grep -c . || true)

  if [ "$n" -eq 0 ]; then
    printf '  %-12s ?v=%s  — all pages current\n' "$asset" "$hash"
    continue
  fi

  drift=$((drift + n))

  if [ "$CHECK" -eq 1 ]; then
    printf '  %-12s ?v=%s  — %s page(s) STALE\n' "$asset" "$hash" "$n"
    printf '%s\n' "$stale" | sed 's/^/       /'
    continue
  fi

  printf '%s\n' "$stale" | while read -r f; do
    [ -n "$f" ] && sed -i '' -E "s|assets/$esc\?v=[A-Za-z0-9]+|assets/$asset?v=$hash|g" "$f"
  done
  printf '  %-12s ?v=%s  — updated %s page(s)\n' "$asset" "$hash" "$n"
done

if [ "$CHECK" -eq 1 ] && [ "$drift" -gt 0 ]; then
  echo
  echo "Drift found. Run ./sync-asset-versions.sh to fix." >&2
  exit 1
fi

exit 0
