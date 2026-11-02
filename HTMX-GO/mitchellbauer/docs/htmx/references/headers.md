# HTMX Headers for Go Handlers

## Request headers from the official reference

- `HX-Boosted`: request came from `hx-boost`
- `HX-Current-URL`: current browser URL
- `HX-History-Restore-Request`: history restore request
- `HX-Prompt`: response to `hx-prompt`
- `HX-Request`: always `true` for HTMX requests
- `HX-Target`: target element id when present
- `HX-Trigger-Name`: triggering element name when present
- `HX-Trigger`: triggering element id when present

### Minimal helper

```go
func isHTMX(r *http.Request) bool {
    return r.Header.Get("HX-Request") == "true"
}
```

## Response headers from the official reference

- `HX-Location`: client-side redirect without a full reload
- `HX-Push-Url`: push a new URL into browser history
- `HX-Redirect`: redirect to another location
- `HX-Refresh`: force a full page refresh
- `HX-Replace-Url`: replace the current URL in history
- `HX-Reswap`: override swap strategy
- `HX-Retarget`: override target selector
- `HX-Reselect`: override selected response fragment
- `HX-Trigger`: emit client-side events
- `HX-Trigger-After-Settle`: emit events after settle
- `HX-Trigger-After-Swap`: emit events after swap

## HTMX 2.0.9 history note

HTMX 2.0.9 fixes `HX-Location` handling so `replace` is honored when `push` is
`false`. It also fixes relative history paths so they resolve against the
current page URL.

If a Go handler returns structured `HX-Location` JSON, test both push and
replace behavior:

```go
w.Header().Set(
    "HX-Location",
    `{"path":"../contacts","push":false,"replace":"/contacts"}`,
)
```

### Redirect example

```go
w.Header().Set("HX-Redirect", "/contacts")
w.WriteHeader(http.StatusOK)
```

### Server event example

```go
w.Header().Set("HX-Trigger", `{"contactSaved":{"id":"42"}}`)
renderTemplate(w, "contact-row", contact)
```

### Toast event pattern

ThoughtSpark uses `HX-Trigger` for admin notifications:

```go
payload := `{"showToast":{"level":"success","message":"Deleted 3 prompts."}}`
w.Header().Set("HX-Trigger", payload)
```

This is especially useful when the main response body is a table or form fragment
and the notification should be handled by a separate UI element.

## Status code guidance

- `200 OK` for a normal fragment response
- `201 Created` when a mutation creates a resource
- `204 No Content` when no swap body is needed
- `400` or `422` for invalid input, paired with rendered error HTML when useful
- `286` can stop polling according to the official docs

## CSRF note

HTMX does not remove CSRF concerns. Use the same protection you already rely on for standard Go forms.
