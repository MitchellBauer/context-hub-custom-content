---
name: postgres-go
description: "Practical PostgreSQL patterns for Go apps using database/sql with the pgx stdlib driver"
metadata:
  languages: "go"
  versions: "5.12.0"
  revision: 4
  updated-on: "2026-11-01"
  source: community
  tags: "postgresql,postgres,go,pgx,database-sql,sql,testing"
---

# PostgreSQL in Go

This entry packages a practical PostgreSQL setup for small and medium Go
applications that use:

- `database/sql`
- `github.com/jackc/pgx/v5/stdlib`
- explicit SQL instead of an ORM
- transaction-aware repository methods

The focus is not every PostgreSQL feature. The focus is the set of patterns that
show up repeatedly in server-rendered Go applications.

## Base setup

Use the `pgx` stdlib driver when you want PostgreSQL-specific behavior while
keeping the standard `database/sql` surface.

```go
import (
    "database/sql"
    "time"

    _ "github.com/jackc/pgx/v5/stdlib"
)

func mustOpen(dsn string) *sql.DB {
    db, err := sql.Open("pgx", dsn)
    if err != nil {
        panic(err)
    }

    db.SetMaxOpenConns(10)
    db.SetMaxIdleConns(5)
    db.SetConnMaxLifetime(5 * time.Minute)

    if err := db.Ping(); err != nil {
        panic(err)
    }

    return db
}
```

## Recommended posture

- keep SQL explicit and near the repository method that owns it
- use transactions for multi-table writes
- model many-to-many joins directly instead of hiding them behind an ORM
- design indexes around actual query paths
- test repository behavior against a real Postgres instance when query semantics matter

## What ThoughtSpark demonstrates well

ThoughtSpark is a good example of:

- `database/sql` plus `pgx` for a Postgres-backed Go app
- schema constraints that mirror application rules
- transaction-based writes for parent-plus-child inserts
- SQL aggregation to hydrate slice fields
- time-window queries and supporting indexes
- integration tests with `testcontainers-go`

## Good first references

- `references/pgx-stdlib.md`
- `references/schema-and-indexes.md`
- `references/query-patterns.md`
- `references/testing-with-testcontainers.md`
- `references/version-notes.md`

## Latest release guidance

- `release-deltas/pgx-5.12.0.md`
