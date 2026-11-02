# postgres-go BYOD Pack

This directory is a Bring Your Own Docs pack for PostgreSQL in Go, centered on
`database/sql` with the `pgx` stdlib driver and the schema/query patterns used in
small server-rendered applications.

## What this gives you

After you build this pack and add it to Context Hub, `chub` can search and fetch
local PostgreSQL + Go guidance instead of relying on scattered notes from app repos.

## Folder structure

```text
postgres-go/
  mitchellbauer/
    docs/
      postgres-go/
        DOC.md
        references/
          pgx-stdlib.md
          schema-and-indexes.md
          query-patterns.md
          testing-with-testcontainers.md
          version-notes.md
```

## Step 1: Validate the content pack

```powershell
chub build '.\postgres-go\' --validate-only
```

## Step 2: Build the local registry output

```powershell
chub build '.\postgres-go\' -o '.\postgres-go\dist\'
```

## Step 3: Add it to Context Hub config

Add the built output as a local source in `~/.chub/config.yaml`:

```yaml
sources:
  - name: community
    url: https://cdn.aichub.org/v1
  - name: local-postgres-go
    path: C:/GitHubProjects/Context-Hub-Custom-Content/postgres-go/dist
```

## Step 4: Use it from Context Hub

```powershell
chub search "postgres go"
chub get mitchellbauer/postgres-go
chub get mitchellbauer/postgres-go --full
```

## Notes

- The pack is based on ThoughtSpark's PostgreSQL usage patterns.
- It targets pgx v5.12.0 and the maintained PostgreSQL 16-18 release lines.
- It focuses on `database/sql`, `pgx/v5/stdlib`, practical schema design, and integration testing.

## Latest release guidance

- `release-deltas/pgx-5.12.0.md`
