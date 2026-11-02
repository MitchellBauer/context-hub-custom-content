# Fyne Canvas and Drawing Reference

## Import

```go
import (
    "fyne.io/fyne/v2"
    "fyne.io/fyne/v2/canvas"
    "fyne.io/fyne/v2/container"
)
```

Canvas objects are low-level drawing primitives. They implement `fyne.CanvasObject`
and can be placed inside containers or used as widget renderers.

---

## Canvas Objects

### Rectangle

```go
rect := canvas.NewRectangle(color.RGBA{R: 255, A: 255})
rect.FillColor = color.RGBA{R: 200, G: 100, B: 0, A: 255}
rect.StrokeColor = color.Black
rect.StrokeWidth = 2
rect.CornerRadius = 4   // rounded corners
rect.Resize(fyne.NewSize(100, 50))
rect.Move(fyne.NewPos(10, 10))
canvas.Refresh(rect)
```

### Circle

```go
circle := canvas.NewCircle(color.RGBA{B: 255, A: 255})
circle.FillColor = color.RGBA{G: 200, A: 255}
circle.StrokeColor = color.Black
circle.StrokeWidth = 1
circle.Resize(fyne.NewSize(80, 80))
```

### Line

```go
line := canvas.NewLine(color.Black)
line.StrokeWidth = 2
line.Position1 = fyne.NewPos(0, 0)
line.Position2 = fyne.NewPos(100, 50)
canvas.Refresh(line)
```

### Text

```go
txt := canvas.NewText("Hello", color.Black)
txt.TextSize = 18
txt.TextStyle = fyne.TextStyle{Bold: true}
txt.Alignment = fyne.TextAlignCenter
canvas.Refresh(txt)
```

Note: `canvas.Text` does not wrap. Use `widget.Label` for wrappable text.

### Image

```go
// From a resource (embedded file)
img := canvas.NewImageFromResource(resourceLogoPng)

// From file path
img := canvas.NewImageFromFile("/path/to/image.png")

// From Go image
img := canvas.NewImageFromImage(goImg)

img.FillMode = canvas.ImageFillContain   // preserve aspect ratio
img.FillMode = canvas.ImageFillStretch   // stretch to fill
img.FillMode = canvas.ImageFillOriginal  // actual pixel size
img.Translucency = 0.5                   // 0.0 opaque, 1.0 transparent
img.Resize(fyne.NewSize(200, 150))
canvas.Refresh(img)
```

### Raster (procedural drawing)

Generate pixels dynamically. The callback receives the pixel dimensions and
returns an `image.Image`.

```go
raster := canvas.NewRaster(func(w, h int) image.Image {
    img := image.NewRGBA(image.Rect(0, 0, w, h))
    for y := 0; y < h; y++ {
        for x := 0; x < w; x++ {
            img.SetRGBA(x, y, color.RGBA{
                R: uint8(x * 255 / w),
                G: uint8(y * 255 / h),
                A: 255,
            })
        }
    }
    return img
})
raster.Resize(fyne.NewSize(200, 200))
```

### Gradient

```go
// Linear gradient
grad := canvas.NewLinearGradient(
    color.RGBA{R: 255, A: 255},  // start color
    color.RGBA{B: 255, A: 255},  // end color
    0,                           // angle in degrees (0 = left→right)
)

// Radial gradient
grad := canvas.NewRadialGradient(
    color.RGBA{R: 255, A: 255},
    color.RGBA{B: 255, A: 255},
)
grad.Resize(fyne.NewSize(100, 100))
```

---

## Refreshing Canvas Objects

After changing a canvas object's properties, call `canvas.Refresh(obj)` to
redraw it. For widget renderers, call `r.Layout(size)` + return from
`CreateRenderer`.

```go
rect.FillColor = color.RGBA{R: 100, A: 255}
canvas.Refresh(rect)
```

---

## Placing Canvas Objects in a Window

Canvas objects go inside containers like any other `fyne.CanvasObject`:

```go
c := container.NewWithoutLayout(rect, circle, line)
rect.Move(fyne.NewPos(10, 10))
rect.Resize(fyne.NewSize(80, 40))
w.SetContent(c)
```

Or mix with widgets using `container.NewStack`:

```go
w.SetContent(container.NewStack(
    canvas.NewRectangle(color.RGBA{R: 240, G: 240, B: 240, A: 255}), // background
    container.NewVBox(widget.NewLabel("on top"), widget.NewButton("btn", nil)),
))
```

---

## Accessing the Canvas Directly

```go
c := w.Canvas()
c.SetOnTypedKey(func(ev *fyne.KeyEvent) {
    fmt.Println("key:", ev.Name)
})
c.SetOnTypedRune(func(r rune) {
    fmt.Println("rune:", string(r))
})
c.Focus(entry)       // focus a focusable widget
c.Unfocus()
c.Focused()          // currently focused widget
size := c.Size()     // canvas dimensions
```

---

## Animation

Fyne's animation API drives float-valued transitions over time.

```go
import "fyne.io/fyne/v2/canvas"

anim := canvas.NewColorRGBAAnimation(
    color.RGBA{R: 255, A: 255},
    color.RGBA{B: 255, A: 255},
    time.Second,
    func(c color.Color) {
        rect.FillColor = c
        canvas.Refresh(rect)
    },
)
anim.Curve = fyne.AnimationEaseInOut  // EaseIn | EaseOut | EaseInOut | Linear
anim.RepeatCount = fyne.AnimationRepeatForever
anim.AutoReverse = true
anim.Start()
// later:
anim.Stop()
```

General-purpose float animation:

```go
anim := canvas.NewPositionAnimation(
    fyne.NewPos(0, 0),
    fyne.NewPos(200, 100),
    500*time.Millisecond,
    func(p fyne.Position) {
        obj.Move(p)
        canvas.Refresh(obj)
    },
)
anim.Start()
```

---

## Custom Widget Renderer (Canvas-based)

When building a custom widget with custom drawing:

```go
type MyWidget struct {
    widget.BaseWidget
}

type myRenderer struct {
    rect   *canvas.Rectangle
    label  *canvas.Text
    widget *MyWidget
}

func (w *MyWidget) CreateRenderer() fyne.WidgetRenderer {
    rect := canvas.NewRectangle(color.RGBA{G: 200, A: 255})
    lbl := canvas.NewText("value", color.Black)
    return &myRenderer{rect: rect, label: lbl, widget: w}
}

func (r *myRenderer) Layout(size fyne.Size) {
    r.rect.Resize(size)
    r.label.Move(fyne.NewPos(4, 4))
}

func (r *myRenderer) MinSize() fyne.Size {
    return fyne.NewSize(60, 30)
}

func (r *myRenderer) Refresh() {
    canvas.Refresh(r.rect)
    canvas.Refresh(r.label)
}

func (r *myRenderer) Objects() []fyne.CanvasObject {
    return []fyne.CanvasObject{r.rect, r.label}
}

func (r *myRenderer) Destroy() {}
```
