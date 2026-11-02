---
name: sqlite-go
description: "SQLite + modernc.org/sqlite guide for Go web applications"
metadata:
  languages: "go"
  versions: "1.54.0"
  revision: 2
  updated-on: "2026-07-28"
  source: community
  tags: "sqlite,go,database,sql,modernc,database-sql"
---

# SQLite for Go

This entry packages practical SQLite guidance for Go applications using
`database/sql` and `modernc.org/sqlite`.

It is written for the style of app that:

- uses `sql.Open("sqlite", dbPath)`
- keeps SQL explicit in repository methods
- creates or verifies schema on startup
- uses transactions for multi-row writes
- serves a server-rendered web UI instead of a JSON-heavy frontend

## Base setup

Register the driver with a blank import and open the database through
`database/sql`.

```go
import (
    "database/sql"
    _ "modernc.org/sqlite"
)

func openDB(dbPath string) (*sql.DB, error) {
    db, err := sql.Open("sqlite", dbPath)
    if err != nil {
        return nil, err
    }
    return db, nil
}
```

## Why this driver is useful

`modernc.org/sqlite` is a pure Go SQLite driver. That makes it attractive when you
want simpler builds and do not want CGO as an app requirement.

In most apps, you still think in normal SQLite terms first:

- schema design
- indexes
- transactions
- `PRAGMA` usage
- `ON CONFLICT` behavior
- query shape and scan discipline

The Go driver mostly affects initialization, DSN/connection details, and some
operational tradeoffs.

## Practical patterns

### Initialize schema at startup

```go
func initSchema(ctx context.Context, db *sql.DB) error {
    schema := `
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name TEXT NOT NULL,
    study_slice TEXT NOT NULL,
    question_prompt TEXT NOT NULL,
    correct_letter TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_questions_book_slice
ON questions(book_name, study_slice);
`
    _, err := db.ExecContext(ctx, schema)
    return err
}
```

### Use `PRAGMA table_info` for lightweight column checks

```go
func hasColumn(ctx context.Context, db *sql.DB, tableName, columnName string) (bool, error) {
    rows, err := db.QueryContext(ctx, "PRAGMA table_info("+tableName+")")
    if err != nil {
        return false, err
    }
    defer rows.Close()

    for rows.Next() {
        var cid int
        var name string
        var columnType string
        var notNull int
        var defaultVal sql.NullString
        var pk int
        if err := rows.Scan(&cid, &name, &columnType, &notNull, &defaultVal, &pk); err != nil {
            return false, err
        }
        if strings.EqualFold(name, columnName) {
            return true, nil
        }
    }

    return false, rows.Err()
}
```

This is a practical migration tactic when your app owns a local SQLite file and
you want simple startup-time schema evolution without a separate migration tool.

### Wrap multi-row writes in transactions

```go
func insertQuestions(ctx context.Context, db *sql.DB, questions []Question) error {
    tx, err := db.BeginTx(ctx, nil)
    if err != nil {
        return err
    }

    stmt, err := tx.PrepareContext(ctx, `
INSERT INTO questions (book_name, study_slice, question_prompt, correct_letter)
VALUES (?, ?, ?, ?)`)
    if err != nil {
        _ = tx.Rollback()
        return err
    }
    defer stmt.Close()

    for _, q := range questions {
        if _, err := stmt.ExecContext(ctx, q.BookName, q.StudySlice, q.QuestionPrompt, q.CorrectLetter); err != nil {
            _ = tx.Rollback()
            return err
        }
    }

    return tx.Commit()
}
```

### Use upserts for app settings or counters

SQLite supports `INSERT ... ON CONFLICT DO UPDATE`.

```sql
INSERT INTO app_settings (key, value, updated_at)
VALUES (?, ?, CURRENT_TIMESTAMP)
ON CONFLICT(key) DO UPDATE SET
    value = excluded.value,
    updated_at = CURRENT_TIMESTAMP;
```

This is a strong fit for user preferences, cached prompts, sync markers, and
other key-value style records.

## Query advice

- Use explicit column lists in `SELECT` statements.
- Keep scan order stable and close to the struct you fill.
- Add indexes for real lookup paths, not hypothetical ones.
- Be careful with `ORDER BY RANDOM()` on large tables. It is convenient, but it
  gets more expensive as the table grows.

## Common SQLite features worth knowing

- `INTEGER PRIMARY KEY` aliases the rowid in SQLite.
- `AUTOINCREMENT` is rarely needed unless you specifically need stricter rowid reuse behavior.
- `PRAGMA table_info(...)` is useful for startup checks.
- `PRAGMA foreign_keys = ON` matters if you rely on foreign key enforcement.
- `CURRENT_TIMESTAMP` is useful for simple created/updated fields.
- `UNIQUE` plus `ON CONFLICT` is often simpler than read-then-write logic.

## Good fit for Go web apps

SQLite works especially well when:

- a single app process owns the database file most of the time
- deployment simplicity matters more than distributed write scaling
- you want backups to be simple file operations
- your app is query-light to medium and mostly request/response driven

## References

- `references/modernc-driver.md`
- `references/schema-and-migrations.md`
- `references/queries-and-transactions.md`
- `references/sqlite-patterns.md`
- `references/version-notes.md`
- `release-deltas/modernc-sqlite-1.54.0.md`
