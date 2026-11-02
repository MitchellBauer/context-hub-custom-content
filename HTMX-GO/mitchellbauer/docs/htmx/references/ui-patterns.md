# UI Patterns for HTMX in Server-Rendered Go Apps

## Inline edit

1. `GET /items/42/edit` returns an edit form fragment.
2. `PUT /items/42` returns the updated display row.
3. Validation failure returns the same form fragment with inline errors.

## Modal editing

- load modal content with `hx-get`
- submit with `hx-post` or `hx-put`
- return the updated row plus any out-of-band UI updates

ThoughtSpark uses a practical variation:

- load the form fragment into a stable admin panel or modal container
- submit the form with HTMX
- return the refreshed table fragment instead of a single row diff
- emit a toast event with `HX-Trigger` when global feedback is useful

## Tabs and panels

- each tab button uses `hx-get`
- all buttons target the same content panel
- add `hx-push-url="true"` if the tab state should be linkable

This is a strong fit for Go admin screens where the outer shell is stable and
only the active panel needs to swap.

## Destructive actions

```html
<button
  hx-delete="/posts/42"
  hx-confirm="Archive this post?"
  hx-target="#post-42"
  hx-swap="outerHTML">
  Archive
</button>
```

## Polling and progress

```html
<div
  hx-get="/jobs/42/status"
  hx-trigger="every 2s"
  hx-target="this"
  hx-swap="outerHTML">
  Checking status...
</div>
```

This is often a good first step before introducing websockets or SSE.

## Progressive enhancement mindset

The official HTMX docs emphasize extending HTML rather than replacing it. In Go, that usually means:

- links still behave like real links
- forms still submit meaningful data
- the server remains the source of truth for rendered UI state

## Batch operations

ThoughtSpark's prompt admin also shows that batch actions fit the same model:

- submit selected row ids with one HTMX form
- perform the mutation on the server
- trigger a summary event
- return the refreshed table
