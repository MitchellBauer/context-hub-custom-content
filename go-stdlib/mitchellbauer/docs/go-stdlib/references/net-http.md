# net/http and Related Packages

## Core packages

- `net/http`
- `net/url`
- `mime/multipart`
- `net/http/httptest`

## High-value patterns

- `http.NewServeMux()` for route registration
- `http.Handler` and `http.HandlerFunc` for composition
- request-scoped `Context()` use
- `http.SetCookie` and explicit response headers
- `http.FileServer` for static assets
- `httptest.NewRecorder` and `httptest.NewRequest` for tests

## Good defaults

- keep handlers small and explicit
- validate request method, payload, and route params early
- set cache headers intentionally for dynamic HTML and static assets
- use `http.Redirect` for normal navigation and HTMX headers only when needed

## Nearby packages to remember

- `net/url` for query parsing and escaping
- `mime/multipart` for file upload handling
- `httptest` for handler tests

## Go 1.27 update

Go 1.27 drains a bounded amount of unread HTTP/1 response content on Close
for connection reuse and adds `Server.MaxHeaderValueCount`. Continue closing
response bodies promptly and explicitly configuring reusable transports.

See `release-deltas/go1.27.1.md` and https://go.dev/doc/go1.27.

## Current release guidance

Go 1.27.3 includes the intervening 1.27.2 security fixes for net/http and
net/textproto. See `release-deltas/go1.27.2.md`.
