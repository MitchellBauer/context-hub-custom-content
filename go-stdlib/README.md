# go-stdlib BYOD Pack

This directory is a Bring Your Own Docs pack for the Go standard library.

## What this gives you

After you build this pack and add it to Context Hub, `chub` can search and fetch
local guidance for the Go standard library without loading the entire upstream
package corpus into context every time.

## Incremental update model

This pack is intentionally split into:

- one stable base entry: `go-stdlib`
- focused reference files by package family
- release delta files in `release-deltas/`

That means future updates can stay small.

### Recommended maintenance workflow

1. Keep the base entry focused on stable concepts and high-traffic packages.
2. Add one new file per Go release in `release-deltas/`.
3. Update only the package-family reference files touched by that release.
4. Bump `metadata.revision` if the package version stays the same and you refine content.
5. Bump `metadata.versions` when the pack is intentionally retargeted to a newer Go release.

### Example incremental cycle

- Base pack: `1.26.0`
- Add delta: `release-deltas/go1.26.1.md`
- Current delta: `release-deltas/go1.27.3.md`
- Only refresh `html-template.md`, `net-http.md`, or other touched references as needed

This gives you an "incremental backup" style workflow instead of reloading the whole standard library every time.

## Folder structure

```text
go-stdlib/
  mitchellbauer/
    docs/
      go-stdlib/
        DOC.md
        references/
          context-time-sync.md
          database-sql.md
          encoding-json.md
          crypto-tls.md
          html-template.md
          net-http.md
          os-io-fs.md
          testing.md
        release-deltas/
          go1.26.1.md
          go1.26.5.md
```

## Validate

```powershell
chub build '.\go-stdlib\' --validate-only
```

## Build

```powershell
chub build '.\go-stdlib\' -o '.\go-stdlib\dist\'
```

## Add to Context Hub

```yaml
sources:
  - name: local-go-stdlib
    path: C:/GitHubProjects/Context-Hub-Custom-Content/go-stdlib/dist
```

## Use it

```powershell
chub search "go stdlib"
chub get mitchellbauer/go-stdlib
chub get mitchellbauer/go-stdlib --file release-deltas\go1.27.3.md
```

## Latest release guidance

- `release-deltas/go1.27.3.md`
