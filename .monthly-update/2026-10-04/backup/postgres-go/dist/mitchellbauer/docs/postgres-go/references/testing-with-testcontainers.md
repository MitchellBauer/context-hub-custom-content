# Testing PostgreSQL Repositories with testcontainers-go

ThoughtSpark uses `testcontainers-go` to run repository integration tests
against a real PostgreSQL container.

## Why this is useful

Repository logic often depends on real PostgreSQL behavior:

- `RETURNING`
- `ON CONFLICT`
- `TIMESTAMPTZ`
- casts like `::time`
- index-backed query plans

Mocking `database/sql` does not validate those semantics.

## Practical pattern

ThoughtSpark starts one Postgres container in `TestMain`, applies `schema.sql`,
and truncates tables between tests instead of rebuilding the container every time.

That gives a good balance:

- realistic SQL behavior
- much faster test runs than one-container-per-test
- clean isolation between cases

## Suggested approach

1. Start a Postgres container in `TestMain`.
2. Open a shared `*sql.DB`.
3. Apply the real schema once.
4. `TRUNCATE ... RESTART IDENTITY CASCADE` before each test.
5. Keep pure logic tests separate from repository integration tests.
