# Go 1.27.1 Delta

Go 1.27.0 was released August 19, 2026; 1.27.1 followed September 1.
This is a documentation target, not a claim that the local toolchain was upgraded.
The maintained 1.26 branch is at 1.26.8. Its intervening releases include security
fixes; read the official release history when remaining on that branch.

## Application-facing changes

- `database/sql.ConvertAssign` exposes scanning conversions to drivers.
- Drivers can implement `database/sql/driver.RowsColumnScanner` for direct destination scanning.
- HTTP/1 response bodies drain a bounded amount on close to improve connection reuse.
- `http.Server.MaxHeaderValueCount` controls the number of accepted header values.
- `httptest.NewTestServer` works with an in-memory network and `testing/synctest`.
- `crypto/tls.Config.Rand` is deprecated; several old TLS GODEBUG compatibility switches were removed.
- Go 1.27 requires macOS 13 or newer.

1.27.1 fixes the compiler, runtime, cgo, go fix, and several packages including
database/sql, encoding/json, and net/http. Existing handler/template/repository
patterns remain useful; test driver conversions and HTTP client behavior when upgrading.

## Sources

- https://go.dev/doc/go1.27
- https://go.dev/doc/devel/release
