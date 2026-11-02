# Query Patterns from ThoughtSpark

## Parent plus child writes in one transaction

ThoughtSpark creates a user row, captures the generated id with `RETURNING`, then
inserts the user's categories within the same transaction.

```go
tx, err := db.Begin()
if err != nil {
    return err
}
defer tx.Rollback()

var id int
err = tx.QueryRow(`
    INSERT INTO user_profiles (email_address, first_name)
    VALUES ($1, $2)
    RETURNING id
`, email, firstName).Scan(&id)
```

This is a good fit when related rows should never exist without the parent.

## Hydrating slice fields with aggregation

ThoughtSpark uses `string_agg` to read categories alongside the main user row.

```sql
SELECT u.id, string_agg(c.category, ',')
FROM user_profiles u
LEFT JOIN user_categories c ON u.id = c.user_id
GROUP BY u.id
```

In Go, split the aggregated string into a slice after scanning. This keeps the
number of round trips low for list and detail views.

## Time-window queries

The scheduler uses a time-window filter and handles midnight wraparound by
switching between:

- `BETWEEN $1::time AND $2::time`
- `>= $1::time OR <= $2::time`

That pattern is useful for reminder systems, digest delivery, and polling jobs.

## Upserts for history or dedupe tables

ThoughtSpark records prompt delivery history with:

```sql
INSERT INTO user_prompt_history (user_id, prompt_id, sent_at)
VALUES ($1, $2, NOW())
ON CONFLICT (user_id, prompt_id) DO UPDATE SET sent_at = NOW()
```

This is a strong pattern when the row represents the latest known state for a
natural key rather than an append-only audit log.
