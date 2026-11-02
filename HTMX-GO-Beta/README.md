# HTMX 4 for Go BYOD Pack

Targets stable HTMX 4.0.1 (4.0.0 released August 28, 2026; 4.0.1 November 1, 2026).
Use `mitchellbauer/htmx-go` for HTMX 4 and `mitchellbauer/htmx` for HTMX 2.
The `mitchellbauer/htmx-go-beta` lookup remains compatible and returns 4.0.1 guidance.
The historical folder and source names are retained so installed configurations work.

## Validate and build

```powershell
chub build '.\HTMX-GO-Beta\' --validate-only
chub build '.\HTMX-GO-Beta\' -o '.\HTMX-GO-Beta\dist\'
```

## Context Hub source

```yaml
sources:
  - name: local-htmx-go-beta
    path: C:/GitHubProjects/Context-Hub-Custom-Content/HTMX-GO-Beta/dist
```

## Use it

```powershell
chub get mitchellbauer/htmx-go --lang go
chub get mitchellbauer/htmx-go --lang go --full
chub get mitchellbauer/htmx-go --lang go --file references/migration-from-v2.md
```

Pin the exact JavaScript version and test the migration before upgrading an app.
