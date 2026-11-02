# fyne-go BYOD Pack

This directory is a Bring Your Own Docs pack for the Fyne v2 GUI toolkit in Go, covering
cross-platform desktop app development with widgets, layouts, data binding, and canvas drawing.

## What this gives you

After you build this pack and add it to Context Hub, `chub` can search and fetch
local Fyne + Go guidance instead of relying on scattered notes.

## Folder structure

```text
fyne-go/
  mitchellbauer/
    docs/
      fyne-go/
        DOC.md
        references/
          widgets.md
          layouts-containers.md
          data-binding.md
          canvas-drawing.md
          version-notes.md
        release-deltas/
          fyne-2.8.0.md
```

## Step 1: Validate the content pack

```powershell
chub build '.\fyne-go\' --validate-only
```

## Step 2: Build the local registry output

```powershell
chub build '.\fyne-go\' -o '.\fyne-go\dist\'
```

## Step 3: Add it to Context Hub config

Add the built output as a local source in `~/.chub/config.yaml`:

```yaml
sources:
  - name: community
    url: https://cdn.aichub.org/v1
  - name: local-fyne-go
    path: C:/GitHubProjects/Context-Hub-Custom-Content/fyne-go/dist
```

## Step 4: Use it from Context Hub

```powershell
chub search "fyne"
chub get mitchellbauer/fyne-go
chub get mitchellbauer/fyne-go --full
```

## Notes

- The pack covers Fyne v2.8.1 with the `fyne.io/fyne/v2` import path.
- Fyne 2.8 requires Go 1.22 or newer.
- Requires a C compiler on the build machine (MSYS2 on Windows, Xcode on macOS, GCC on Linux).
- Examples emphasize practical desktop app patterns: windows, widgets, layouts, and goroutine safety.

## Latest release guidance

- `release-deltas/fyne-2.8.1.md`
