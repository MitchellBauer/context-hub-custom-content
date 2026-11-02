# Schema and Migration Patterns

## Startup schema creation

`CREATE TABLE IF NOT EXISTS` and `CREATE INDEX IF NOT EXISTS` are a practical fit
for local-app SQLite startup.

```sql
CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## Lightweight migration checks

`PRAGMA table_info(table_name)` returns column metadata and is useful when you
need to detect whether a column already exists before running `ALTER TABLE`.

Common app pattern:

1. create baseline table if it does not exist
2. inspect columns with `PRAGMA table_info`
3. add missing columns with `ALTER TABLE`
4. continue startup normally

## Index guidance

Add indexes for actual access paths such as:

- book + slice lookup
- unique keys used for upserts
- time-ordered audit or ledger screens

Examples:

```sql
CREATE INDEX IF NOT EXISTS idx_questions_book_slice
ON questions(book_name, study_slice);

CREATE UNIQUE INDEX IF NOT EXISTS idx_missed_ledger_book_slice_qid
ON missed_ledger(book_name, study_slice, qid);
```

## Table design reminders

- Prefer explicit `NOT NULL` on required fields.
- Store timestamps in a consistent format.
- Use `TEXT`, `INTEGER`, and simple constraints unless you truly need more.
- Keep schema readable because in SQLite-heavy apps you often debug directly from raw SQL.
