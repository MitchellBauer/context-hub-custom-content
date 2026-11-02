# Windows Win32 Clipboard Notes

## Relevant APIs

- `OpenClipboard`
- `EmptyClipboard`
- `SetClipboardData`
- `CloseClipboard`
- `GlobalAlloc`
- `GlobalLock`
- `GlobalUnlock`

## Rules that matter to Context

### Open/close discipline

- `OpenClipboard` prevents other applications from modifying clipboard content
  while it is open.
- Microsoft documents that `OpenClipboard` fails if another window already has
  the clipboard open.
- Every successful `OpenClipboard` should be paired with `CloseClipboard`.

### Ownership caveat

- Microsoft Learn states that if an application calls `OpenClipboard` with
  `hwnd = NULL`, then `EmptyClipboard` sets clipboard ownership to `NULL`, and
  this causes `SetClipboardData` to fail.

That means a console app should not assume `OpenClipboard(0)` is the safest
pattern just because it compiles.

### Memory lifetime

- `SetClipboardData` takes a handle, not a copied byte buffer.
- On success, ownership of the handle is transferred to the system.
- The caller must not free the handle after success.
- Before success, cleanup remains the caller's responsibility.

### Why `GMEM_MOVEABLE` still matters here

- Microsoft generally recommends heap functions for new code.
- Clipboard APIs are one of the notable legacy integration points where global
  movable memory is still part of the documented pattern.

### UTF-16 expectations

- `CF_UNICODETEXT` expects UTF-16 text.
- The buffer must be NUL-terminated.
- Embedded NULs are not valid for normal clipboard text flow.

## Sources

- [OpenClipboard](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-openclipboard)
- [EmptyClipboard](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-emptyclipboard)
- [SetClipboardData](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setclipboarddata)
- [GlobalAlloc](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globalalloc)
- [GlobalLock](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globallock)
- [GlobalUnlock](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globalunlock)