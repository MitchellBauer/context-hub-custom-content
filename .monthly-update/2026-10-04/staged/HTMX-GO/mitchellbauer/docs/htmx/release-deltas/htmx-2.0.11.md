# HTMX 2.0.11 Delta

Released September 22, 2026. Updates the previous 2.0.9 pack through 2.0.10.

- `<hx-partial hx-target="...">` in a response can update additional targets.
- Ancestor `hx-push-url="false"` works correctly with boosted descendants.
- Response-header checks avoid substring matches that could cause TypeError.
- Out-of-band targets resolve when the originating element has been detached.
- The intervening 2.0.10 release restores TypeScript declarations and improves settle selector escaping.

Existing 2.x Go request detection and response conventions remain applicable.
Do not apply HTMX 4 inheritance or event conventions to 2.x templates.

Source: https://raw.githubusercontent.com/bigskysoftware/htmx/master/CHANGELOG.md
