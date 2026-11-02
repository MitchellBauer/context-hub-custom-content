# SQLite Driver Version Notes

Target: modernc.org/sqlite 1.61.1, released October 31, 2026.
Bundled engine: SQLite 3.54.1. Requires Go 1.26 or newer and the driver's
matching modernc.org/libc version, v1.79.0.

The blank import and `database/sql` pattern remain applicable. This pack's target
does not upgrade any application's go.mod. Check each app's declared version
and database tests before adopting it.

Read `release-deltas/modernc-sqlite-1.61.1.md` for upgrade-sensitive behavior.
The earlier 1.60.1 and 1.54.0 deltas remain historical references.

Sources:

- https://pkg.go.dev/modernc.org/sqlite@v1.61.1
- https://gitlab.com/cznic/sqlite/-/raw/v1.61.1/go.mod
- https://gitlab.com/cznic/sqlite/-/raw/v1.61.1/CHANGELOG.md
