# Go 1.27.3 Delta

Released October 19, 2026. Updates this pack from 1.27.1 to 1.27.3.

This release fixes security issues in crypto/x509. Review certificate-validation
tests when upgrading. It also includes the intervening 1.27.2 fixes described
in `release-deltas/go1.27.2.md`.

The stable application patterns in this pack remain applicable. Update the
toolchain and rebuild applications separately; changing these docs does not
patch existing executables.

Source: [Go release history](https://go.dev/doc/devel/release#go1.27.3).
