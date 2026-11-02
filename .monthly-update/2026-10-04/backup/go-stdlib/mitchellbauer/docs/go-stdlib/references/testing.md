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
