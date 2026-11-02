---
name: htmx
description: "Official HTMX 2.x guide for building server-rendered web apps in Go"
metadata:
  languages: "go"
  versions: "2.0.11"
  revision: 4
  updated-on: "2026-10-04"
  source: community
  tags: "htmx,go,html,templates,server-rendered,web"
---

# HTMX for Go

This entry packages the core HTMX documentation into a Go-friendly reference for
server-rendered applications.

The official docs emphasize a few core ideas that map directly to Go:

- any element can issue an HTTP request
- any event can trigger that request
- any HTTP verb can be used
- any element can be the update target
- the server usually responds with HTML, not JSON

That last point is the key fit for Go apps. A typical Go + HTMX application uses
`net/http` plus `html/template`, renders full pages for normal requests, and
returns partial HTML for HTMX swaps.

## Base pattern

Serve a full page for direct navigation and a fragment for HTMX requests.

```go
func contactsPage(w http.ResponseWriter, r *http.Request) {
    data := loadContacts()

    if r.Header.Get("HX-Request") == "true" {
        renderTemplate(w, "contacts-list", data)
        return
    }

    renderTemplate(w, "contacts-page", data)
}
```

```html
<div
  hx-get="/contacts"
  hx-trigger="load"
  hx-target="#contacts-list"
  hx-swap="innerHTML">
  <div id="contacts-list">Loading...</div>
</div>
```

## Core HTMX features to use first

The official reference centers on these attributes first:

- `hx-get`
- `hx-post`
- `hx-push-url`
- `hx-select`
- `hx-select-oob`
- `hx-swap`
- `hx-swap-oob`
- `hx-target`
- `hx-trigger`
- `hx-vals`

In Go apps, the most common subset is even smaller:

- `hx-get`, `hx-post`, `hx-put`, `hx-patch`, `hx-delete`
- `hx-target`
- `hx-swap`
- `hx-trigger`
- `hx-include`
- `hx-push-url`
- `hx-boost`

## Recommended Go stack

- `net/http` is enough for many HTMX applications.
- `html/template` is the default safe choice for HTML rendering.
- Keep full-page templates and fragment templates separate.
- Return HTML for HTMX requests unless a route truly exists for a non-HTMX JSON consumer.

## Common request flow

### GET fragment into a target

```html
<button
  hx-get="/users/42/card"
  hx-target="#profile-card"
  hx-swap="outerHTML">
  Load profile
</button>
```

### POST a form and append a rendered fragment

```html
<form
  hx-post="/contacts"
  hx-target="#contacts-list"
  hx-swap="beforeend">
  <input type="text" name="name" />
  <input type="email" name="email" />
  <button type="submit">Save</button>
</form>
```

```go
func createContact(w http.ResponseWriter, r *http.Request) {
    if err := r.ParseForm(); err != nil {
        http.Error(w, "invalid form", http.StatusBadRequest)
        return
    }

    contact := saveContact(r.FormValue("name"), r.FormValue("email"))
    renderTemplate(w, "contact-row", contact)
}
```

## Practical rules

### Detect HTMX requests explicitly

- `HX-Request: true` means the request originated from HTMX.
- Still support non-HTMX navigation when practical.
- Reuse the same route for page and fragment rendering when the behavior is naturally the same.

### Return fragments with stable roots

- Use `outerHTML` only when your response includes the wrapper element.
- Use `innerHTML` when your response includes only the target contents.
- Keep target ids stable so swaps remain predictable.

### Use normal HTTP semantics

- Use `GET` for reads and navigation-style interactions.
- Use `POST`, `PUT`, `PATCH`, and `DELETE` for mutations.
- Return validation errors as HTML with an appropriate `4xx` status.

### Keep the server authoritative

- Compute UI state on the server.
- Re-render the changed fragment instead of manually mutating DOM state in JavaScript.
- Prefer idempotent fragment refreshes over custom client-side state machinery.

## ThoughtSpark-derived patterns

ThoughtSpark adds a few patterns that are especially useful in real Go apps:

- pre-parse page, partial, and admin template sets separately so block names do not collide
- return partial HTML for success and error states instead of mixing JSON into form flows
- use one admin shell page and swap tab bodies with HTMX requests
- refresh the canonical table fragment after a mutation so the UI stays server-driven
- use `HX-Trigger` for toast events and other cross-page feedback

These patterns are documented in:

- `references/go-patterns.md`
- `references/ui-patterns.md`
- `references/headers.md`
- `references/thoughtspark-admin-crud.md`

## Template layout pattern

```text
templates/
  layout.html
  pages/
    contacts.html
  partials/
    contact-row.html
    contacts-list.html
    flash.html
```

This makes it easy to serve:

- full pages for normal requests
- fragment-only responses for HTMX swaps
- out-of-band updates for shared UI like flash messages

## Important HTMX headers

The official reference calls out these request headers:

- `HX-Boosted`
- `HX-Current-URL`
- `HX-History-Restore-Request`
- `HX-Prompt`
- `HX-Request`
- `HX-Target`
- `HX-Trigger-Name`
- `HX-Trigger`

The most useful response headers for Go handlers are:

- `HX-Location`
- `HX-Push-Url`
- `HX-Redirect`
- `HX-Refresh`
- `HX-Replace-Url`
- `HX-Reswap`
- `HX-Retarget`
- `HX-Reselect`
- `HX-Trigger`
- `HX-Trigger-After-Settle`
- `HX-Trigger-After-Swap`

## Good defaults

### Search box

```html
<input
  type="search"
  name="q"
  hx-get="/search"
  hx-trigger="keyup changed delay:500ms"
  hx-target="#results"
  placeholder="Search..." />
<div id="results"></div>
```

### Row delete

```html
<button
  hx-delete="/contacts/42"
  hx-target="#contact-42"
  hx-swap="outerHTML">
  Delete
</button>
```

### Polling status

```html
<div
  hx-get="/jobs/42/status"
  hx-trigger="every 2s"
  hx-target="this"
  hx-swap="outerHTML">
  Checking status...
</div>
```

The official docs also note that a polling response can be stopped with HTTP status `286`.

## Go-specific guidance

- Use CSRF protection exactly as you would for normal forms.
- Test both full-page and HTMX fragment responses with `httptest`.
- Treat HTMX as HTML transport, not as a reason to move rendering into JavaScript.
- Prefer simple links and forms first, then enhance them with `hx-boost` or targeted swaps.

## References

- `references/attributes.md`
- `references/headers.md`
- `references/go-patterns.md`
- `references/ui-patterns.md`
- `references/thoughtspark-admin-crud.md`
- `references/version-notes.md`
- `release-deltas/htmx-2.0.9.md`

## Latest release guidance

- `release-deltas/htmx-2.0.11.md`
