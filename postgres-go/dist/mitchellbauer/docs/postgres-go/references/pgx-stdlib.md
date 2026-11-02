# pgx Stdlib Driver with database/sql

This pack targets `github.com/jackc/pgx/v5` version `5.11.0`.

ThoughtSpark uses the `pgx` stdlib driver like this:

```go
import _ "github.com/jackc/pgx/v5/stdlib"
db, err := sql.Open("pgx", dsn)
```

This is a strong default when:

- the codebase already uses `database/sql`
- you want PostgreSQL instead of a generic SQL target
- you do not need a higher-level query builder

## Connection string shape

ThoughtSpark uses a URL-style DSN:

```text
postgres://user:password@host:port/dbname?sslmode=disable
```

That is easy to generate from environment-based configuration and easy to log
carefully after redacting secrets.

## Pool tuning

Small apps still benefit from explicit pool settings:

- `SetMaxOpenConns`
- `SetMaxIdleConns`
- `SetConnMaxLifetime`

Even conservative values are better than leaving pool behavior entirely implicit.

## Ping on startup

ThoughtSpark treats startup connectivity as mandatory and calls `db.Ping()`
before serving traffic. That is a good fit for applications where the database
is required for nearly every route.

## Supported versions

pgx v5 follows the Go and PostgreSQL projects' supported-version policies. At
this pack revision, pgx requires Go 1.25 or newer and supports PostgreSQL 14 or
newer. This pack focuses on PostgreSQL 16-18.

Keep the module on an explicit version:

```bash
go get github.com/jackc/pgx/v5@v5.12.0
```

## Sources

- https://pkg.go.dev/github.com/jackc/pgx/v5
- https://pkg.go.dev/github.com/jackc/pgx/v5/stdlib

## 5.11 upgrade notes

See `release-deltas/pgx-5.11.0.md`. Direct array/range scanning requires
Go 1.27; pgx 5.11 itself still supports Go 1.25. Check text timestamptz
locations and production connection URI parsing when upgrading.

## 5.12 upgrade notes

The current target is 5.12.0. See `release-deltas/pgx-5.12.0.md` for two
security fixes, the new `BatchResults.Tx` requirement for custom implementations,
and the changed Windows service-file search order.
