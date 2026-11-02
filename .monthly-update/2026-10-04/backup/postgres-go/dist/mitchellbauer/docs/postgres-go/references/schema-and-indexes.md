# Schema and Index Patterns

ThoughtSpark's schema shows several practical patterns for Postgres-backed Go apps.

## Put business rules in the schema

Use `CHECK`, `NOT NULL`, `UNIQUE`, and foreign keys so the database enforces the
same invariants the handlers validate.

Examples from ThoughtSpark:

- categories constrained by `CHECK (...)`
- `email_address` marked `UNIQUE`
- `number_of_prompts` constrained to a bounded range
- join-table rows cleaned up with `ON DELETE CASCADE`

## Model many-to-many relations directly

A simple junction table is often enough:

```sql
CREATE TABLE user_categories (
    user_id  INTEGER REFERENCES user_profiles(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    PRIMARY KEY (user_id, category)
);
```

This maps cleanly to repository methods that:

- insert the parent row
- insert each related row inside the same transaction
- delete and recreate child rows during full replacement updates

## Keep operational indexes close to actual query paths

ThoughtSpark adds indexes for:

- email lookups during signup and account flows
- notification time lookups for the scheduler
- prompt category and recency lookups
- per-user history ordered by send time

That is the right mindset: index for the queries you really run, not for abstract completeness.
