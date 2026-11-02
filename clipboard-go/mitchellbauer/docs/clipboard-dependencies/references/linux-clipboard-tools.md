# Linux Clipboard Tool Notes

## Tool priority in this project

The current non-Windows implementation checks for tools in this order:

1. `xclip`
2. `xsel`
3. `wl-copy`

That ordering matters because the tools target different display stacks.

For new code, choose by the active session before falling back by executable
availability:

1. Prefer `wl-copy` when `WAYLAND_DISPLAY` is set.
2. Prefer `xclip` or `xsel` when `DISPLAY` is set.
3. Return a useful error when no compatible display session and tool agree.

Merely finding `xclip` first does not mean it can reach an X server from a
Wayland-only session.

## `xclip`

- Reads from stdin by default.
- Uses the X11 selection model.
- Defaults to PRIMARY unless the clipboard selection is explicitly requested.
- The current code correctly uses `-selection clipboard`.

## `xsel`

- Operates on X11 selections.
- Defaults to PRIMARY selection unless the clipboard is explicitly requested.
- The current code correctly uses `--clipboard --input`.

## `wl-copy`

- Writes to the Wayland clipboard.
- Reads from stdin when no text argument is provided.
- May fork into the background by default.
- Supports MIME-aware clipboard content, though this project currently sends
  plain text only.

## Environment caveats

- `xclip` and `xsel` require a working X11 session or display forwarding.
- `wl-copy` requires a Wayland session.
- A machine can have multiple tools installed, but the first match in code
  controls behavior.

## Sources

- [xclip man page](https://www.mankier.com/1/xclip)
- [xsel man page](https://www.mankier.com/1/xsel.1x)
- [wl-clipboard man page](https://www.mankier.com/1/wl-clipboard)
- [wl-clipboard project](https://github.com/bugaevc/wl-clipboard)
