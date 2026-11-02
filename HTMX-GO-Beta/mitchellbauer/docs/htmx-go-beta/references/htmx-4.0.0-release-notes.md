# HTMX 4.0.0 Release Notes

Released August 28, 2026; first stable HTMX 4 release. The npm `latest` tag
continues to select HTMX 2, so install `htmx.org@4.0.0` explicitly.

## Changes since beta6

- `hx-query` provides a core shorthand for QUERY requests.
- SSE, WebSocket, and multipart streaming behavior and event conventions were refined.
- Multipart streams gained resume cursors and connection details.
- `htmx.initialize()` supports asynchronous initialization.
- Requests made with `htmx.ajax()` support abort events.
- `<hx-partial>` accepts extended selectors.
- Array-valued custom elements submit repeated fields.

Go routes and middleware must explicitly allow QUERY if adopted; verify proxy
support before depending on it. Test reconnects, cancellation, and incomplete
streams before introducing streaming responses.

## Sources

- https://github.com/bigskysoftware/htmx/releases/tag/v4.0.0
- https://raw.githubusercontent.com/bigskysoftware/htmx/four/CHANGELOG.md
- https://four.htmx.org/announcements/2026-08-28-htmx-4.0.0-is-released
