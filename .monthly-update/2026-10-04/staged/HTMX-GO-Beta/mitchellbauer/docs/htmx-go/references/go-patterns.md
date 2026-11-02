# Go Patterns for HTMX 4

## Full versus partial rendering

```go
func contacts(w http.ResponseWriter, r *http.Request) {
    data := loadContacts(r.Context())

    w.Header().Add("Vary", "HX-Request")
    w.Header().Add("Vary", "HX-Request-Type")

    if r.Header.Get("HX-Request") == "true" &&
        r.Header.Get("HX-Request-Type") == "partial" {
        renderTemplate(w, "contacts-list", data)
        return
    }

    renderTemplate(w, "contacts-page", data)
}
```

## Validation errors

HTMX 4 swaps error bodies by default. A Go handler can return a targeted
validation fragment with `422`:

```go
if validationErr != nil {
    w.WriteHeader(http.StatusUnprocessableEntity)
    renderTemplate(w, "contact-form-errors", data)
    return
}
```

Make sure the triggering element's target is appropriate for both success and
error fragments, or use `hx-status`/`HX-Retarget`.

## History restoration

Treat `HX-History-Restore-Request: true` as a request for a complete,
restorable representation unless the route deliberately implements a different
history strategy.

## Testing matrix

Use `httptest` to cover:

- normal browser request
- HTMX `partial` request
- HTMX `full` request
- history restoration request
- `4xx` fragment response
- `5xx` safe error fragment
- response-header navigation and retargeting

## Version isolation

Keep HTMX 4 templates, vendored JavaScript, and tests isolated from HTMX
2 applications. Do not infer HTMX 4 adoption from generic `hx-*` attributes
alone; record the exact script version in the project.
