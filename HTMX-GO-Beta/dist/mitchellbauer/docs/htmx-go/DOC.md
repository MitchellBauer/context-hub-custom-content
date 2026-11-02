---
name: htmx-go
description: "HTMX 4.0.1 stable guide for server-rendered Go applications"
metadata:
  languages: "go"
  versions: "4.0.1"
  revision: 3
  updated-on: "2026-11-01"
  source: community
  tags: "htmx,go,stable,html,templates,server-rendered,web"
---

# HTMX 4 for Go

Use this entry only when an application explicitly targets HTMX 4
(current release `4.0.1`).

HTMX 4.0.0 was released on August 28, 2026, and the 4.0.1 patch on
November 1, 2026 (see `references/htmx-4.0.1-release-notes.md`). Existing HTMX 2 applications
should use `mitchellbauer/htmx` until their migration has been tested.
The older `mitchellbauer/htmx-go-beta` ID remains available as a compatibility
lookup for this stable guidance.

## Install 4.0.1

```html
<script
  src="https://cdn.jsdelivr.net/npm/htmx.org@4.0.1"
  integrity="sha384-Qp9rdC8H7EqOoX+nR0P3RPG2Noji+qdwJlGpfzwQJsfOpp3sGwIdSP9xO3+UlEhn"
  crossorigin="anonymous"></script>
```

The CDN URL serves `dist/htmx.min.js` from the npm package. For offline Go
applications, vendor that exact artifact and record its checksum instead of
depending on a CDN at runtime. 4.0.1 `dist/htmx.min.js` SHA-256:
`a0abb04f2f45a1f89d1d4844023245537e5e6014c87b144553e0607b4cc32130`.
Read the version from the vendored file with `htmx.version` in the browser.

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
error response must return deliberate HTML for the declared target. Watch
`http.Error`: its plain-text body replaces the target too, which can wipe the
buttons a user needs to recover. Send an HTML fragment with a way back (a
retry button or a reload link) instead. Errors written by middleware
(`http.CrossOriginProtection`'s 403, `http.MaxBytesReader`) land the same way.

## Overlapping requests and double submits

Each element has a request queue. With no `hx-sync`, the strategy is
`queue first`: a second trigger while a request runs is queued (one at a
time) and sent when the first finishes. **The form values are captured when
the second trigger fires**, so the queued request repeats the old values even
if the first response replaced the form.

For anything that must not run twice (print, pay, submit an order), drop
the extra press and disable the control:

```html
<form id="main">
  <button type="button" hx-post="/print" hx-target="#work"
          hx-sync="#main:drop" hx-disable="this">Print</button>
</form>
```

- `hx-sync="#main:drop"` puts the request in the form's queue, so every
  button using the same selector shares it, and drops a trigger while one
  runs. The queue lives on the selected element, which survives swaps of
  `#work`.
- `hx-disable="this"` (a selector) disables those elements during the
  request. It is HTMX 2's `hx-disabled-elt`; HTMX 2's `hx-disable` is now
  `hx-ignore`.
- Still make the Go handler safe to repeat where it matters (an idempotency
  key or a state check). Another tab, a retry or a proxy can resend.

See `references/request-sync.md` for every strategy.

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

The `htmx-2-compat` extension additionally restores old event names. Even with
`implicitInheritance` on, 4.0.1 does not inherit the request verbs
(`hx-get`, `hx-post`, ...), `hx-action`, `hx-trigger` or `hx-validate`; put
them on each element.

## Go-specific rules

- Keep HTMX 2 and HTMX 4 templates clearly separated during migration.
- Test normal browser, HTMX partial, HTMX full, validation-error, and history
  restoration requests.
- Add `Vary` headers when full and partial responses share a URL.
- Do not assume HTMX 2 event names, inheritance, or error-status behavior.
- Guard requests that must not repeat with `hx-sync="<shared>:drop"` and
  `hx-disable`, and make the handler safe to repeat.
- Pin an exact version (`4.0.1`); do not use an unversioned `next` URL in
  deployed apps. npm's `latest` tag is still HTMX 2.

## References

- `references/migration-from-v2.md`
- `references/headers.md`
- `references/attributes-and-events.md`
- `references/request-sync.md`
- `references/go-patterns.md`
- `references/htmx-4.0.1-release-notes.md`
- `references/htmx-4.0.0-release-notes.md`
