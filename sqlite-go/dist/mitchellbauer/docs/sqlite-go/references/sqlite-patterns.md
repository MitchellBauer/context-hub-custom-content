# SQLite Patterns for Go Apps

## Repository shape

A clean pattern is:

- one repository struct that owns `*sql.DB`
- methods grouped by domain action
- SQL kept close to the behavior it powers
- scan helpers for repeated row shapes

## Good use cases

SQLite is a strong fit for:

- local-first tools
- single-service internal apps
- admin panels
- quiz, notes, and workflow apps
- embedded metadata stores

## HTTP app integration

In server-rendered Go apps, SQLite often pairs well with:

- `net/http`
- `html/template`
- local file deployment
- startup schema verification
- simple backup/restore workflows

## When to rethink SQLite

You may outgrow it when:

- you need many concurrent writers across multiple app instances
- you need network-native database operations
- dataset size or query shape pushes past what your current approach can handle comfortably

That does not mean SQLite is wrong. It means you should watch real write patterns,
locking behavior, and slow queries before making assumptions.
