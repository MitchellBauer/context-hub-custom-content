# Fyne Widgets Reference

## Standard Widgets

Import: `fyne.io/fyne/v2/widget`

### Label

```go
lbl := widget.NewLabel("text")
lbl := widget.NewLabelWithStyle("text", fyne.TextAlignCenter, fyne.TextStyle{Bold: true})
lbl := widget.NewLabelWithData(binding.NewString())  // bound label

lbl.SetText("new text")
lbl.Text              // current text value
lbl.Alignment         // fyne.TextAlignLeading | Center | Trailing
lbl.Wrapping          // fyne.TextTruncate | TextWrapBreak | TextWrapWord
lbl.TextStyle.Bold    // true/false
lbl.TextStyle.Italic  // true/false
lbl.Refresh()         // force redraw after direct field mutation
```

### Button

```go
btn := widget.NewButton("Label", func() { /* tapped */ })
btn := widget.NewButtonWithIcon("Label", theme.HomeIcon(), func() { /* tapped */ })

btn.SetText("new label")
btn.SetIcon(theme.DeleteIcon())
btn.Importance = widget.LowImportance      // subtle appearance
btn.Importance = widget.MediumImportance   // default
btn.Importance = widget.HighImportance     // accent/primary
btn.Importance = widget.DangerImportance   // destructive (red)
btn.Importance = widget.WarningImportance  // warning (amber)
btn.Disable()
btn.Enable()
btn.Disabled()  // bool
```

### Entry (single-line text input)

```go
e := widget.NewEntry()
e := widget.NewEntryWithData(binding.NewString())

e.SetText("value")
e.SetPlaceHolder("hint text")
e.Text              // current value
e.OnChanged = func(s string) { }
e.OnSubmitted = func(s string) { }   // Enter key
e.Password = true   // mask characters — must set before rendering or call Refresh
e.MultiLine = true  // becomes a multiline text area
e.Wrapping = fyne.TextWrapWord
e.Validator = validation.NewRegexp(`\d+`, "must be digits")
```

### Multiline entry

```go
ta := widget.NewMultiLineEntry()
ta.SetText("line1\nline2")
ta.Wrapping = fyne.TextWrapWord
ta.SetMinRowsVisible(5)
```

### Check

```go
c := widget.NewCheck("Label", func(checked bool) { })
c := widget.NewCheckWithData("Label", binding.NewBool())

c.SetChecked(true)
c.Checked  // bool
c.Disable()
```

### RadioGroup

```go
rg := widget.NewRadioGroup([]string{"A", "B", "C"}, func(s string) { })
rg.SetSelected("B")
rg.Selected     // string
rg.Horizontal = true
```

### Select (dropdown)

```go
sel := widget.NewSelect([]string{"One", "Two", "Three"}, func(s string) { })
sel.SetSelected("Two")
sel.Selected          // string
sel.PlaceHolder = "Choose..."
sel.SetOptions([]string{"X", "Y"})
```

### SelectEntry (editable dropdown)

```go
se := widget.NewSelectEntry([]string{"Option A", "Option B"})
se.SetText("custom value")
se.SetOptions([]string{"New", "Options"})
```

### Slider

```go
sl := widget.NewSlider(0, 100)       // min, max
sl := widget.NewSliderWithData(0, 100, binding.NewFloat())

sl.SetValue(42)
sl.Value        // float64
sl.Step = 5     // snap increment
sl.Orientation = widget.Vertical  // default is Horizontal
sl.OnChanged = func(f float64) { }
```

### ProgressBar

```go
pb := widget.NewProgressBar()       // 0.0 to 1.0
pb.SetValue(0.75)
pb.Value  // float64

inf := widget.NewProgressBarInfinite()  // animated, indeterminate
inf.Start()
inf.Stop()
```

### Separator

```go
widget.NewSeparator()   // horizontal rule, useful in VBox
```

### Toolbar

```go
tb := widget.NewToolbar(
    widget.NewToolbarAction(theme.DocumentCreateIcon(), func() { /* new */ }),
    widget.NewToolbarSeparator(),
    widget.NewToolbarAction(theme.DeleteIcon(), func() { /* delete */ }),
    widget.NewToolbarSpacer(),
    widget.NewToolbarAction(theme.HelpIcon(), func() { /* help */ }),
)
```

### Card

