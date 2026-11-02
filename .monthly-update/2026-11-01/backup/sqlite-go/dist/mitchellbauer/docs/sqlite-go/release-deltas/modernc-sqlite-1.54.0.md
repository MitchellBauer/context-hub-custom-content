# modernc.org/sqlite 1.54.0 Delta

## Pack update

- Previous version: `1.39.1`
- New version: `1.54.0`
- Published: July 15, 2026
- Embedded SQLite: `3.53.3`

## Important additions since 1.39.1

- pre-update and rollback hooks
- Go virtual-table module support
- backup page-count reporting
- pluggable page-cache interfaces
- additional time conversion options
- broader platform support synchronized with SQLite 3.53.3

## Upgrade checklist

1. Upgrade in the application module with
   `go get modernc.org/sqlite@v1.54.0`.
2. Allow Go modules to select the matching `modernc.org/libc` dependency.
3. Run repository, migration, transaction, WAL, and backup tests.
4. Test every deployed GOOS/GOARCH target.
5. Review scan behavior if the application uses driver time-conversion options.

`Quiz-Runner` remains on 1.39.1 until its own dependency is deliberately
upgraded. Do not assume this documentation update changed that application.

## Official source

- https://pkg.go.dev/modernc.org/sqlite
