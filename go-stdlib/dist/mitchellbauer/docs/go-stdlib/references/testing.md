# testing and diagnostics

## Core packages

- `testing`
- `net/http/httptest`
- `testing/fstest`

## High-value patterns

- table-driven tests for parsing and validation logic
- `httptest` for handler verification
- focused fixtures instead of giant integration setups
- assertions on status code, headers, and response body shape

## Diagnostic helpers to remember

- `runtime` for runtime information
- `pprof` for profiling when performance investigation matters
- benchmarks in `testing` for hot paths

## Go 1.27 update

Go 1.27 adds `httptest.NewTestServer` for in-memory networking with
`testing/synctest`. Ordinary `httptest.NewServer` remains appropriate for
existing handler tests.

See `release-deltas/go1.27.1.md` and https://go.dev/doc/go1.27.
