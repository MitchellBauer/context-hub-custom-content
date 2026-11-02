# HTMX 4.0.1 Release Notes

Released November 1, 2026 (npm 23:05 UTC), the first HTMX 4 patch release.
npm tags: `next` = 4.0.1, `latest` = 2.0.11 (HTMX 2). Install
`htmx.org@4.0.1` explicitly.

## Changes

- Any trigger cancels a pending `delay` or `throttle` trigger on the same
  element, as in 2.x.
- An older response no longer overwrites a newer one with `hx-sync` replace
  (#4028).
- A response with only `hx-partial` no longer blanks the body; `ignoreTitle`
  works in `hx-partial`.
- History back/forward is more reliable; `hx-history-cache` POST stamp fixed
  (#4067).
- `hx-trigger` works on boosted elements (#4127).
- `every 2s [cond]` honors its filter (#4133).
- `changed` modifier fixed on forms and for several `changed` triggers on one
  element (#4035, #4096).
- `scrollTarget` and `showTarget` work with `window`, `document` (#4159) and
  relative selectors (#4089).
- `intersect` supports `from` (#4080).
- `hx-sse`, `hx-multipart`: reconnect timeout for unresponsive servers (#4099).
- `hx-live`: boolean attribute binding with `:?attr` (#4022).
- `hx-download`: `ctx` exposed in events (#4152); prefers `filename*` (#4043).
- `hx-head` no longer appends duplicate titles (#4083).
- `implicitInheritance` no longer inherits verbs, `hx-action` or `hx-trigger`
  (the source also stops inheriting `hx-validate`).
- Works around Chrome 150-156 dropping HTML comments when parsing (#4150).
- `htmx-2-compat`: corrected timing of `htmx:load`, `htmx:afterOnLoad`,
  `htmx:beforeOnLoad` and `htmx:beforeProcessNode`.
- Upgrade guide and `upgrade-check` event mappings corrected (#4128).
- Stale `hx-compat` and `hx-optimistic` files removed from `dist/ext` (#4042).
  `htmx-2-compat` is still shipped.

Also visible in the source diff:

- A swap is skipped when its target was removed from the page during the
  request.
- A request timeout now fires `htmx:error`; other aborts don't.
- A named submit button that owns `hx-post` is treated as its own submitter
  (#4073).
- A POST from `document.body` sends no body.

## Go impact

- Drop-in for 4.0.0 apps that already use explicit inheritance. If you relied
  on `implicitInheritance` for verbs, `hx-action`, `hx-trigger` or
  `hx-validate`, move them onto each element.
- Re-test history (back/forward) and any `delay`/`throttle` triggers.
- Update the vendored file and its recorded checksum:
  - `dist/htmx.min.js` SHA-256 `a0abb04f2f45a1f89d1d4844023245537e5e6014c87b144553e0607b4cc32130`
  - SRI `sha384-Qp9rdC8H7EqOoX+nR0P3RPG2Noji+qdwJlGpfzwQJsfOpp3sGwIdSP9xO3+UlEhn`

## Sources

- https://github.com/bigskysoftware/htmx/releases/tag/v4.0.1
- npm `htmx.org@4.0.1` (dist diffed against 4.0.0)
