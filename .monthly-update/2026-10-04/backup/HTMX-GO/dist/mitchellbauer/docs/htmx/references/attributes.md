# HTMX Attributes That Matter Most in Go

## Core attributes from the official reference

The HTMX reference lists these as the core attributes:

- `hx-get`
- `hx-post`
- `hx-on*`
- `hx-push-url`
- `hx-select`
- `hx-select-oob`
- `hx-swap`
- `hx-swap-oob`
- `hx-target`
- `hx-trigger`
- `hx-vals`

## Additional attributes you will use often in Go apps

- `hx-boost` for progressive enhancement of links and forms
- `hx-delete`, `hx-put`, `hx-patch` for mutation routes
- `hx-disabled-elt` to prevent duplicate submissions
- `hx-headers` for extra request headers such as CSRF
- `hx-include` to include related inputs in a request
- `hx-indicator` for loading states
- `hx-params` to filter submitted parameters
- `hx-replace-url` when state should replace current history
- `hx-request` for request options
- `hx-sync` to coordinate overlapping requests
- `hx-validate` for validation behavior

HTMX 2.0.9 preserves elements that were already disabled in the source HTML
when `hx-disabled-elt` finishes a request. Do not rely on HTMX to enable a
control that your server-rendered template intentionally marked `disabled`.

## Swap choices

- `innerHTML` replaces target contents
- `outerHTML` replaces the entire target element
- `beforebegin`, `afterbegin`, `beforeend`, `afterend` insert around or inside the target

Use `outerHTML` only when the server returns the wrapping node.

## Trigger patterns from the docs

The official docs highlight these trigger patterns:

- natural element events by default
- `mouseenter` or other explicit DOM events
- `once`
- `changed`
- `delay:<time>`
- `throttle:<time>`
- `from:<selector>`
- special events like `load`, `revealed`, and `intersect`
- polling with `every 2s`

### Search example

```html
<input
  type="text"
  name="q"
  hx-get="/search"
  hx-trigger="keyup changed delay:500ms"
  hx-target="#search-results"
  placeholder="Search...">
<div id="search-results"></div>
```

## Go advice

- Keep one obvious target per interaction.
- Name fragment templates to match the DOM block they replace.
- Reach for `hx-select` only when returning a larger response is simpler than rendering a dedicated fragment.
- Prefer `hx-boost` for navigation before adding lots of per-element request attributes.
