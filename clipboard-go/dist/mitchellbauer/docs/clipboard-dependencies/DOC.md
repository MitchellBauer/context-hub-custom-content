---
name: clipboard-dependencies
description: "Clipboard dependency guide for the Context CLI across Windows, macOS, X11, and Wayland"
metadata:
  languages: "go"
  versions: "1.0.0"
  revision: 2
  updated-on: "2026-07-28"
  source: community
  tags: "clipboard,windows,macos,linux,go,context"
---

# Clipboard Dependencies for Context

This doc pack narrows the external dependency surface for the Context CLI down to
the clipboard layer, which is the only nontrivial platform integration in the
current codebase.

## Why this matters in this repo

The project code relies on:

- Windows Win32 clipboard APIs in `clipboard_windows.go`
- Command-line clipboard tools on non-Windows in `clipboard_nonwindows.go`

Everything else is mostly Go standard library and local file processing.

## Dependency map

### Windows

- `OpenClipboard`
- `EmptyClipboard`
- `SetClipboardData`
- `CloseClipboard`
- `GlobalAlloc`
- `GlobalLock`
- `GlobalUnlock`
- `CF_UNICODETEXT`

See `references/windows-win32.md`.

### macOS

- `pbcopy`
- `pbpaste`

See `references/macos-pbcopy.md`.

### Linux / BSD desktop environments

- `xclip` for X11
- `xsel` for X11
- `wl-copy` for Wayland

See `references/linux-clipboard-tools.md`.

## High-value rules

### Windows ownership and memory rules

- Clipboard writes are serialized. `OpenClipboard` can fail if another app still
  owns the clipboard, so retry logic is reasonable.
- `SetClipboardData` transfers ownership of the memory handle to the system on
  success. The caller must not free or reuse that handle after success.
- Clipboard text for `CF_UNICODETEXT` must be UTF-16 and NUL-terminated.
- The clipboard API still expects global movable memory for this path, even
  though newer apps otherwise prefer heap allocation APIs.

### Windows caution for this project

Microsoft Learn says that if `OpenClipboard` is called with `NULL`, then
`EmptyClipboard` sets the owner to `NULL`, which causes `SetClipboardData` to
fail. That is directly relevant to the current implementation because it opens
the clipboard with a null owner.

Treat that as a concrete audit item before making further Windows clipboard
changes.

### macOS and Linux command behavior

- `pbcopy` reads from standard input and uses locale settings to determine text
  encoding; UTF-8 is the recommended path.
- `xclip` defaults to the X11 PRIMARY selection unless `-selection clipboard` is
  used.
- `xsel` also defaults to PRIMARY unless the clipboard is explicitly requested.
- `wl-copy` reads from stdin when no text arguments are given and may fork into
  the background unless foreground mode is requested.

## Suggested ingestion workflow

1. Keep this entry as the overview.
2. Put platform-specific rules in the reference files.
3. Rev the `metadata.revision` field whenever you materially update the content.
4. If the project starts depending on a third-party Go clipboard library later,
   add a second doc entry instead of mixing package docs into this entry.

## Versioning note

This pack has no upstream semantic version because it covers operating-system
APIs and independently released command-line tools. Pack revision 2 refreshes
the source guidance without claiming that those dependencies share one version.

## Source links

- Microsoft Learn: OpenClipboard, EmptyClipboard, SetClipboardData, GlobalAlloc,
  GlobalLock, GlobalUnlock
- Apple `pbcopy` / `pbpaste` man page mirror
- `wl-clipboard` man page
- `xclip` and `xsel` man pages

Use the reference files for direct links and excerpts.
