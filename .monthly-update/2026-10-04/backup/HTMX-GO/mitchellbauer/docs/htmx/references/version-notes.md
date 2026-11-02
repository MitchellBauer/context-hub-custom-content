# Version Notes

## Version target

This stable BYOD entry is pinned to HTMX `2.0.9`.

## HTMX 2.0.9

Released April 15, 2026, this is a maintenance release with no planned API
migration for Go handlers.

It fixes:

- `HX-Location` honoring `replace` when `push` is `false`
- relative history paths resolving against the current page
- empty `class=""` attributes left after HTMX utility classes are removed
- `hx-disabled-elt` preserving controls disabled in the source HTML

It also adds the failing selector to `htmx:oobErrorNoTarget` details and logs.

See `release-deltas/htmx-2.0.9.md` for the incremental update.

## Version caveat

HTMX 2.0.10 was tagged on April 21, 2026. It restores TypeScript definitions
accidentally omitted from 2.0.9 and improves selector escaping during settle
lookup.

This pack remains pinned to 2.0.9 by request. Browser-script users are not
affected by the missing TypeScript definition file, but TypeScript/npm users
should prefer 2.0.10.

## Scope

The pack covers stable HTMX 2.x semantics and Go server-rendering patterns.
HTMX 4 beta guidance is intentionally maintained in the separate
`mitchellbauer/htmx-go-beta` entry.

## Official sources

- https://github.com/bigskysoftware/htmx/releases/tag/v2.0.9
- https://raw.githubusercontent.com/bigskysoftware/htmx/v2.0.9/CHANGELOG.md
- https://github.com/bigskysoftware/htmx/releases/tag/v2.0.10
