# Migrating HTMX 2 Applications to HTMX 4

## Start with the upgrade checker

HTMX 4 includes a checker for templates and JavaScript:

```powershell
npx htmx.org@4.0.1 upgrade-check -- .\path\to\project
```

It requires Python 3 and reports file/line findings.

## Behavioral changes

- Requests use `fetch()` instead of `XMLHttpRequest`.
- Attribute inheritance is explicit by default.
- `4xx` and `5xx` bodies swap by default.
- The default request timeout is 60 seconds instead of unlimited.
- The default settle delay changes from 20 ms to 1 ms.

## Removed attributes

- `hx-vars`: use `hx-vals` with `js:`
- `hx-params`: use `htmx:config:request`
- `hx-prompt`: load the `hx-prompt` extension to retain prompt input
- `hx-ext`: include extension scripts directly
- `hx-disinherit` and `hx-inherit`: explicit inheritance makes them unnecessary
- `hx-request`: use `hx-config`
- `hx-history`: removed with the old local-storage history model

## Renamed controls

- HTMX 2 `hx-disable` becomes HTMX 4 `hx-ignore`
- HTMX 2 `hx-disabled-elt` becomes HTMX 4 `hx-disable`

Review these names carefully; a blind replacement can reverse intent.

## New controls

- `hx-action`: request URL
- `hx-method`: request method
- `hx-config`: per-element fetch/request configuration
- `hx-ignore`: disable HTMX processing
- `hx-status`: response handling by status

## Extension migration

- Replace `htmx.defineExtension()` with `htmx.registerExtension()`.
- Remove `hx-ext` attributes.
- Replace callback-style `onEvent` handling with event-specific hooks.
- Test SSE and WebSocket extensions separately because both were rewritten.

## Compatibility bridge

Use the `htmx-2-compat` extension to restore implicit inheritance, old event
names, and previous error-swapping defaults while migrating incrementally.

## Go handler checklist

- Detect `HX-Request-Type`.
- Return intentional HTML for `4xx` and `5xx`.
- Recheck `HX-Source` and `HX-Target` parsing.
- Remove dependencies on `HX-Trigger-Name` and `HX-Prompt` request headers.
- Remove `HX-Trigger-After-Swap` and `HX-Trigger-After-Settle` responses.
- Test history and relative URLs.
- Set `Vary` when one URL can produce full and partial HTML.

## Official source

- https://four.htmx.org/docs/get-started/migration/

## Additional migration checks

- DELETE no longer collects enclosing form inputs; add `hx-include="closest form"` when needed.
- Replace `hx-trigger` queuing modifiers with `hx-sync`.
- Quote selectors containing spaces or commas in `from:` and `target:` modifiers.
- Main swaps precede out-of-band swaps; check dependencies between targets.
- History restoration re-fetches pages instead of using a localStorage page cache.
- Rename `hx-encoding` to `hx-encode`.

Source: https://four.htmx.org/docs/whats-new-in-htmx-4
