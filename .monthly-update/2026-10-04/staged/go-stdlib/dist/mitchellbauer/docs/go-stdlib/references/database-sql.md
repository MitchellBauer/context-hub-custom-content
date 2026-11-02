# database/sql

## Role

`database/sql` is the standard abstraction for SQL database access in Go.

## High-value patterns

- open once at startup and share `*sql.DB`
- use context-aware query methods
- use explicit `SELECT` column lists
- isolate repeated scan logic in helpers
- wrap multi-step writes in transactions

## Common types

- `*sql.DB`
- `*sql.Tx`
- `*sql.Rows`
- `*sql.Row`
- `sql.NullString` and related nullable helpers

## Practical caution

`database/sql` is not an ORM. It works best when you keep SQL readable and explicit.

## Go 1.27 update

Go 1.27 adds `sql.ConvertAssign` and `driver.RowsColumnScanner`. With pgx
5.11 on Go 1.27, arrays and ranges can scan directly into Go destinations.
Test application-specific scanning conversions when upgrading.

See `release-deltas/go1.27.1.md` and https://go.dev/doc/go1.27.
