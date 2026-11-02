---
name: htmx-go-beta
description: "HTMX 4.0.0 stable guide for server-rendered Go applications"
metadata:
  languages: "go"
  versions: "4.0.0"
  revision: 2
  updated-on: "2026-10-04"
  source: community
  tags: "htmx,go,stable,html,templates,server-rendered,web"
---

# HTMX 4 for Go

Use this entry only when an application explicitly targets HTMX
`4.0.0`.

HTMX 4.0.0 was released on August 28, 2026. Existing HTMX 2 applications
should use `mitchellbauer/htmx` until their migration has been tested.
The stable HTMX 4 lookup is `mitchellbauer/htmx-go`; this older ID remains
available for compatibility with existing callers.

## Install 4.0.0

```html
<script
  src="https://cdn.jsdelivr.net/npm/htmx.org@4.0.0"
  integrity="sha384-BvJpBiO8Kh31EqtJe5DRIeWrHWnCGkwytKs9NKFi86Hhw96dEqdEMzZDeK9iEGTc"
  crossorigin="anonymous"></script>
```

For offline Go applications, vendor that exact artifact and record its checksum
instead of depending on a CDN at runtime.

## What remains familiar

The HTML-over-the-wire architecture is unchanged:

- elements issue HTTP requests
- Go handlers return HTML
- `hx-target` selects the update destination
- `hx-swap` controls insertion
- forms and links remain the progressive-enhancement foundation

```html
<form
  hx-post="/contacts"
  hx-target="#contacts"
  hx-swap="beforeend">
  <input name="name" required>
  <button type="submit">Add</button>
</form>
```

```go
func createContact(w http.ResponseWriter, r *http.Request) {
    if err := r.ParseForm(); err != nil {
        http.Error(w, "invalid form", http.StatusBadRequest)
        return
    }

    contact := saveContact(r.FormValue("name"))
    renderTemplate(w, "contact-row", contact)
}
```

## Two major default changes

### Attribute inheritance is explicit

HTMX 2 inherited many attributes automatically. HTMX 4 requires
`:inherited`:

```html
<div hx-confirm:inherited="Delete this item?">
  <button hx-delete="/items/42">Delete</button>
</div>
```

### Error responses swap by default

HTMX 4 swaps `4xx` and `5xx` response bodies. Only `204` and `304` skip swaps
by default.

This suits Go handlers that render validation and error fragments, but every
error response must return deliberate HTML for the declared target.

## Request detection

```go
func requestType(r *http.Request) string {
    if r.Header.Get("HX-Request") != "true" {
        return "browser"
    }
    return r.Header.Get("HX-Request-Type") // "partial" or "full"
}
```

HTMX 4 also sends `Accept: text/html`.

## Migration compatibility

To temporarily restore the two main HTMX 2 defaults:

```html
<script>
  htmx.config.implicitInheritance = true
  htmx.config.noSwap = [204, 304, '4xx', '5xx']
</script>
```

The `htmx-2-compat` extension additionally restores old event names.

## Go-specific rules

- Keep HTMX 2 and HTMX 4 templates clearly separated during migration.
- Test normal browser, HTMX partial, HTMX full, validation-error, and history
  restoration requests.
- Add `Vary` headers when full and partial responses share a URL.
- Do not assume HTMX 2 event names, inheritance, or error-status behavior.
- Pin `4.0.0`; do not use an unversioned `next` URL in deployed apps.

## References

- `references/migration-from-v2.md`
- `references/headers.md`
- `references/attributes-and-events.md`
- `references/go-patterns.md`
- `references/htmx-4.0.0-release-notes.md`