```go
card := widget.NewCard("Title", "Subtitle",
    widget.NewLabel("Card body content"),
)
card.SetTitle("New Title")
card.SetSubTitle("New Sub")
card.SetContent(widget.NewButton("Action", nil))
```

### Accordion

```go
acc := widget.NewAccordion(
    widget.NewAccordionItem("Section 1", widget.NewLabel("Content 1")),
    widget.NewAccordionItem("Section 2", widget.NewLabel("Content 2")),
)
acc.MultiOpen = true   // allow multiple sections open at once
acc.Open(0)            // open item by index
acc.Close(0)
```

### RichText

```go
rt := widget.NewRichTextFromMarkdown("**Bold** and _italic_ text")
rt := widget.NewRichText(
    &widget.TextSegment{
        Text:  "Bold",
        Style: widget.RichTextStyleStrong,
    },
    &widget.TextSegment{Text: " normal"},
)
rt.Wrapping = fyne.TextWrapWord
```

### Hyperlink

```go
u, _ := url.Parse("https://fyne.io")
hl := widget.NewHyperlink("Visit Fyne", u)
hl.SetText("New Label")
hl.SetURL(u)
```

### Icon

```go
icon := widget.NewIcon(theme.HomeIcon())
icon.SetResource(theme.InfoIcon())
```

### Form widget

```go
form := widget.NewForm(
    widget.NewFormItem("Name", widget.NewEntry()),
    widget.NewFormItem("Email", widget.NewEntry()),
)
form.OnSubmit = func() { fmt.Println("submitted") }
form.OnCancel = func() { fmt.Println("cancelled") }
form.SubmitText = "Save"
form.CancelText = "Discard"
```

---

## Collection Widgets

Collection widgets are optimized for large datasets. They use a template + data
approach instead of creating one widget per item.

### List

```go
list := widget.NewList(
    func() int { return len(items) },                         // count
    func() fyne.CanvasObject {                                // create template
        return widget.NewLabel("template")
    },
    func(id widget.ListItemID, obj fyne.CanvasObject) {       // update item
        obj.(*widget.Label).SetText(items[id])
    },
)
list.OnSelected = func(id widget.ListItemID) { fmt.Println(id) }
list.OnUnselected = func(id widget.ListItemID) { }
list.Select(0)
list.Unselect(0)
list.Refresh()   // call after items slice changes
```

### Table

```go
table := widget.NewTable(
    func() (int, int) { return rows, cols },
    func() fyne.CanvasObject { return widget.NewLabel("cell") },
    func(id widget.TableCellID, obj fyne.CanvasObject) {
        obj.(*widget.Label).SetText(data[id.Row][id.Col])
    },
)
table.SetColumnWidth(0, 200)
table.SetRowHeight(0, 40)
table.OnSelected = func(id widget.TableCellID) { }
```

### Tree

```go
tree := widget.NewTree(
    func(id widget.TreeNodeID) []widget.TreeNodeID {    // child IDs
        return children[id]
    },
    func(id widget.TreeNodeID) bool {                  // is branch?
        return len(children[id]) > 0
    },
    func(branch bool) fyne.CanvasObject {              // create template
        return widget.NewLabel("node")
    },
    func(id widget.TreeNodeID, branch bool, obj fyne.CanvasObject) { // update
        obj.(*widget.Label).SetText(id)
    },
)
tree.OnSelected = func(id widget.TreeNodeID) { }
tree.OpenBranch("root")
tree.CloseBranch("root")
```

### GridWrap

```go
grid := widget.NewGridWrap(
    fyne.NewSize(100, 100),                           // item size
    func() int { return len(items) },
    func() fyne.CanvasObject { return widget.NewLabel("item") },
    func(id widget.GridWrapItemID, obj fyne.CanvasObject) {
        obj.(*widget.Label).SetText(items[int(id)])
    },
)
```

---

## Disabling and Enabling Widgets

Any widget implementing `fyne.Disableable`:

```go
w.Disable()
w.Enable()
w.Disabled()  // bool
```

---

## Custom Widgets

Implement `fyne.Widget` by embedding `widget.BaseWidget`:

```go
type MyWidget struct {
    widget.BaseWidget
    value string
}

func NewMyWidget(v string) *MyWidget {
    w := &MyWidget{value: v}
    w.ExtendBaseWidget(w)
    return w
}

func (w *MyWidget) CreateRenderer() fyne.WidgetRenderer {
    lbl := widget.NewLabel(w.value)
    return widget.NewSimpleRenderer(lbl)
}
```
