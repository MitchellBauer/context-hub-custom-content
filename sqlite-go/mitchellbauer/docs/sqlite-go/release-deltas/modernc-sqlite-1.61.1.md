# modernc.org/sqlite 1.61.1 Delta

Released October 31, 2026; updates 1.60.1 through 1.61.0 to 1.61.1.
Requires Go 1.26, embeds SQLite 3.54.1, and pins modernc.org/libc v1.79.0.

## Upgrade-sensitive behavior

- 1.61.1 repairs a prepared-statement performance regression introduced in 1.61.0.
- VFS databases created with `vfs.New` reject unsupported writes and journal
  deletion instead of panicking or aborting.
- Lock waits during queries, row completion, and commit respond to their
  associated contexts. Rollback behavior is unchanged in 1.61.1.
- From 1.61.0, shared-cache transaction startup waits rather than immediately
  returning a shared-cache lock error; use a context to bound that wait.
- `_time_format=string_no_monotonic` and connection authorizers are opt-in.
- Test prepared statements, cancellation, transactions, and custom VFS usage
  before adopting the driver in an application.

Earlier upgrade constraints remain in `release-deltas/modernc-sqlite-1.60.1.md`.

Sources:

- [Tagged changelog](https://gitlab.com/cznic/sqlite/-/raw/v1.61.1/CHANGELOG.md)
- [Tagged module requirements](https://gitlab.com/cznic/sqlite/-/raw/v1.61.1/go.mod)
