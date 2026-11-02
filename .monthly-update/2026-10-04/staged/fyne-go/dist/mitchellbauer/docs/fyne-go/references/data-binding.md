# Fyne Data Binding Reference

## Import

```go
import "fyne.io/fyne/v2/data/binding"
```

Data binding connects a widget's display to an underlying value. When the value
changes, bound widgets refresh automatically. Updates via binding are thread-safe.

---

## Primitive Bindings

Each primitive type has a `New<Type>` constructor and an `External<Type>` variant
for wrapping an existing variable.

### String

```go
s := binding.NewString()
s.Set("hello")
v, err := s.Get()   // returns (string, error)

// Bind to a widget
lbl := widget.NewLabelWithData(s)
entry := widget.NewEntryWithData(s)

// Listen for changes
s.AddListener(binding.NewDataListener(func() {
    v, _ := s.Get()
    fmt.Println("changed to:", v)
}))
```

### Int

```go
n := binding.NewInt()
n.Set(42)
v, _ := n.Get()

lbl := widget.NewLabelWithData(binding.IntToString(n))
```

### Float

```go
f := binding.NewFloat()
f.Set(3.14)
v, _ := f.Get()

sl := widget.NewSliderWithData(0, 100, f)
pb := widget.NewProgressBarWithData(f)
```

### Bool

```go
b := binding.NewBool()
b.Set(true)
v, _ := b.Get()

check := widget.NewCheckWithData("Enable", b)
```

### Bytes, Rune, URI

```go
by := binding.NewBytes()
r  := binding.NewRune()
u  := binding.NewURI()
```

---

## External Bindings

Wrap an existing Go variable so the binding reflects and updates it.

```go
name := "Alice"
ext := binding.BindString(&name)

ext.Set("Bob")
fmt.Println(name)  // "Bob"

v, _ := ext.Get()
fmt.Println(v)     // "Bob"
```

The binding holds a pointer to the variable. Changes via `Set` update the variable;
changes to the variable directly do NOT notify listeners — call `ext.Reload()` to
push external changes into the binding.

```go
name = "Carol"
ext.Reload()   // notifies listeners with the new value
```

---

## Type Conversion

Convert between incompatible binding types using built-in converters.

```go
n := binding.NewInt()

// Int → String for display in a label
strN := binding.IntToString(n)
lbl := widget.NewLabelWithData(strN)

// Float → String
f := binding.NewFloat()
strF := binding.FloatToString(f)

// Int → Float
floatFromInt := binding.IntToFloat(n)
```

Custom converter (implement `binding.DataItem`):

```go
upper := binding.NewSprintf("%s", s)   // format string to string
```

For complex transforms use `binding.NewDataListener` and compute manually.

---

## Collection Bindings

### StringList

```go
list := binding.NewStringList()
list.Set([]string{"Apple", "Banana", "Cherry"})
list.Append("Date")

v, _ := list.GetValue(0)   // "Apple"
list.SetValue(0, "Avocado")

length := list.Length()

// Bind to a List widget
wlist := widget.NewListWithData(list,
    func() fyne.CanvasObject { return widget.NewLabel("item") },
    func(item binding.DataItem, obj fyne.CanvasObject) {
        str, _ := item.(binding.String).Get()
        obj.(*widget.Label).SetText(str)
    },
)
```

### UntypedList

```go
ul := binding.NewUntypedList()
ul.Append("value")
ul.Append(42)
v, _ := ul.GetValue(0)
```

### StringTree

```go
tree := binding.NewStringTree()
tree.Set(
    map[string][]string{
        "":    {"fruits", "veggies"},
        "fruits":  {"apple", "banana"},
        "veggies": {"carrot"},
    },
    map[string]string{
        "fruits":  "Fruits",
        "veggies": "Vegetables",
        "apple":   "Apple",
        "banana":  "Banana",
        "carrot":  "Carrot",
    },
)
```

### DataMap

```go
m := binding.NewStringMap()
m.Set(map[string]string{"key": "value"})
m.SetValue("key", "updated")
v, _ := m.GetValue("key")
keys, _ := m.Keys()
```

---

## Preferences Binding

Persist values through app restarts using `app.Preferences()`.

```go
a := app.New()
prefs := a.Preferences()

// Bind directly to a preference key
darkMode := binding.BindPreferenceBool("dark-mode", prefs)
darkMode.Set(true)

// On next launch, .Get() returns true automatically
```

Available preference binding types:
- `BindPreferenceBool(key, prefs)`
- `BindPreferenceString(key, prefs)`
- `BindPreferenceInt(key, prefs)`
- `BindPreferenceFloat(key, prefs)`

---

## Listeners

Any binding can have listeners attached.

```go
s := binding.NewString()

listener := binding.NewDataListener(func() {
    v, _ := s.Get()
    fmt.Println("new value:", v)
})

s.AddListener(listener)
// later:
s.RemoveListener(listener)
```

---

## Thread Safety

All binding operations (`Get`, `Set`, `Append`, etc.) are safe to call from any
goroutine. Listener callbacks are dispatched on the main goroutine, so they can
safely update widgets without using `fyne.Do`.
