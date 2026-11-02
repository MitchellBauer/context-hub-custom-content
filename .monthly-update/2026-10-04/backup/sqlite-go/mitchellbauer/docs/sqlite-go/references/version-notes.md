# Version Notes

## Version target in this pack

This BYOD entry targets `modernc.org/sqlite` version `1.54.0`.

`Quiz-Runner` still declares version `1.39.1`. Treat this pack as forward-looking
for that project until its module dependency is upgraded and its database tests
pass.

## What this pack is based on

- official SQLite documentation for SQL semantics, `PRAGMA`, table creation, and upserts
- `pkg.go.dev` package documentation for `modernc.org/sqlite`
- practical Go usage through `database/sql`

## Scope choice

This pack focuses more on SQLite behavior than on driver-specific API details,
because most day-to-day work in apps like yours is about SQL design, migrations,
transactions, and repository patterns.

Driver-specific features added after 1.39.1 include pre-update and rollback
hooks, virtual-table support, richer backup progress, and pluggable page-cache
APIs. Load `release-deltas/modernc-sqlite-1.54.0.md` when planning an upgrade.

The driver documentation warns that applications should use the same
`modernc.org/libc` version selected by the driver's own `go.mod`.
