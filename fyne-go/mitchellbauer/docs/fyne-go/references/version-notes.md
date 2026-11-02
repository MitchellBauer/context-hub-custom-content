# Fyne Version Notes

## Current version: v2.8.2 (announced October 12, 2026)

See `release-deltas/fyne-2.8.2.md` for fixes since 2.8.1.
The 2.8 migration notes below still apply.

Import path: `fyne.io/fyne/v2`

Minimum Go version: **1.22**

---

## v2.8 - Migration and Platform Changes

- Wayland support is enabled by default and selected automatically at runtime.
- GUI work launched from background goroutines should use `fyne.Do` or
  `fyne.DoAndWait`; applications that have not migrated receive runtime
  warnings.
- Popups no longer include padding by default.
- `canvas.Polygon` was renamed to `canvas.RegularPolygon`.
- A circle now remains circular and is centered within its available space.
- Windows 7, Windows 8, and macOS 10.14 or earlier are no longer supported.

The release also adds scheduled notifications, accessibility testing, secondary
monitor support, richer Markdown, additional canvas objects, and expanded
window APIs.

See `release-deltas/fyne-2.8.0.md` before upgrading an existing application.

---

## v2.6 — Thread Safety Changes (Important)

Before v2.6, updating a widget from a goroutine required calling `canvas.Refresh`
directly and hoping it was safe. This was fragile.

**v2.6 added `fyne.Do` and `fyne.DoAndWait`** as the official way to marshal
work onto the main goroutine:

```go
// Non-blocking — schedules fn on main goroutine
fyne.Do(func() {
    label.SetText("updated")
})

// Blocking — waits for fn to complete before returning
fyne.DoAndWait(func() {
    label.SetText("updated")
    result = label.Text
})
```

Use `fyne.Do` for fire-and-forget GUI updates from background goroutines.
Use `fyne.DoAndWait` when you need to read back a GUI value.

Data binding (`binding.*`) is always thread-safe regardless of version — no
`fyne.Do` wrapper needed when calling `binding.Set`.

---

## v2.5 — Notable Additions

- `container.NewInnerWindow` — floating in-app panels (MDI style)
- `widget.GridWrap` — uniform-size item grid with wrapping rows
- Improved theme customization API

---

## v2.4 — Notable Additions

- `widget.RichText` — mixed-style text with segments (bold, italic, code, links)
- `container.NewDocTabs` — closeable document tabs
- `widget.FileIcon` — file-type icons

---

## v2.3 — Notable Additions

- `widget.Table` gained `SetColumnWidth` and `SetRowHeight`
- `canvas.NewColorRGBAAnimation` for color-transition animations

---

## v2.2 — Notable Additions

- `widget.Tree` — hierarchical list with expand/collapse
- `widget.Separator` added to widget package
- `container.NewAppTabs` tab location options (Leading/Trailing)

---

## Platform Notes

### Windows

- Requires MSYS2 with `mingw-w64-x86_64-gcc`. Add `C:\msys64\mingw64\bin` to PATH.
- `fyne package` produces an `.exe` with bundled resources. Use `fyne release` for
  a signed installer.

### macOS

- Requires Xcode command-line tools.
- `fyne package -os darwin` produces a `.app` bundle.
- For notarization: `fyne release -os darwin -certificate <name> -developer-id <id>`.

### Linux

- Requires `gcc`, `libgl1-mesa-dev`, `xorg-dev` (or equivalent for your distro).
- `fyne package -os linux` produces a `.tar.gz`.

### Cross-compilation

Cross-compiling Fyne requires the target platform's C libraries. The recommended
approach is to use a Docker container (e.g., `fyne-cross`) or build natively on
each target OS.

```bash
go install github.com/fyne-io/fyne-cross@latest
fyne-cross windows -arch=*
fyne-cross darwin  -arch=*
fyne-cross linux   -arch=*
```

---

## Go Module Setup

```bash
go mod init myapp
go get fyne.io/fyne/v2@latest
go install fyne.io/fyne/v2/cmd/fyne@latest
```

Verify install:

```bash
fyne version
```

---

## Common Build Errors

**`gcc: command not found`** — C compiler not on PATH. Install MSYS2/Xcode/GCC.

**`cannot find -lGL`** (Linux) — Missing OpenGL dev libraries. Install `libgl1-mesa-dev`.

**`no required module provides fyne.io/fyne/v2`** — Run `go get fyne.io/fyne/v2`.

**Blank window on Windows** — Ensure the MSYS2 DLLs are in PATH at runtime, or
use `fyne package` to bundle them.
