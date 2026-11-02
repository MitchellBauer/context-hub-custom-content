# Fyne Layouts and Containers Reference

## Imports

```go
import (
    "fyne.io/fyne/v2"
    "fyne.io/fyne/v2/container"
    "fyne.io/fyne/v2/layout"
    "fyne.io/fyne/v2/widget"
)
```

---

## Layout Types

### HBox — horizontal row

Items arranged left-to-right. Each item takes its natural width. A `layout.Spacer`
pushes subsequent items to the right edge.

```go
container.NewHBox(
    widget.NewLabel("Left"),
    layout.NewSpacer(),
    widget.NewButton("Right", nil),
)
```

### VBox — vertical stack

Items stacked top-to-bottom. Each item takes its natural height.

```go
container.NewVBox(
    widget.NewLabel("Top"),
    widget.NewEntry(),
    widget.NewButton("Bottom", nil),
)
```

### Grid — fixed columns

Items flow left-to-right then wrap. All cells are the same size (max of all items).

```go
container.New(layout.NewGridLayout(3),
    widget.NewButton("1", nil),
    widget.NewButton("2", nil),
    widget.NewButton("3", nil),
    widget.NewButton("4", nil),
    widget.NewButton("5", nil),
)
```

### GridWrap — fixed item size, wrapping rows

All items are forced to the same specified size and wrap into rows.

```go
container.New(layout.NewGridWrapLayout(fyne.NewSize(100, 80)),
    widget.NewButton("A", nil),
    widget.NewButton("B", nil),
    widget.NewButton("C", nil),
)
```

### Border — edge anchoring

Top, bottom, left, and right items are anchored to their respective edges.
The center item expands to fill the remaining space.

```go
container.NewBorder(
    widget.NewToolbar(...),    // top
    widget.NewLabel("status"), // bottom
    nil,                       // left (omit with nil)
    nil,                       // right
    mainContent,               // center — fills remaining space
)
```

### Form — label-value pairs

Two-column layout where odd children are labels and even children are inputs.
Equivalent to `layout.NewFormLayout`.

```go
container.New(layout.NewFormLayout(),
    widget.NewLabel("Name"),  widget.NewEntry(),
    widget.NewLabel("Email"), widget.NewEntry(),
    widget.NewLabel("Role"),  widget.NewSelect(roles, nil),
)
```

Or use the `widget.Form` widget directly for built-in submit/cancel buttons.

### Center

Positions a single child in the center of the available space.

```go
container.NewCenter(widget.NewLabel("Centered"))
```

### Max / Stack

All children fill the full space, layered on top of each other.
`container.NewStack` is the idiomatic name in v2.

```go
container.NewStack(backgroundWidget, foregroundWidget)
```

### Padded

Wraps content with the theme's standard padding on all sides.

```go
container.NewPadded(widget.NewLabel("Padded content"))
```

### Without layout (manual positioning)

Position and size each child manually. Useful for canvas-based UIs, not typical widget UIs.

```go
c := container.NewWithoutLayout(widget1, widget2)
widget1.Move(fyne.NewPos(10, 20))
widget1.Resize(fyne.NewSize(100, 30))
```

---

## Container-Specific Types

### AppTabs

Tab bar that switches between named content panes.

```go
tabs := container.NewAppTabs(
    container.NewTabItem("Home", homeContent),
    container.NewTabItem("Settings", settingsContent),
)
tabs.SetTabLocation(container.TabLocationTop)    // Top | Bottom | Leading | Trailing
tabs.OnChanged = func(tab *container.TabItem) { }
tabs.SelectIndex(0)
tabs.Selected()       // *TabItem
```

### DocTabs

Like AppTabs but with closeable tabs, suited for document-style apps.

```go
dt := container.NewDocTabs(
    container.NewTabItem("file.go", editor1),
)
dt.OnClosed = func(tab *container.TabItem) { }
dt.Append(container.NewTabItem("new.go", editor2))
```

### Scroll

Makes any content scrollable. Wraps a single child.

```go
scroll := container.NewScroll(widget.NewLabel("long content..."))
scroll := container.NewVScroll(content)   // vertical only
scroll := container.NewHScroll(content)   // horizontal only

scroll.ScrollToBottom()
scroll.ScrollToTop()
scroll.Offset  // fyne.Position — current scroll position
```

### Split

Divides space between two items with a draggable divider.

```go
split := container.NewHSplit(leftPanel, rightPanel)
split := container.NewVSplit(topPanel, bottomPanel)

split.Offset = 0.3   // 0.0–1.0, fraction given to the leading pane
```

### InnerWindow (v2.5+)

An in-app floating panel with a title bar, useful for MDI-style UIs.

```go
inner := container.NewInnerWindow("Panel Title", content)
inner.CloseIntercept = func() { /* handle close */ }
```

---

## Nesting Containers

Build complex layouts by nesting containers. A common three-panel layout:

```go
sidebar := container.NewVBox(
    widget.NewButton("Item 1", nil),
    widget.NewButton("Item 2", nil),
)

main := container.NewBorder(
    widget.NewToolbar(...),   // top toolbar
    nil, nil, nil,
    container.NewScroll(contentWidget),  // scrollable center
)

w.SetContent(container.NewHSplit(sidebar, main))
```

---

## Spacers

`layout.NewSpacer()` expands to fill available space in HBox/VBox:

```go
// Right-align a button in a toolbar row
container.NewHBox(
    widget.NewLabel("Title"),
    layout.NewSpacer(),
    widget.NewButton("Action", nil),
)
```

---

## Refreshing Containers

After adding or removing items from a container's `Objects` slice, call `Refresh`:

```go
c := container.NewVBox(widget.NewLabel("initial"))

// Add item dynamically
c.Add(widget.NewLabel("added"))      // Add method handles refresh

// Or mutate and refresh manually
c.Objects = append(c.Objects, widget.NewLabel("manual"))
c.Refresh()
```
