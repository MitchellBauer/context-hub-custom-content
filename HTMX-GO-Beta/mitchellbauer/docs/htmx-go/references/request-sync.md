# HTMX 4 Request Queueing (`hx-sync`)

Read from the 4.0.1 source (`RequestQueue` in `dist/htmx.js`). HTMX 4 uses
`hx-sync` for all queueing; HTMX 2's `queue` modifiers on `hx-trigger` are
gone.

## Where the queue lives

- Without `hx-sync`, each element has its own queue.
- `hx-sync="<selector>:<strategy>"` uses the queue of the element the selector
  finds (`closest`, `find`, `this` and other extended selectors work). Elements
  that name the same element share one queue.
- `hx-sync="<strategy>"` alone keeps the element's own queue.
- Choose a sync element that is not replaced by the swap (for example the
  form around the swapped area), or the queue goes away with it.

## Strategies

| Strategy | When a request is already running |
| --- | --- |
| *(none)* = `queue first` | Queue this one if the queue is empty; otherwise drop it. |
| `drop` | Drop this one. |
| `abort` | Drop this one. The running `abort` request is itself cancelled by any later non-`abort` request in the same queue. |
| `replace` | Abort the running request, clear the queue, run this one. |
| `queue last` | Replace whatever is queued with this one. |
| `queue all` | Queue every request in order. |

Unknown strategy text falls back to `queue first`.

## Values are captured at trigger time

The request body (form values, `hx-vals`, `hx-include`) is built before the
request is queued. A queued request sends what the form held when it was
triggered, even if the running request's response swapped the form away.
4.0.1 does skip the **swap** of a response whose target was removed from the
page, but the request itself is still sent.

## Recipes

Prevent a double submit (print, pay, save):

```html
<button hx-post="/print" hx-sync="closest form:drop" hx-disable="this">Print</button>
```

Search box (latest input wins):

```html
<input name="q" hx-get="/search" hx-trigger="input changed delay:300ms"
       hx-target="#results" hx-sync="this:replace">
```

Validate a field without blocking the form's submit:

```html
<input name="email" hx-post="/validate/email" hx-sync="closest form:abort">
```

The submit (non-`abort`) cancels a running validation request.

## Disabling controls during a request

`hx-disable="<selector>"` sets `disabled` on the matched elements while the
request runs and restores them afterwards (counted, so overlapping requests
don't enable too early). HTMX 2 called this `hx-disabled-elt`. HTMX 2's
`hx-disable` (stop processing a subtree) is HTMX 4's `hx-ignore`.

## 4.0.1 fixes

- An older response no longer overwrites a newer one under `hx-sync` replace
  (#4028).
- Indicators and disabled elements are tracked on the request context, so
  they are restored even when a queued request runs later.
- Any trigger now cancels a pending `delay` or `throttle` trigger on the same
  element, as in 2.x.

## Server side

`hx-sync` only covers one browser page. Make handlers that must not repeat
safe on their own: check state ("already printed"), or use an idempotency key
generated with the form.
