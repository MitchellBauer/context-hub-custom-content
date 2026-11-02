# sqlite-go BYOD Pack

This directory is a Bring Your Own Docs pack for SQLite in Go, with an emphasis on
`modernc.org/sqlite` and the practical query patterns used in server-rendered Go apps.

## What this gives you

After you build this pack and add it to Context Hub, `chub` can search and fetch
local SQLite + Go guidance instead of relying on scattered notes.

## Folder structure

```text
sqlite-go/
  mitchellbauer/
    docs/
      sqlite-go/
        DOC.md
        references/
          modernc-driver.md
          schema-and-migrations.md
          queries-and-transactions.md
          sqlite-patterns.md
          version-notes.md
        release-deltas/
          modernc-sqlite-1.54.0.md
```

## Step 1: Validate the content pack

```powershell
chub build '.\sqlite-go\' --validate-only
```

## Step 2: Build the local registry output

```powershell
chub build '.\sqlite-go\' -o '.\sqlite-go\dist\'
```

## Step 3: Add it to Context Hub config

Add the built output as a local source in `~/.chub/config.yaml`:

```yaml
sources:
  - name: community
    url: https://cdn.aichub.org/v1
  - name: local-sqlite-go
    path: C:/GitHubProjects/Context-Hub-Custom-Content/sqlite-go/dist
```

## Step 4: Use it from Context Hub

```powershell
chub search "sqlite"
chub get mitchellbauer/sqlite-go
chub get mitchellbauer/sqlite-go --full
```

## Notes

- The pack is centered on official SQLite documentation and `modernc.org/sqlite` usage from Go.
- The driver reference targets `modernc.org/sqlite` v1.60.1 (Go 1.26 or newer).
- The examples emphasize stdlib `database/sql` and practical repository patterns.

## Latest release guidance

- `release-deltas/modernc-sqlite-1.60.1.md`
