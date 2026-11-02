# HTMX Go BYOD Pack

This directory is a Bring Your Own Docs pack for building HTMX applications in Go.

## What this gives you

After you build this pack and add it to Context Hub, `chub` can search and fetch
local HTMX + Go guidance instead of relying on ad hoc prompts.

## Folder structure

```text
HTMX-GO/
  mitchellbauer/
    docs/
      htmx/
        DOC.md
        references/
          attributes.md
          headers.md
          go-patterns.md
          thoughtspark-admin-crud.md
          ui-patterns.md
          version-notes.md
        release-deltas/
          htmx-2.0.9.md
```

This follows the Context Hub BYOD structure from the local docs:

- `author/docs/<entry>/DOC.md`
- optional `references/` files for deeper detail

## Step 1: Validate the content pack

```powershell
chub build '.\HTMX-GO\' --validate-only
```

## Step 2: Build the local registry output

```powershell
chub build '.\HTMX-GO\' -o '.\HTMX-GO\dist\'
```

## Step 3: Add it to Context Hub config

Add the built output as a local source in `~/.chub/config.yaml`:

```yaml
sources:
  - name: community
    url: https://cdn.aichub.org/v1
  - name: local-context
    path: C:/GitHubProjects/Context-Hub-Custom-Content/HTMX-GO/dist
```

## Step 4: Use it from Context Hub

```powershell
chub search "htmx"
chub get mitchellbauer/htmx
chub get mitchellbauer/htmx --full
```

## Notes

- The pack is focused on official HTMX documentation, with Go examples added for server-rendered applications.
- The stable pack is pinned to HTMX 2.0.11.
- The structure and metadata follow the local `Context-Hub-Docs` authoring guidance in this repository.

## Latest release guidance

- `release-deltas/htmx-2.0.11.md`
