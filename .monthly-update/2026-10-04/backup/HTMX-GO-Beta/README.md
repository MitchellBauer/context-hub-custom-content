# HTMX Go Beta BYOD Pack

This is a separate pre-release documentation pack for HTMX 4.

It does not replace the stable `HTMX-GO` pack. Keep both sources registered so
agents can select stable HTMX 2.x guidance or experimental HTMX 4 guidance
explicitly.

## Version

- HTMX `4.0.0-beta6`
- Pre-release: APIs and behavior may still change

## Structure

```text
HTMX-GO-Beta/
  mitchellbauer/
    docs/
      htmx-go-beta/
        DOC.md
        references/
          attributes-and-events.md
          beta6-release-notes.md
          go-patterns.md
          headers.md
          migration-from-v2.md
```

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
chub get mitchellbauer/htmx-go-beta --lang go
chub get mitchellbauer/htmx-go-beta --lang go --full
chub get mitchellbauer/htmx-go-beta --lang go --file references\migration-from-v2.md
```

Always identify the beta version in implementation plans and code-review notes.
