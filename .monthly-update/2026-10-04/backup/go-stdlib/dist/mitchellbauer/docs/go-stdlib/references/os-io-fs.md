# os, io, fs, and filepath

## Core packages

- `os`
- `io`
- `io/fs`
- `path/filepath`
- `embed`

## Typical responsibilities

- reading and writing files
- walking directories
- path handling
- embedding templates or static assets
- environment variable access

## Practical rules

- use `filepath` for OS-native paths
- use `io.Copy` for stream transfer patterns
- use `os.ReadFile` and `os.WriteFile` for simple file operations
- treat environment-driven config as input validation work, not as trusted data

## `os.Root` security note for Go 1.26.5

Go 1.26.5 fixes CVE-2026-39822. On Unix systems before the fix, an
`os.Root` operation could follow a final symlink outside the root when the path
ended in a slash.

- Run Go 1.26.5 or newer when using `os.Root` as a filesystem boundary.
- Continue validating application-level paths even when `os.Root` is used.
- Treat paths ending in `/` as meaningful input rather than normalizing them
  away without considering security behavior.

See `release-deltas/go1.26.5.md` for the release-specific summary.
