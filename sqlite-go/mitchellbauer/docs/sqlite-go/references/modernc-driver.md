# modernc.org/sqlite Driver Notes

## Package role

`modernc.org/sqlite` is a pure Go SQLite driver used through `database/sql`.
This pack targets driver version `1.61.1`, which embeds SQLite `3.54.1`.

Typical import and open pattern:

```go
import (
    "database/sql"
    _ "modernc.org/sqlite"
)

db, err := sql.Open("sqlite", dbPath)
```

## Why teams choose it

- no CGO requirement
- easier cross-platform builds in many environments
- works with standard `database/sql` patterns

## What stays the same

Most SQL and schema behavior comes from SQLite itself, not from the Go driver.
That means the real documentation priority is usually:

1. official SQLite SQL behavior
2. Go `database/sql` usage
3. driver-specific operational notes

## Connection guidance

Open the DB once at startup, verify it with a ping or startup query if that fits
your app style, and share the `*sql.DB` handle through your repository layer.

## Practical caution

If you need advanced connection tuning, WAL behavior, busy timeouts, or other
runtime-specific settings, document and test those as app decisions instead of
assuming a driver default will always be enough.

## Dependency alignment

Do not independently force an arbitrary `modernc.org/libc` version. Use the
version selected by `modernc.org/sqlite` unless a tested application-specific
constraint requires otherwise.

Pin the driver explicitly:

```bash
go get modernc.org/sqlite@v1.61.1
```

## Advanced APIs

Version 1.54.0 includes Go-facing facilities for virtual tables, connection
hooks, pre-update and rollback hooks, incremental backup inspection, and custom
page caches. These APIs are optional; ordinary applications can continue using
the blank import and `database/sql`.

## Source

- https://pkg.go.dev/modernc.org/sqlite

## Current upgrade requirements

Version 1.61.1 requires Go 1.26 and pins modernc.org/libc v1.79.0.
Use `file:` URIs for SQLite URI options such as `mode=ro`; a plain
filename with `?mode=ro` does not enforce read-only access.
See `release-deltas/modernc-sqlite-1.61.1.md` before upgrading.
