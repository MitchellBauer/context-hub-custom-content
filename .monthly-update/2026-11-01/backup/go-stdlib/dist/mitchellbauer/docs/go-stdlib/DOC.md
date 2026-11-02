---
name: go-stdlib
description: "Go standard library guide for server-side Go applications"
metadata:
  languages: "go"
  versions: "1.27.1"
  revision: 3
  updated-on: "2026-10-04"
  source: community
  tags: "go,stdlib,net-http,html-template,database-sql,encoding-json"
---

# Go Standard Library

This entry is a practical guide to the Go standard library for application work,
not an attempt to copy every upstream package page into one document.

The goal is to keep a compact base entry and push package-family detail into
reference files so future updates can be incremental.

## What "stdlib" means

The Go standard library is the set of packages that ship with Go itself.

High-value examples for application work:

- `net/http`
- `html/template`
- `database/sql`
- `encoding/json`
- `os`
- `io`
- `fs`
- `context`
- `time`
- `sync`
- `testing`

## Why this pack is organized by package family

If you try to treat the entire standard library as one monolithic doc, updates
become expensive and noisy.

Instead, this pack uses:

- a stable overview file
- focused references for the package families most common in application code
- release delta files for point-release changes

That keeps token usage lower and makes maintenance easier.

## Core package families for web apps

### HTTP and request handling

- `net/http`
- `net/url`
- `mime/multipart`
- `http/cookiejar` when needed

### Rendering and parsing

- `html/template`
- `text/template`
- `encoding/json`
- `encoding/csv`

### Data and storage

- `database/sql`
- `database/sql/driver`

### Filesystem and process environment

- `os`
- `io`
- `io/fs`
- `path/filepath`
- `embed`

### Concurrency and lifecycle

- `context`
- `time`
- `sync`
- `errors`
- `log` or `log/slog`

### Tests and diagnostics

- `testing`
- `httptest`
- `testing/fstest`
- `runtime`
- `pprof`

## Practical rules

- Prefer stdlib first when it already covers the problem well.
- Reach for external dependencies only when they clearly improve correctness or speed of delivery.
- Keep handlers, templates, DB access, and tests explicit.
- Use small wrappers around stdlib packages instead of building large abstraction layers too early.

## Release-aware workflow

For Go point releases, do not rebuild your mental model of the whole standard library.

Instead:

1. read the new release delta file in `release-deltas/`
2. inspect only the package-family references touched by that delta
3. update your app code only where those package changes matter

This mirrors an incremental-backup workflow: small diffs layered on top of a stable base.

## Reference files

- `references/net-http.md`
- `references/html-template.md`
- `references/database-sql.md`
- `references/encoding-json.md`
- `references/os-io-fs.md`
- `references/crypto-tls.md`
- `references/context-time-sync.md`
- `references/testing.md`
- `release-deltas/go1.26.1.md`
- `release-deltas/go1.26.5.md`

## Latest release guidance

- `release-deltas/go1.27.1.md`
