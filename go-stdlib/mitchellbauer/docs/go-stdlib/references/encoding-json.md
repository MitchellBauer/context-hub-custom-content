# encoding/json

## Good fit

Use `encoding/json` for API payloads, config files, and machine-readable output.

## Practical patterns

- define explicit structs for stable payloads
- use `json.Decoder` for streamed request bodies
- prefer explicit tags when JSON field names matter
- validate decoded data after parsing

## Common reminder

For server-rendered HTML apps, not every interaction should become JSON just because JSON is available.
