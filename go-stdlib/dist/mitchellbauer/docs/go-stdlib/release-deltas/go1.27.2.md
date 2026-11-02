# Go 1.27.2 Delta

Released October 8, 2026. This is an intervening release; the current pack
targets Go 1.27.3, which includes these fixes.

Security fixes affect the Go command, crypto/tls, html/template, net/http,
net/textproto, and os. Bug fixes also affect the compiler, linker, runtime,
development tools, compression, cryptography, JSON, HTTP, and filesystem code.

When upgrading from 1.27.1, rerun handler, template, TLS, JSON, and filesystem
tests. Rebuild deployed binaries to include standard-library fixes.

Source: [Go release history](https://go.dev/doc/devel/release#go1.27.2).
