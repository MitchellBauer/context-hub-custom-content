# Fyne 2.8.0 Delta

## Pack update

- Previous version: `2.7.3`
- New version: `2.8.0`
- Released: July 11, 2026
- Minimum Go version: `1.22`

## Upgrade checks

1. Build and test with Go 1.22 or newer.
2. Move background-goroutine UI changes to `fyne.Do` or `fyne.DoAndWait`.
3. Check popup layouts because default padding was removed.
4. Rename uses of `canvas.Polygon` to `canvas.RegularPolygon`.
5. Test Linux applications under both Wayland and X11.
6. Reconfirm the supported Windows and macOS deployment targets.

## Notable additions

- scheduled notifications
- additional canvas primitives and shaders
- richer Markdown and form validation
- secondary monitor and window-position APIs
- optional accessibility support through the `accessibility` build tag

## Official source

- https://github.com/fyne-io/fyne/releases/tag/v2.8.0
