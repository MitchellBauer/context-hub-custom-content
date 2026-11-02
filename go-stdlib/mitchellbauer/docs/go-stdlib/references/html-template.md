# html/template and text/template

## Use `html/template` for HTML output

`html/template` provides contextual auto-escaping for HTML templates and should be
the default choice for server-rendered web apps.

## Practical patterns

- parse templates at startup
- keep page templates and fragment templates separate
- pass explicit data structs to templates
- keep helper functions small if you add a `FuncMap`

## Important distinction

- `html/template` is for HTML output
- `text/template` is for non-HTML text output

If you render HTML with `text/template`, you lose the safety benefits of HTML-aware escaping.

## Current release guidance

The current Go 1.27.3 target includes the html/template security fixes from
1.27.2. See `release-deltas/go1.27.2.md` and `release-deltas/go1.27.3.md`.
