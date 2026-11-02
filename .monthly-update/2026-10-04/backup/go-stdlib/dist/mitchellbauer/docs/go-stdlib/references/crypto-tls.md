# crypto/tls

## Role

`crypto/tls` implements TLS clients and servers and is used by `net/http` for
HTTPS connections.

## Practical guidance

- Prefer current supported Go point releases because TLS security fixes ship
  with the toolchain and standard library.
- Start from `tls.Config` defaults unless compatibility requirements justify
  an explicit override.
- Clone shared configurations before request- or host-specific changes.
- Avoid logging secrets, session tickets, pre-shared-key identities, or raw
  handshake material.

## Go 1.26.5 security note

Go 1.26.5 fixes CVE-2026-42505. Before the fix, Encrypted Client Hello
handshakes could expose pre-shared-key identities in the unencrypted outer
ClientHello, allowing a passive observer to infer the server hostname.

Applications using ECH should run Go 1.26.5 or newer. Ordinary TLS users should
also stay current because `crypto/tls` fixes are delivered through Go point
releases.

See `release-deltas/go1.26.5.md` for the release-specific summary.
