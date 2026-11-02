# HTMX 2.0.9 Delta

## Upgrade target

- Previous pack version: `2.0.7`
- New pack version: `2.0.9`
- Official release date: April 15, 2026

## Changes relevant to Go applications

### History and `HX-Location`

- Structured `HX-Location` responses now honor `replace` when `push` is false.
- Relative history paths resolve against the current page URL.

Test handlers that construct `HX-Location`, `HX-Push-Url`, or
`HX-Replace-Url` responses and any page using relative navigation.

### Disabled controls

`hx-disabled-elt` now preserves controls that were already disabled in the
server-rendered HTML.

### Swap cleanup

HTMX no longer leaves an empty `class=""` after removing its request and swap
utility classes.

### OOB diagnostics

`htmx:oobErrorNoTarget` now includes the selector that failed to match, making
out-of-band swap problems easier to diagnose.

## Compatibility

No Go handler API changes are required. Existing HTMX 2.x attributes, request
headers, response headers, and fragment-rendering patterns remain valid.

## 2.0.10 caveat

HTMX 2.0.10 restores TypeScript definitions accidentally omitted from 2.0.9.
This pack intentionally remains pinned to 2.0.9.

## Official sources

- https://github.com/bigskysoftware/htmx/releases/tag/v2.0.9
- https://raw.githubusercontent.com/bigskysoftware/htmx/v2.0.9/CHANGELOG.md
