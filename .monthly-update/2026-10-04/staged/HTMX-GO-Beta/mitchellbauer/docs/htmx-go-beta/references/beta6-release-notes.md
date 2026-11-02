# HTMX 4.0.0-beta6 Release Notes

Historical reference only. Current guidance targets 4.0.0; see
`htmx-4.0.0-release-notes.md`.

## Release

- Version: `4.0.0-beta6`
- Released: July 23, 2026
- Status: pre-release

## Beta6 changes

- New `hx-multipart` extension for streamed `multipart/mixed` and
  `multipart/parallel` responses, with per-part `HX-*` action headers
- History scroll restoration through the Navigation API with a Firefox fallback
- `HCON` exposed to extensions
- Custom request methods such as `query`
- Breaking event rename from `htmx:swap:finally` to `htmx:finally:swap`
- `HX-Trigger` response events now fire after swapping
- `hx-live` avoids no-change updates and caches compiled `safeEval` tags
- `hx-ws` forwards WebSocket protocols and includes implementation refinements
- Better trusted-types behavior in the optimistic extension
- Manual input-value collection for custom elements

## Go impact

The server-facing changes most likely to matter are:

- custom methods may require explicit routing and authorization
- multipart streaming can carry multiple incremental HTML actions
- `HX-Trigger` event timing changed
- history behavior needs regression testing

Do not adopt the multipart or custom-method features without integration tests
covering proxies, middleware, cancellation, and partial failures.

## Official sources

- https://github.com/bigskysoftware/htmx/releases/tag/v4.0.0-beta6
- https://four.htmx.org/docs/
- https://four.htmx.org/docs/get-started/migration/
- https://four.htmx.org/reference/
