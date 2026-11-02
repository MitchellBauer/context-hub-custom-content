# Queries and Transactions

## Transactions

Use transactions whenever one logical operation writes multiple rows or combines
read/write steps that should succeed or fail together.

Typical pattern:

```go
tx, err := db.BeginTx(ctx, nil)
if err != nil {
    return err
}

defer tx.Rollback()

// writes here

return tx.Commit()
```

## Prepared statements

For repeated inserts inside one transaction, `PrepareContext` is a practical choice.
It keeps the loop simple and reduces repetition.

## Upserts

SQLite supports `ON CONFLICT DO UPDATE`, which is often better than:

1. `SELECT` to check existence
2. conditional `INSERT` or `UPDATE`

Use it for settings, deduplicated ledger rows, and counters anchored on unique keys.

## Random selection

`ORDER BY RANDOM()` is convenient and often fine for smaller tables.

For larger tables, treat it as a possible scaling hot spot. If the dataset grows,
consider alternate sampling strategies rather than assuming `RANDOM()` will stay cheap.

## Scan discipline

- keep `SELECT` column order explicit
- keep `Scan(...)` order identical to the query
- isolate scanning into small helper functions when a row shape is reused
