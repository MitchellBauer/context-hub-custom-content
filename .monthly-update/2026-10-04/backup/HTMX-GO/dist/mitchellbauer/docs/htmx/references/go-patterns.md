# Go Patterns for HTMX Apps

## One route, two render modes

This is the most practical server pattern for Go.

```go
func listTodos(w http.ResponseWriter, r *http.Request) {
    todos := repo.List(r.Context())

    if r.Header.Get("HX-Request") == "true" {
        renderTemplate(w, "todos-list", todos)
        return
    }

    renderTemplate(w, "todos-page", todos)
}
```

## Pre-parse template sets by surface area

ThoughtSpark keeps page templates, partials, and admin templates in separate
parsed sets. In Go this avoids block collisions and makes handler intent clear.

```go
type Templates struct {
    signup   *template.Template
    account  *template.Template
    partials *template.Template
    admin    *template.Template
}
```

This is a good pattern when:

- full pages share a layout
- partials are rendered independently for HTMX swaps
- an admin area has its own template names and blocks

## Form validation returns HTML

The official docs frame HTMX around HTML responses, so validation should usually re-render the form fragment rather than return JSON.

```go
type FormData struct {
    Values map[string]string
    Errors map[string]string
}

func createTodo(w http.ResponseWriter, r *http.Request) {
    _ = r.ParseForm()

    title := strings.TrimSpace(r.FormValue("title"))
    if title == "" {
        w.WriteHeader(http.StatusUnprocessableEntity)
        renderTemplate(w, "todo-form", FormData{
            Values: map[string]string{"title": title},
            Errors: map[string]string{"title": "Title is required"},
        })
        return
    }

    todo := repo.Create(r.Context(), title)
    renderTemplate(w, "todo-row", todo)
}
```

ThoughtSpark uses this pattern for signup and account flows: invalid input
returns an error partial, while success returns a success partial tailored to
the submitted values.

## Server-driven CRUD refreshes

For admin mutations, a simple and reliable pattern is:

1. parse and validate the form
2. save or delete on the server
3. re-render the table fragment
4. optionally emit `HX-Trigger` for a toast or follow-up action

This avoids stitching together row-level patches on the client.

## Out-of-band updates

When one action updates both a local target and a shared UI area like a flash banner, return both fragments and mark the shared one out of band.

```html
<div id="flash" hx-swap-oob="true">Saved</div>
<li id="todo-42">...</li>
```

ThoughtSpark uses a close cousin of this pattern with `HX-Trigger` response
headers to show toast notifications after CSV imports and bulk deletes.

## Search and filtering

```html
<form
  hx-get="/issues"
  hx-target="#issue-results"
  hx-trigger="change, submit, keyup changed delay:500ms from:#query">
  <input id="query" name="q" type="search" />
  <select name="status">
    <option value="">Any</option>
    <option value="open">Open</option>
    <option value="closed">Closed</option>
  </select>
</form>
```

## Testing strategy

Use `httptest` to assert both behaviors:

- full request returns page shell markup
- HTMX request returns fragment markup only
- invalid input returns an error status plus rendered inline errors
- redirect flows set the expected HTMX response header
- admin mutations return the expected refreshed fragment
