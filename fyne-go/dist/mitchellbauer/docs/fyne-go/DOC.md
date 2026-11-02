---
name: fyne-go
description: "Fyne v2 GUI toolkit guide for building cross-platform desktop apps in Go"
metadata:
  languages: "go"
  versions: "2.8.2"
  revision: 4
  updated-on: "2026-11-01"
  source: community
  tags: "fyne,go,gui,desktop,ui,cross-platform,widgets"
---

# Fyne for Go

Fyne is a cross-platform GUI toolkit written in Go. A single codebase produces
native-style desktop apps on Windows, macOS, Linux, and mobile. It uses OpenGL
for rendering and requires a C compiler at build time.

It is written for apps that:

- ship as standalone desktop executables
- need a native-feel UI without embedding a web browser
- want to stay in pure Go without JavaScript or HTML/CSS

## Prerequisites

A C compiler is required:

- **Windows**: Install [MSYS2](https://www.msys2.org/) and add `mingw-w64-x86_64-gcc` to PATH
- **macOS**: Install Xcode command-line tools (`xcode-select --install`)
- **Linux**: `sudo apt-get install gcc libgl1-mesa-dev xorg-dev`

Install the toolkit and CLI tool:

```bash
go get fyne.io/fyne/v2
go install fyne.io/fyne/v2/cmd/fyne@latest
```

## Minimal application

```go
package main

import (
    "fyne.io/fyne/v2/app"
    "fyne.io/fyne/v2/widget"
)

func main() {
    a := app.New()
    w := a.NewWindow("Hello")
    w.SetContent(widget.NewLabel("Hello, Fyne!"))
    w.ShowAndRun()
}
```

`ShowAndRun` combines `Show` and `app.Run`. Call it on the main window at the
end of `main`. It blocks until the window is closed.

## Application and window

```go
a := app.New()                         // create the app (one per process)
a.SetIcon(resourceIconPng)            // optional app icon (embedded resource)

w := a.NewWindow("My App")            // primary window
w.Resize(fyne.NewSize(800, 600))      // set initial size
w.SetFixedSize(true)                  // prevent resize
w.CenterOnScreen()                    // center before showing
w.SetMaster()                         // closing this window quits the app

w2 := a.NewWindow("Second")          // additional windows are fine
w2.Show()                             // show without blocking

w.ShowAndRun()                        // show main window and start event loop
```

## Setting content

`SetContent` replaces the window's content with any `fyne.CanvasObject`.
Most of the time that is a container wrapping multiple widgets.

```go
w.SetContent(
    container.NewVBox(
        widget.NewLabel("Name"),
        widget.NewEntry(),
        widget.NewButton("Submit", func() { fmt.Println("clicked") }),
    ),
)
```

Call `w.Content().Refresh()` to force a redraw if you update a widget that
does not automatically trigger one.

## Thread safety

GUI updates must happen on the main thread. When updating from a goroutine,
wrap the update in `fyne.Do` (non-blocking) or `fyne.DoAndWait` (blocking):

```go
go func() {
    result := doExpensiveWork()
    fyne.Do(func() {
        label.SetText(result)
    })
}()
```

`fyne.Do` / `fyne.DoAndWait` were added in v2.6. Before that, `fyne.Canvas.Refresh`
was called directly, which was not always safe.

## Common widget patterns

### Label

```go
lbl := widget.NewLabel("Hello")
lbl.SetText("Updated")
lbl.Wrapping = fyne.TextWrapWord   // wrap long text
```

### Button

```go
btn := widget.NewButton("Click me", func() {
    fmt.Println("tapped")
})
btn.Importance = widget.HighImportance  // primary/accent style
btn.Disable()
btn.Enable()
```

### Entry (single-line text input)

```go
entry := widget.NewEntry()
entry.SetPlaceHolder("Type here...")
entry.OnChanged = func(s string) { fmt.Println(s) }
entry.OnSubmitted = func(s string) { fmt.Println("submitted:", s) }
text := entry.Text
```

### Check

```go
check := widget.NewCheck("Enable feature", func(checked bool) {
    fmt.Println("checked:", checked)
})
check.SetChecked(true)
```

### Select (dropdown)

```go
sel := widget.NewSelect([]string{"Option A", "Option B", "Option C"}, func(s string) {
    fmt.Println("selected:", s)
})
sel.SetSelected("Option A")
```

### ProgressBar

```go
bar := widget.NewProgressBar()
bar.SetValue(0.5)   // 0.0 to 1.0
```

For indeterminate: `widget.NewProgressBarInfinite()`.

## Common layout patterns

```go
import "fyne.io/fyne/v2/container"
import "fyne.io/fyne/v2/layout"

// Vertical stack
container.NewVBox(widget1, widget2, widget3)

// Horizontal row
container.NewHBox(widget1, widget2, widget3)

// 3-column grid
container.New(layout.NewGridLayout(3), w1, w2, w3, w4, w5, w6)

// Border layout (cardinal positions + center fill)
container.NewBorder(top, bottom, left, right, center)

// Form (label-field pairs)
container.New(layout.NewFormLayout(),
    widget.NewLabel("Name"), widget.NewEntry(),
    widget.NewLabel("Email"), widget.NewEntry(),
)

// Centered single widget
container.NewCenter(widget.NewLabel("Centered"))
```

## Data binding basics

Bind a string to a label so updates propagate automatically:

```go
import "fyne.io/fyne/v2/data/binding"

str := binding.NewString()
str.Set("initial value")

lbl := widget.NewLabelWithData(str)

// Update from anywhere (even goroutines — binding is thread-safe)
str.Set("new value")  // label refreshes automatically
```

## Menus

```go
a.SetIcon(resourceIconPng)

menu := fyne.NewMainMenu(
    fyne.NewMenu("File",
        fyne.NewMenuItem("Open", func() { /* ... */ }),
        fyne.NewMenuItemSeparator(),
        fyne.NewMenuItem("Quit", func() { a.Quit() }),
    ),
    fyne.NewMenu("Help",
        fyne.NewMenuItem("About", func() { /* ... */ }),
    ),
)
w.SetMainMenu(menu)
```

## Dialogs

```go
import "fyne.io/fyne/v2/dialog"

// Simple info dialog
dialog.ShowInformation("Title", "Message body.", w)

// Confirmation
dialog.ShowConfirm("Delete?", "This cannot be undone.", func(ok bool) {
    if ok { deleteItem() }
}, w)

// File open
dialog.ShowFileOpen(func(r fyne.URIReadCloser, err error) {
    if r == nil { return }
    defer r.Close()
    // read from r
}, w)
```

## Packaging

```bash
# Bundle app with icon for current platform
fyne package -icon icon.png

# Cross-compile for a specific OS
fyne package -os windows -icon icon.png
fyne package -os darwin  -icon icon.png
fyne package -os linux   -icon icon.png

# Embed static resources (images, fonts) into Go code
fyne bundle -o bundled.go icon.png
```

`fyne package` produces a platform-native distributable (`.exe` installer on
Windows, `.app` bundle on macOS, `.tar.gz` on Linux).

## References

- `references/widgets.md`
- `references/layouts-containers.md`
- `references/data-binding.md`
- `references/canvas-drawing.md`
- `references/version-notes.md`
- `release-deltas/fyne-2.8.0.md`

## Latest release guidance

- `release-deltas/fyne-2.8.2.md`
