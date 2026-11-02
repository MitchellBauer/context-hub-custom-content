# HTMX 4 Attributes and Events

## Familiar request attributes

- `hx-get`, `hx-post`, `hx-put`, `hx-patch`, `hx-delete`
- `hx-trigger`
- `hx-target`
- `hx-swap`
- `hx-select`
- `hx-include`
- `hx-vals`
- `hx-headers`
- `hx-encode`

## New or promoted controls

- `hx-action` plus `hx-method` separates request URL from method
- `hx-config` configures fetch behavior per element
- `hx-ignore` disables HTMX processing
- `hx-status` defines handling for response statuses
- `hx-preload` and `hx-optimistic` are first-class enhancement attributes

## Explicit inheritance

```html
<section hx-target:inherited="#results">
  <button hx-get="/search/recent">Recent</button>
</section>
```

Use `:append` to extend an inherited value.

## Event naming

HTMX 4 lifecycle names use additional colon-separated segments:

- `htmx:config:request`
- `htmx:before:request`
- `htmx:after:request`
- `htmx:finally:request`
- `htmx:before:swap`
- `htmx:after:swap`
- `htmx:finally:swap`
- `htmx:before:cleanup`
- `htmx:after:cleanup`

During the beta series, HTMX renamed `htmx:swap:finally` to `htmx:finally:swap`.

## Removed event groups

- validation lifecycle events were removed; use native form validation
- XHR progress/load events were removed because requests use `fetch()`

Use the `hx-multipart` extension when streamed multipart responses are
required.
