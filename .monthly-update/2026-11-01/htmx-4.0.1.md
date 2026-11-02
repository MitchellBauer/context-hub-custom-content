# HTMX 4.0.1 evidence (November 1, 2026)

## Release

- npm `htmx.org` time: 4.0.0 `2026-08-28T12:56:49.159Z`, 4.0.1 `2026-11-01T23:05:38.097Z`
- npm dist-tags: `next` 4.0.1, `latest` 2.0.11
- GitHub release: https://github.com/bigskysoftware/htmx/releases/tag/v4.0.1
  (published 2026-11-01T23:06:22Z)

## Artifact

`npm pack htmx.org@4.0.1`, `package/dist/htmx.min.js`:

- SHA-256 `a0abb04f2f45a1f89d1d4844023245537e5e6014c87b144553e0607b4cc32130`
- SHA-384 (SRI) `Qp9rdC8H7EqOoX+nR0P3RPG2Noji+qdwJlGpfzwQJsfOpp3sGwIdSP9xO3+UlEhn`
- `https://cdn.jsdelivr.net/npm/htmx.org@4.0.1` returns the same bytes (SRI
  matched); package.json `jsdelivr` and `unpkg` point at `dist/htmx.min.js`.
- 4.0.0 `dist/htmx.min.js` SRI `BvJpBiO8Kh31EqtJe5DRIeWrHWnCGkwytKs9NKFi86Hhw96dEqdEMzZDeK9iEGTc`
  matched the previous pack, confirming the same file was compared.

## Source checks behind request-sync.md

From `dist/htmx.js` 4.0.1:

- `#determineSyncStrategy`: no `hx-sync` -> `"queue first"`; unknown text -> `"queue first"`.
- `#getRequestQueue`: `selector:strategy` uses the queue of
  `#findOrWarn(elt, selector)`, which supports extended selectors
  (`closest`, `find`, `next`, `previous`, `this`).
- `RequestQueue.admit`: `replace` (or a running `abort` request) aborts and
  clears; `queue all` appends; `queue last` replaces the queue; default queues
  only when empty; `drop`/`abort` are dropped while busy.
- `#handleTriggerEvent` builds the request body before `#issueRequest` admits
  it, so a queued request sends the values from trigger time.
- `#disableElements(ctx)`: `hx-disable` is a selector; elements are counted and
  re-enabled after the request.

## Diff against 4.0.0 also noted

- `implicitInheritance` stops inheriting `hx-action`, verbs, `hx-trigger` and
  `hx-validate`.
- Swap skipped if `ctx.target.isConnected === false`.
- `dist/ext/hx-compat*` and `hx-optimistic.min.js.map` removed;
  `htmx-2-compat` retained.

## Applied in

Fishbowl Reprint vendored 4.0.1 (commit 4e233fc) and added
`hx-sync="#main:drop" hx-disable="this"` to its Print and Retry buttons after a
double press was found to print two tags (commit 0af735c). Three presses sent
one request in a dry-run browser check.
