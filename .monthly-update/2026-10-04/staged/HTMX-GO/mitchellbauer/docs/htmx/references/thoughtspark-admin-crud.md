# ThoughtSpark Admin CRUD Patterns

This reference captures the HTMX patterns used by ThoughtSpark's admin interface.

## Shell plus swap-target tabs

Render one full admin shell, then load tab bodies into a stable panel.

- `GET /admin` returns the full page shell
- `GET /admin/prompts` returns the prompts table fragment
- `GET /admin/users` returns the users table fragment

This keeps navigation simple while avoiding a client-side router.

## Modal or side-panel editing

Load the form fragment on demand:

```html
<button
  hx-get="/admin/prompts/new"
  hx-target="#prompt-form"
  hx-swap="innerHTML">
  New prompt
</button>
```

The server returns only the form HTML. The same endpoint can also load an
existing record for edit mode.

## Mutation returns refreshed canonical fragment

ThoughtSpark does not hand-build row diffs in JavaScript. After create, update,
or delete, the server re-renders the prompts table and swaps it back in.

```go
func (h *AdminHandler) SavePrompt(w http.ResponseWriter, r *http.Request) {
    if err := h.Prompts.Save(p); err != nil {
        http.Error(w, "failed to save prompt", http.StatusInternalServerError)
        return
    }

    h.ListPrompts(w, r)
}
```

This trades some extra HTML for simpler state management and fewer UI edge cases.

## HTMX-triggered toasts

ThoughtSpark uses `HX-Trigger` to emit structured events after imports and bulk
actions.

```go
w.Header().Set("HX-Trigger", `{"showToast":{"level":"success","message":"Imported"}}`)
```

That is a strong fit when:

- the swapped fragment should stay focused on content
- a notification banner or toast is managed elsewhere in the page
- you want the server to control both the action result and the feedback event

## Multipart import flows

CSV imports still fit cleanly into HTMX:

- submit the multipart form with `hx-post`
- validate rows on the server
- trigger a toast summarizing inserted and skipped rows
- return the refreshed table fragment

This is often simpler than building a separate JSON upload API.
