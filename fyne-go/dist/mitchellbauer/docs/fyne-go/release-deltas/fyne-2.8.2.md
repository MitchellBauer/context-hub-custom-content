# Fyne 2.8.2 Delta

Release announcement: October 12, 2026. The Go module proxy records the tagged
commit at October 7, 2026. Updates this pack from 2.8.1 to 2.8.2.

## Changes worth checking

- Select's default placeholder follows the user's locale.
- Window dimensions are limited by the graphics driver's drawing capacity.
- Android retains read access to files and folders selected by the user.
- The X11 mobile simulator accepts keyboard input.

## Fixes relevant to desktop applications

- Fixed-size Windows windows recover correctly after minimization.
- Drop callbacks use the current drop position.
- File dialogs avoid a size-related nil-pointer crash.
- Long labels on Wayland, trailing-aligned selections, oversized child menus,
  image raster bounds, SVG output, and adjoining rectangle rendering receive fixes.
- Text and graphics performance improve; iOS typing latency and Android entry
  backspace behavior are also addressed.

Minimum Go remains 1.22. Existing 2.8 migration and GUI-thread rules still apply.
Exercise affected windows and widgets in each application's platform tests.

Sources:

- [Release announcement](https://github.com/fyne-io/fyne/releases/tag/v2.8.2)
- [Tagged module requirements](https://raw.githubusercontent.com/fyne-io/fyne/v2.8.2/go.mod)
- [Module proxy record](https://proxy.golang.org/fyne.io/fyne/v2/@v/v2.8.2.info)
