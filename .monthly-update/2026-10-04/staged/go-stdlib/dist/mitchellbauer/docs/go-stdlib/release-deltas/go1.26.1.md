# Go 1.26.1 Delta

## Release target

- Installed locally on this machine: `go1.26.1`
- Official release date: March 5, 2026
- `pkg.go.dev` package publication updates may appear on March 6, 2026 for stdlib pages

## Why this file exists

This file is the incremental layer for the `go-stdlib` pack.

When a future Go point release lands, add a new delta file instead of rewriting the whole base entry.

## Officially noted changes in Go 1.26.1

The release notes call out security fixes in:

- `crypto/x509`
- `html/template`
- `net/url`
- `os`

The release also includes bug fixes to the compiler, linker, runtime, and the `go` command.

## What to review in app code

For most application code, the most relevant packages to revisit after `1.26.1` are:

- `html/template`
- `net/url`
- `os`

If your app handles certificates or custom trust flows, also review:

- `crypto/x509`

## Practical update workflow

1. Confirm your installed version with `go version`.
2. Read the release delta file first.
3. Re-open only the touched package-family references.
4. Update your BYOD pack only where the point release actually changed behavior or guidance.

## Local verification result

This machine currently reports:

```text
go version go1.26.1 windows/amd64
```

## Future incremental pattern

When `go1.26.2` or `go1.27.0` arrives:

- add a new release delta file
- update only affected reference files
- leave unchanged package-family docs alone
