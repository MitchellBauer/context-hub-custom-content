# macOS `pbcopy` / `pbpaste` Notes

## Why it matters

On macOS, this project uses `pbcopy` and writes the generated text to the
command's standard input.

## Behavior

- `pbcopy` copies stdin to the general pasteboard by default.
- `pbpaste` reads from the general pasteboard by default.
- The tools use locale environment variables to determine encoding.
- UTF-8 is the recommended encoding path.

## Implications for Context

- Piping UTF-8 text from Go into `pbcopy` is the expected path.
- If locale settings are broken or unusually configured, text encoding issues are
  possible even when the Go string is correct.
- The current code path is simpler and less error-prone than the Windows native
  path because ownership and memory management are delegated to the OS tool.

## Source

- [pbcopy / pbpaste man page mirror](https://keith.github.io/xcode-man-pages/pbcopy.1.html)