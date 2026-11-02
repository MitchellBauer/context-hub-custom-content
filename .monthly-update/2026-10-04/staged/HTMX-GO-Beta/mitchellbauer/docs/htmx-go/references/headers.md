# HTMX 4 Headers for Go Handlers

## Request headers

- `HX-Request`: request originated from HTMX
- `HX-Request-Type`: `partial` or `full`
- `HX-Current-URL`: browser URL at request start
- `HX-Source`: source element as `tagName#id`
- `HX-Target`: target element as `tagName#id`
- `HX-Boosted`: boosted navigation
- `HX-History-Restore-Request`: back/forward restoration
- `Accept`: explicitly includes `text/html`

Do not parse `HX-Target` as a bare element ID in migrated Go code.

```go
func isPartialHTMX(r *http.Request) bool {
    return r.Header.Get("HX-Request") == "true" &&
        r.Header.Get("HX-Request-Type") == "partial"
}
```

## Removed request headers

- HTMX 2 request `HX-Trigger`: use `HX-Source`
- `HX-Trigger-Name`: use `HX-Source`
- `HX-Prompt`: restored by the `hx-prompt` extension when needed

## Response headers

Still supported:

- `HX-Trigger`
- `HX-Location`
- `HX-Push-Url`
- `HX-Redirect`
- `HX-Refresh`
- `HX-Replace-Url`
- `HX-Retarget`
- `HX-Reswap`
- `HX-Reselect`

Removed:

- `HX-Trigger-After-Swap`
- `HX-Trigger-After-Settle`

Events declared by the `HX-Trigger` response header fire after the
swap.

## Cache variation

When one Go route returns both complete pages and fragments:

```go
w.Header().Add("Vary", "HX-Request")
w.Header().Add("Vary", "HX-Request-Type")
w.Header().Add("Vary", "HX-History-Restore-Request")
```

Choose the exact `Vary` fields that affect your representation.
