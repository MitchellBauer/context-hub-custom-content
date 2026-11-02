# modernc.org/sqlite 1.60.1 Delta

Updated from 1.54.0 through September 29, 2026.

- Requires Go 1.26; match modernc.org/libc v1.77.1 from the driver's go.mod.
- Bundles SQLite 3.53.4, including the upstream multi-database journal recovery fix.
- 1.60.1 improves argument binding for statements with many parameters.
- 1.60.0 converts memory-mapped WAL shared-memory faults into an I/O error.
- VFS close rejects active databases: close database connections before the VFS.
- Some invalid exported lib constants were removed; audit direct lib imports.
- Invalid custom page-cache implementations now panic; callbacks have stricter lifetime requirements.
- Driver-specific virtual-table registration honors the supplied database's driver.
- Optional StrictPragmas rejects multi-statement `_pragma` values. It is off by default.
- Linux OFD locking and `_defensive` mode are opt-in, not automatic defaults.

Check migration, rollback/recovery, pooled connections, and bulk inserts on each
app. Preserve the chosen driver/libc pairing; do not independently bump libc.

Sources:

- https://gitlab.com/cznic/sqlite/-/raw/v1.60.1/CHANGELOG.md
- https://proxy.golang.org/modernc.org/sqlite/@v/v1.60.1.mod
