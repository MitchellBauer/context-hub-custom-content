# Go 1.26.5 Delta

## Release target

- Previous installed baseline: `go1.26.4`
- Installed locally on this machine: `go1.26.5`
- Official release date: July 7, 2026

## Security fixes

### `os`: `os.Root` escape through a trailing slash

Go 1.26.5 fixes CVE-2026-39822. On Unix systems, an `os.Root` operation could
follow a final symlink outside the root when the supplied path ended in `/`.

Review applications that:

- use `os.OpenRoot` or `os.Root`
- accept user-controlled relative paths
- depend on `os.Root` as a filesystem security boundary

Upgrading to Go 1.26.5 applies the fix. No API migration is required.

### `crypto/tls`: Encrypted Client Hello privacy leak

Go 1.26.5 fixes CVE-2026-42505. The ECH implementation could expose
pre-shared-key identities in the unencrypted outer ClientHello, allowing a
passive observer to infer the protected server hostname.

Review applications that explicitly use Encrypted Client Hello or TLS session
resumption. Upgrading to Go 1.26.5 applies the fix.

## Other fixes

The official release history also lists bug fixes in:

- the compiler
- the runtime
- the `go` command
- `net`
- `os`
- `syscall`

These are maintenance fixes rather than new standard-library APIs. Existing
Go 1.26 source should remain compatible.

## Incremental pack changes

This update changes only:

- package metadata from `1.26.1` to `1.26.5`
- this release delta
- `references/crypto-tls.md`
- the Go 1.26.5 security note in `references/os-io-fs.md`

The remaining standard-library reference files are unchanged.

## Verification

```text
go version go1.26.5 windows/amd64
```

## Official sources

- Go release history: https://go.dev/doc/devel/release#go1.26.5
- Go 1.26.5 announcement: https://groups.google.com/g/golang-announce/c/OrmQE_Yp5Sc
- ECH vulnerability: https://pkg.go.dev/vuln/GO-2026-5856
