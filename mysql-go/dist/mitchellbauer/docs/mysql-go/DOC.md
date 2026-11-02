---
name: mysql-go
description: "go-sql-driver/mysql guide for Go: DSN config, TLS, UTC sessions, read-only connections"
metadata:
  languages: "go"
  versions: "1.10.1"
  revision: 1
  updated-on: "2026-11-01"
  source: community
  tags: "mysql,mariadb,go,database-sql,go-sql-driver,tls"
---

# MySQL / MariaDB for Go

`github.com/go-sql-driver/mysql` is the `database/sql` driver for MySQL and
MariaDB. Pure Go, no CGO. v1.10.x supports Go 1.24 and newer and is tested
against MySQL and MariaDB (11.8 and 12.3 added in 1.10.1).

```go
import (
    "database/sql"

    "github.com/go-sql-driver/mysql"
)
```

The import registers the driver as `"mysql"`. Use `sql.Open("mysql", dsn)`.
`sql.Open` does not connect; call `db.PingContext` to check.

## Build the DSN from a Config

Prefer `mysql.NewConfig()` and `FormatDSN()` over string concatenation. Special
characters in the password then need no escaping.

```go
mc := mysql.NewConfig() // use NewConfig, not &mysql.Config{}: it sets safe defaults
mc.Net = "tcp"
mc.Addr = "db.example.com:3306"
mc.User = "app"
mc.Passwd = password
mc.DBName = "appdb"
mc.ParseTime = true     // DATETIME/TIMESTAMP -> time.Time
mc.Loc = time.UTC       // location used when parsing times
mc.Params = map[string]string{"time_zone": "'+00:00'"} // session variable

db, err := sql.Open("mysql", mc.FormatDSN())
if err != nil { /* bad DSN */ }
db.SetMaxOpenConns(10)
db.SetConnMaxLifetime(5 * time.Minute) // stay under the server's wait_timeout
```

v1.10.1 fixed `FormatDSN()` dropping `Addr` when `Net` was empty. Set `Net`
explicitly anyway.

## Times and UTC

Store and read UTC; convert for display. Three settings work together:

- `ParseTime = true`: without it, DATETIME comes back as `[]byte`.
- `Loc = time.UTC`: how the driver interprets and sends times.
- `Params["time_zone"] = "'+00:00'"`: makes the **server session** UTC, so
  `NOW()` and `TIMESTAMP` conversions agree. The value needs the inner single
  quotes.

## TLS

`mc.TLSConfig` takes `"true"`, `"false"`, `"skip-verify"`, `"preferred"`, or the
name of a config you registered:

```go
if err := mysql.RegisterTLSConfig("pinned-ca", &tls.Config{RootCAs: pool}); err != nil { ... }
mc.TLSConfig = "pinned-ca"
```

- Registered names are **global to the process**. Two connections using
  different CA files must register different names (for example include the
  user in the name), or the second registration overwrites the first.
- Use a pinned CA (`RootCAs`) for a private CA instead of `skip-verify`.

## Read-only connections

To make a pool refuse writes, set the session variable in the DSN:

```go
mc.Params["transaction_read_only"] = "1"
```

The server then rejects writes on those sessions. Treat this as a second line
of defense. The first is a database account with `SELECT` only. Both together
mean a bug in the app cannot change the data. A session can still turn the
variable off, so grants matter more than the flag.

## Multiple statements

`mc.MultiStatements = true` lets one `Exec` run a whole migration script. Turn
it on **only** for the connection that runs trusted migrations: it also turns
SQL injection into stacked statements. Keep a separate pool without it for
normal queries.

## Queries

```go
var name string
err := db.QueryRowContext(ctx, `SELECT name FROM printer WHERE printer_id = ?`, id).Scan(&name)
if errors.Is(err, sql.ErrNoRows) { /* not found */ }
```

- Always use `?` placeholders. `interpolateParams=true` (the `InterpolateParams`
  field) sends one round trip instead of prepare/execute but then the driver
  builds the SQL text; use it only if you need it. v1.10.0 stopped treating
  `?` inside string literals and comments as placeholders; v1.10.1 fixed a
  typed-nil `json.RawMessage` being interpolated as an empty string (now `NULL`).
- Nullable columns: scan into `sql.NullString`, `sql.NullInt64`, or
  `mysql.NullTime` (use `sql.NullTime` on current Go).
- `COALESCE(col, '')` in SQL is often simpler than null types for display data.
- Close `*sql.Rows`, and check `rows.Err()` after the loop.

## Errors

Match server errors by number:

```go
var me *mysql.MySQLError
if errors.As(err, &me) && me.Number == 1062 { /* duplicate key */ }
```

Common numbers: 1062 duplicate entry, 1045 access denied, 1142 command denied
to user (a read-only grant doing what it should), 1213 deadlock (retry the
transaction).

## Connection pool notes

- `ErrBadConn`/"invalid connection" after idle periods means a firewall or the
  server closed the connection. Lower `SetConnMaxLifetime`.
- `SetMaxOpenConns` bounds load on a shared server. Pick a small number for a
  read-only lookup pool.
- `tx.Commit()` and `tx.Rollback()` return the real cached error since 1.9.3.

## Version notes

- 1.10.1 (2026-09-02): `FormatDSN` keeps `Addr` with empty `Net`; typed-nil
  `json.RawMessage` interpolates as `NULL`.
- 1.10.0 (2026-04-28): `max_allowed_packet` lookup fix; placeholder detection
  ignores `?` in strings and comments; edwards25519 1.2.0.
- 1.9.x: zlib compression, `Charset()` option, `VECTOR` type, custom dial
  function, real errors from Commit/Rollback.
