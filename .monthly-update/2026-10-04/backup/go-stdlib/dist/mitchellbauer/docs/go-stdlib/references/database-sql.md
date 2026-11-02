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
