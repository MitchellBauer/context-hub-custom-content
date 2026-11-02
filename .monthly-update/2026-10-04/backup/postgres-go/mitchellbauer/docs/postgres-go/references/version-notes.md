# PostgreSQL and pgx Version Notes

## Pack targets

- pgx: `v5.10.0`, released June 3, 2026
- PostgreSQL 16: current minor `16.14`
- PostgreSQL 17: current minor `17.10`
- PostgreSQL 18: current minor `18.4`

PostgreSQL minor releases are cumulative bug-fix and security releases. Stay on
the newest minor release for the major version you operate.

PostgreSQL 19 is still a beta release and is outside this stable pack.

## Compatibility posture

- The `github.com/jackc/pgx/v5/stdlib` import path remains correct for
  `database/sql`.
- pgx v5.10.0 supports the Go project's two current major release lines,
  beginning with Go 1.25 at this revision.
- PostgreSQL minor upgrades normally do not require dump and restore, but always
  read the intervening release notes for version-specific migration warnings.
- The May 2026 PostgreSQL minors include security fixes, so deployments should
  not remain on earlier minors merely because the major version is unchanged.

## Official sources

- https://pkg.go.dev/github.com/jackc/pgx/v5
- https://www.postgresql.org/docs/release/
- https://www.postgresql.org/support/versioning/
