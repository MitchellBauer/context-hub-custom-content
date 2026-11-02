# SQLite Driver Version Notes

Target: modernc.org/sqlite 1.60.1, released September 29, 2026.
Bundled engine: SQLite 3.53.4. Requires Go 1.26 or newer and the driver's
matching modernc.org/libc version, v1.77.1.

The blank import and `database/sql` pattern remain applicable. This pack's target
does not upgrade any application's go.mod. Check each app's declared version
and database tests before adopting it.

Read `release-deltas/modernc-sqlite-1.60.1.md` for upgrade-sensitive behavior.
The earlier 1.54.0 delta remains a historical reference.

Sources:

- https://pkg.go.dev/modernc.org/sqlite@v1.60.1
- https://proxy.golang.org/modernc.org/sqlite/@v/v1.60.1.mod
- https://gitlab.com/cznic/sqlite/-/raw/v1.60.1/CHANGELOG.md
