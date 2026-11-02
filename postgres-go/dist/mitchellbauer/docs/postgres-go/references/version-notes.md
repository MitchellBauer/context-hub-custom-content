# PostgreSQL and pgx Version Notes

Verified November 1, 2026:

- pgx 5.12.0, changelog dated October 30 and tagged October 31 UTC; minimum Go 1.25.
- PostgreSQL 16.15, 17.11, and 18.6, released August 13, 2026.
- PostgreSQL 18.5 was skipped. PostgreSQL 19 RC1 is a prerelease and is outside this pack.
- The next stable maintenance releases are scheduled for November 12, 2026.

pgx's stdlib import path remains `github.com/jackc/pgx/v5/stdlib`.
Go 1.27 enables direct PostgreSQL array/range scans through database/sql.
Read `release-deltas/pgx-5.12.0.md` for security fixes and compatibility checks,
and the earlier 5.11.0 delta for connection-string and date/time changes.

Same-major PostgreSQL updates do not require dump/restore, but the August
release notes include follow-up configuration and data cleanup steps. Review
logical-decoding plugin allowlists, affected pgcrypto data, and extension indexes
before declaring an upgrade complete. Read all intervening notes for older baselines.

Sources:

- https://github.com/jackc/pgx/blob/v5.12.0/CHANGELOG.md
- https://www.postgresql.org/support/versioning/
- https://www.postgresql.org/about/news/postgresql-19-rc-1-released-3409/
- https://www.postgresql.org/docs/16/release-16-15.html
- https://www.postgresql.org/docs/release/17.11/
- https://www.postgresql.org/docs/release/18.6/
